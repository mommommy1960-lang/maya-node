/** Real loopback HTTP → test-injected tenant gate → SQLite regressions.
 * Identity headers below are deliberately TEST-ONLY fixtures, NOT sessions,
 * passwords, production authentication, or independent customer actors.
 * The ordinary /api/action route remains an intentionally untrusted demo.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createLocalDemo } from './synthetic-local-demo-server.mjs';

const participants = {
  donor: 'fictional-donor',
  receiver: 'fictional-receiver',
  transport: 'fictional-transporter'
};
const fixtures = new Map([
  ...Object.entries(participants).map(([role, actorId]) =>
    [role, {authenticated:true,tenantId:'SYN-coalition-A',role,actorId}]),
  ['other-tenant', {authenticated:true,tenantId:'SYN-coalition-B',role:'donor',actorId:participants.donor}],
  ['wrong-actor', {authenticated:true,tenantId:'SYN-coalition-A',role:'donor',actorId:'SYN-attacker'}],
  ['operator', {authenticated:true,tenantId:'SYN-coalition-A',role:'operator',actorId:'SYN-admin'}]
]);
const resolver = req => fixtures.get(req.headers['x-syn-session']) ?? null;
async function withDemo(fn, opts = {}) {
  const app = createLocalDemo(opts);
  const url = await app.listen();
  try { return await fn(url, app); }
  finally { await app.close(); }
}
async function route(url, identity, action, extra = {}) {
  const response = await fetch(url + '/api/tenant-order', {
    method:action?'POST':'GET',
    headers:{...(identity?{'x-syn-session':identity}:{}),
      ...(action?{'content-type':'application/json'}:{})},
    ...(action?{body:JSON.stringify({action,...extra})}:{})
  });
  return [response.status, await response.json()];
}
async function demo(url, action, extra = {}) {
  const response = await fetch(url + '/api/action', {
    method:'POST', headers:{'content-type':'application/json'},
    body:JSON.stringify({action,...extra})
  });
  return [response.status, await response.json()];
}
async function ready(url, app) {
  assert.equal((await demo(url,'start'))[0],200);
  // Direct in-process fixture setup, intentionally not exposed over HTTP.
  app.tenantGate.provisionForSyntheticTest('SYN-DEMO-ORDER','SYN-coalition-A',100);
}

test('tenant HTTP route is closed unless an independent server-side test resolver is installed',async()=>withDemo(async url=>{
  const [status, body] = await route(url,null);
  assert.equal(status,403);
  assert.equal(body.error,'tenant_route_unavailable');
  assert.equal((await demo(url,'start'))[0],200);
  assert.equal((await route(url,'donor'))[0],403);
}));

test('missing principal, cross-tenant and cross-actor HTTP reads fail before leaking order data',async()=>withDemo(async(url,app)=>{
  await ready(url,app);
  for(const session of [null,'other-tenant','wrong-actor','forged']) {
    const [status,body] = await route(url,session);
    assert.equal(status,403);assert.equal(Object.hasOwn(body,'order'),false);
  }
  const [status,body]=await route(url,'receiver');
  assert.equal(status,200);
  assert.equal(body.order.id,'SYN-DEMO-ORDER');
  assert.equal(body.synthetic,true);
  assert.equal(Object.hasOwn(body,'commercial'),false);
  // Scoped receiver may now view a receipt, but none exists before pickup.\n  assert.equal(body.receipt,null);
},{resolveServerPrincipal:resolver}));

test('HTTP approval uses server-selected fictional role, never client identity fields',async()=>withDemo(async(url,app)=>{
  await ready(url,app);
  for(const extra of [{role:'donor'},{actorId:'fictional-donor'},{tenantId:'SYN-coalition-A'},{authenticated:true}]) {
    const [status,body]=await route(url,'receiver','approve',extra);
    assert.equal(status,403); assert.equal(body.error,'client_identity_claim_denied');
  }
  assert.equal((await route(url,'wrong-actor','approve'))[0],403);
  assert.equal((await route(url,'other-tenant','approve'))[0],403);
  assert.equal((await route(url,'operator','approve'))[0],403);
  const results=await Promise.all(['receiver','donor','transport'].map(id=>route(url,id,'approve')));
  results.forEach(([status])=>assert.equal(status,200));
  const [,body]=await route(url,'donor');
  assert.deepEqual(body.order.approvals.map(a=>a.actorId).sort(),Object.values(participants).sort());
  assert.equal(body.order.state,'approved');
},{resolveServerPrincipal:resolver}));

test('guarded pickup refuses fake payment bypass and wrong actor; no outside side effects',async()=>withDemo(async(url,app)=>{
  await ready(url,app);
  assert.equal((await route(url,'transport','pickup'))[0],409);
  for(const who of ['donor','receiver','transport'])
    assert.equal((await route(url,who,'approve'))[0],200);
  assert.equal((await route(url,'donor','pickup'))[0],403); // deny wrong role before inspecting payment state
  assert.equal((await route(url,'transport','pickup'))[0],409);
  for(const action of ['quote','accept-terms','mock-authorize'])
    assert.equal((await demo(url,action))[0],200); // test-only commercial fixture
  assert.equal((await route(url,'donor','pickup'))[0],403);
  const [status,body]=await route(url,'transport','pickup');
  assert.equal(status,200);assert.equal(body.order.state,'picked_up');
  assert.equal((await route(url,'receiver','cancel'))[0],409);
  assert.equal(app.ledger.available('SYN-TRUCK'),4);
},{resolveServerPrincipal:resolver}));

test('guarded tenant HTTP authorization and immutable binding survive SQLite restart',async()=>{
  const dir=mkdtempSync(join(tmpdir(),'maya-http-tenant-'));
  const filename=join(dir,'synthetic.sqlite');
  try {
    await withDemo(async(url,app)=>{
      await ready(url,app);
      assert.equal((await route(url,'donor','approve'))[0],200);
    },{filename,resolveServerPrincipal:resolver});
    await withDemo(async(url,app)=>{
      assert.equal((await route(url,'other-tenant'))[0],403);
      assert.equal((await route(url,'wrong-actor','approve'))[0],403);
      const [status,body]=await route(url,'receiver','approve');
      assert.equal(status,200);assert.equal(body.order.approvals.length,2);
      assert.throws(()=>app.tenantGate.provisionForSyntheticTest('SYN-DEMO-ORDER','SYN-coalition-B',200),/tenant_binding_conflict/);
      assert.equal((await route(url,'receiver','delete'))[0],403);
    },{filename,resolveServerPrincipal:resolver});
  } finally {rmSync(dir,{recursive:true,force:true});}
});
