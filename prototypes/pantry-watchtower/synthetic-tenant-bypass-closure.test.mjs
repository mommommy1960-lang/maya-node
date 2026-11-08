/**
 * Nonproduction HTTP bypass-closure tests for Maya's opt-in tenant boundary.
 * The resolver maps a spoofable header to fictional principals solely for
 * automated testing. It is NOT login or permission to expose this server.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createLocalDemo } from './synthetic-local-demo-server.mjs';

const actors = {
  donor: { authenticated:true, tenantId:'SYN-A', role:'donor', actorId:'fictional-donor' },
  receiver: { authenticated:true, tenantId:'SYN-A', role:'receiver', actorId:'fictional-receiver' },
  transport: { authenticated:true, tenantId:'SYN-A', role:'transport', actorId:'fictional-transporter' },
  outsider: { authenticated:true, tenantId:'SYN-B', role:'donor', actorId:'fictional-donor' },
  impostor: { authenticated:true, tenantId:'SYN-A', role:'transport', actorId:'other-transporter' },
};
const fakeResolver = req => actors[req.headers['x-syn-session']] ?? null;

async function withGuard(fn, options={}) {
  const app = createLocalDemo({
    tenantGuardedOnly:true, resolveServerPrincipal:fakeResolver, ...options
  });
  const url = await app.listen();
  try { return await fn(url, app); }
  finally { await app.close(); }
}
function seedInProcess(app) {
  app.act({action:'start'}); // only a trusted local test fixture can create it
  app.tenantGate.provisionForSyntheticTest('SYN-DEMO-ORDER','SYN-A',100);
}
async function call(url,path,{method='GET',who=null,action=null,origin=null}={}) {
  const headers = { ...(who?{'x-syn-session':who}:{}),
    ...(origin?{origin}:{}),
    ...(method==='POST'?{'content-type':'application/json'}:{}) };
  const r=await fetch(url+path, {method,headers,
    ...(method==='POST'?{body:JSON.stringify({action})}:{})});
  return [r.status, await r.json()];
}
const legacy = ['/api/state','/api/action','/','/synthetic-journey-client.mjs'];

test('guarded mode requires an explicit test resolver and a boolean flag',()=>{
  assert.throws(()=>createLocalDemo({tenantGuardedOnly:true}),/tenant_guarded_mode_requires_test_resolver/);
  assert.throws(()=>createLocalDemo({tenantGuardedOnly:'true',resolveServerPrincipal:fakeResolver}),/invalid_tenant_guarded_mode/);
});

test('strict tenant mode blocks every untrusted state, mutation and browser route even with a fictional principal',async()=>withGuard(async(url,app)=>{
  seedInProcess(app);
  const before=app.snapshot();
  for(const path of legacy) {
    const [status,body]=await call(url,path,{who:'donor'});
    assert.equal(status,403,path);
    assert.deepEqual(body,{error:'untrusted_demo_routes_disabled'});
    assert.equal(Object.hasOwn(body,'order'),false);
  }
  for(const action of ['start','approve','quote','accept-terms','mock-authorize','pickup','deliver','cancel']) {
    const [status,body]=await call(url,'/api/action',{method:'POST',who:'donor',action});
    assert.equal(status,403,action); assert.deepEqual(body,{error:'untrusted_demo_routes_disabled'});
  }
  assert.deepEqual(app.snapshot(),before,'blocked requests must not mutate or expose SQLite state');
  const [status,body]=await call(url,'/api/tenant-order',{who:'donor'});
  assert.equal(status,200);assert.equal(body.order.id,'SYN-DEMO-ORDER');
  assert.equal(body.identityMode,'SERVER_INJECTED_TEST_DOUBLE_NOT_REAL_AUTH');
}));

test('protected approval still works, but cross-tenant HTTP and old demo impersonation cannot bypass it',async()=>withGuard(async(url,app)=>{
  seedInProcess(app);
  assert.equal((await call(url,'/api/tenant-order',{who:'outsider'}))[0],403);
  assert.equal((await call(url,'/api/tenant-order',{method:'POST',who:'outsider',action:'approve'}))[0],403);
  assert.equal((await call(url,'/api/tenant-order',{method:'POST',who:'receiver',action:'approve'}))[0],200);
  assert.equal((await call(url,'/api/action',{method:'POST',who:'donor',action:'approve'}))[0],403);
  const [status,read]=await call(url,'/api/tenant-order',{who:'donor'});
  assert.equal(status,200);
  assert.deepEqual(read.order.approvals.map(a=>a.role),['receiver']);
  assert.equal((await call(url,'/api/tenant-order',{method:'POST',who:'donor',action:'approve'}))[0],200);
  assert.equal(app.orders.get('SYN-DEMO-ORDER').approvals.length,2);
}));

test('old demo bypass remains closed across SQLite restart while tenant binding persists',async()=>{
  const dir=mkdtempSync(join(tmpdir(),'maya-guarded-closure-'));
  const filename=join(dir,'demo.sqlite');
  try {
    await withGuard(async(url,app)=>{
      seedInProcess(app);
      assert.equal((await call(url,'/api/tenant-order',{method:'POST',who:'donor',action:'approve'}))[0],200);
    },{filename});
    await withGuard(async(url,app)=>{
      for(const path of legacy)
        assert.equal((await call(url,path,{who:'receiver'}))[0],403);
      assert.equal((await call(url,'/api/action',{method:'POST',action:'cancel'}))[0],403);
      assert.equal((await call(url,'/api/tenant-order',{who:'outsider'}))[0],403);
      const [status,body]=await call(url,'/api/tenant-order',{who:'receiver'});
      assert.equal(status,200);
      assert.deepEqual(body.order.approvals.map(a=>a.role),['donor']);
      assert.equal(app.ledger.available('SYN-TRUCK'),4);
    },{filename});
  } finally { rmSync(dir,{recursive:true,force:true}); }
});

test('strict mode rejects cross-origin requests and never serves the untrusted UI as a fallback',async()=>withGuard(async(url,app)=>{
  seedInProcess(app);
  assert.equal((await call(url,'/api/tenant-order',{who:'donor',origin:'https://attacker.example'}))[0],403);
  assert.equal((await call(url,'/',{who:'donor'}))[0],403);
  assert.equal((await call(url,'/api/state'))[0],403);
  assert.equal(app.orders.get('SYN-DEMO-ORDER').state,'reserved');
}));


test('guarded pickup hides fictional payment status from unauthenticated or unauthorized actors',async()=>withGuard(async(url,app)=>{
  seedInProcess(app);
  for(const role of ['donor','receiver','transport']) app.act({action:'approve',role});
  const denied = [null,'outsider','donor','impostor'];
  async function checkUnauthorized() {
    const before = app.snapshot();
    for(const who of denied) {
      const [status,body] = await call(url,'/api/tenant-order',{method:'POST',who,action:'pickup'});
      assert.equal(status,403,'unauthorized pickup must not reveal commercial progress');
      assert.equal(Object.hasOwn(body,'order'),false);
      assert.notEqual(body.error,'mock_authorization_required');
    }
    assert.deepEqual(app.snapshot(),before,'denied calls must not mutate fictional order');
  }
  await checkUnauthorized(); // no mock authorization yet
  assert.equal((await call(url,'/api/tenant-order',{method:'POST',who:'transport',action:'pickup'}))[0],409);
  for(const action of ['quote','accept-terms','mock-authorize']) app.act({action}); // trusted in-process fixture
  await checkUnauthorized(); // authorized mock state must not change unauthorized response
  const [status,body]=await call(url,'/api/tenant-order',{method:'POST',who:'transport',action:'pickup'});
  assert.equal(status,200);
  assert.equal(body.order.state,'picked_up');
}));
