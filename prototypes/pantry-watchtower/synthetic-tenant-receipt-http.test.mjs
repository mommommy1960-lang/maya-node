/** Synthetic-only receiver receipt over guarded loopback HTTP, NOT real authentication.
 * Test session headers are intentionally spoofable server-injected fixtures.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createLocalDemo } from './synthetic-local-demo-server.mjs';

const actor = {
  donor: {authenticated:true, tenantId:'SYN-A', role:'donor', actorId:'fictional-donor'},
  receiver: {authenticated:true, tenantId:'SYN-A', role:'receiver', actorId:'fictional-receiver'},
  transport: {authenticated:true, tenantId:'SYN-A', role:'transport', actorId:'fictional-transporter'},
  wrongTenant: {authenticated:true, tenantId:'SYN-B', role:'receiver', actorId:'fictional-receiver'},
  wrongReceiver: {authenticated:true, tenantId:'SYN-A', role:'receiver', actorId:'fictional-impostor'}
};
const resolver = req => actor[req.headers['x-syn-session']] ?? null;
async function withGuard(fn, opts={}) {
  const app=createLocalDemo({clock:()=>1000, tenantGuardedOnly:true, resolveServerPrincipal:resolver, ...opts});
  const url=await app.listen();
  try {return await fn(url,app);}
  finally {await app.close();}
}
async function call(url,who,action,extra={}) {
  const response=await fetch(url+'/api/tenant-order',{
    method:action?'POST':'GET',
    headers:{...(who?{'x-syn-session':who}:{}),...(action?{'content-type':'application/json'}:{})},
    ...(action?{body:JSON.stringify({action,...extra})}:{})
  });
  return [response.status,await response.json()];
}
function seed(app) {
  app.act({action:'start'}); // fixture ONLY, never a public creation API
  app.tenantGate.provisionForSyntheticTest('SYN-DEMO-ORDER','SYN-A',1000);
}
async function preparedForDelivery(url,app) {
  seed(app);
  for (const who of ['donor','receiver','transport'])
    assert.equal((await call(url,who,'approve'))[0],200);
  for (const action of ['quote','accept-terms','mock-authorize'])
    app.act({action}); // fake commercial state, never Stripe or money
  assert.equal((await call(url,'transport','pickup'))[0],200);
}

test('guarded delivery refuses unauthenticated, cross-tenant and wrong-role receiver attempts without a state oracle',async()=>withGuard(async(url,app)=>{
  seed(app);
  for(const who of [null,'wrongTenant','wrongReceiver','donor','transport']) {
    const before=app.snapshot();
    const [status,body]=await call(url,who,'deliver',{mode:'partial'});
    assert.equal(status,403);
    assert.equal(Object.hasOwn(body,'receipt'),false);
    assert.deepEqual(app.snapshot(),before);
  }
  // Authorized receiver learns only that pickup has not happened.
  assert.equal((await call(url,'receiver','deliver',{mode:'full'}))[0],409);
  assert.equal(app.delivery.getReceipt('SYN-DEMO-ORDER'),null);
  assert.equal((await call(url,'donor'))[1].receipt,undefined);
}));

test('guarded full receiver delivery settles bundle, preserves zero food restock and shows only receiver receipt',async()=>withGuard(async(url,app)=>{
  await preparedForDelivery(url,app);
  for (const who of [null,'wrongTenant','wrongReceiver','donor','transport']) {
    const before=app.snapshot();
    assert.equal((await call(url,who,'deliver',{mode:'bogus'}))[0],403);
    assert.deepEqual(app.snapshot(),before);
  }
  assert.equal((await call(url,'receiver','deliver',{mode:'bogus'}))[0],409);
  assert.equal((await call(url,'receiver','deliver',{mode:'full',actorId:'fictional-donor'}))[0],403);
  const [status,body]=await call(url,'receiver','deliver',{mode:'full'});
  assert.equal(status,200);
  assert.equal(body.order.state,'reconciled');
  assert.equal(body.receipt.received,8);
  assert.equal(body.receipt.missing,0);
  assert.equal(body.receipt.verifiedSignature,false);
  assert.equal(app.ledger.available('SYN-FOOD'),4);
  assert.equal(app.ledger.available('SYN-COLD'),12);
  assert.equal(app.ledger.available('SYN-TRUCK'),12);
  const [,donorRead]=await call(url,'donor');
  assert.equal(Object.hasOwn(donorRead,'receipt'),false);
  assert.equal((await call(url,'receiver'))[1].receipt.id,'SYN-DEMO-RECEIPT');
}));

test('partial guarded receipt and receiver-only exception review survive SQLite restart',async()=>{
  const dir=mkdtempSync(join(tmpdir(),'maya-guarded-receipt-'));
  const filename=join(dir,'orders.sqlite');
  try {
    await withGuard(async(url,app)=>{
      await preparedForDelivery(url,app);
      const [status,partial]=await call(url,'receiver','deliver',{mode:'partial'});
      assert.equal(status,200);
      assert.equal(partial.order.state,'exception');
      assert.equal(partial.receipt.received,6);
      assert.equal(partial.receipt.rejected,1);
      assert.equal(partial.receipt.missing,1);
      assert.equal(app.ledger.available('SYN-FOOD'),4);
      assert.equal((await call(url,'donor','document-exception'))[0],403);
      assert.equal((await call(url,'wrongTenant','document-exception'))[0],403);
      assert.equal((await call(url,'wrongReceiver','document-exception'))[0],403);
      assert.equal(app.delivery.getReceipt('SYN-DEMO-ORDER').disposition,null);
    },{filename});
    await withGuard(async(url,app)=>{
      assert.equal((await call(url,'wrongTenant'))[0],403);
      const [status,review]=await call(url,'receiver','document-exception');
      assert.equal(status,200);
      assert.equal(review.order.state,'reconciled');
      assert.equal(review.receipt.disposition.code,'exception_documented');
      assert.equal(review.receipt.received,6);
      assert.equal(app.ledger.available('SYN-FOOD'),4);
      assert.equal(app.ledger.available('SYN-TRUCK'),12);
      assert.equal((await call(url,'donor'))[1].receipt,undefined);
    },{filename});
  } finally {rmSync(dir,{recursive:true,force:true});}
});
