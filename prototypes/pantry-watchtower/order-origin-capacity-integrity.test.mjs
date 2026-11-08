/** Fault-injection tests: one corrupted bundle must never mint fictional capacity.
 * Synthetic-only data, no external identity, payments, or real dispatch.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {ReservationLedger} from './reservation-ledger.mjs';
import {SyntheticOrderStore} from './synthetic-order-store.mjs';
import {SyntheticDeliverySettlement} from './synthetic-delivery-settlement.mjs';

const parties={donor:'synthetic-donor',receiver:'synthetic-receiver',transport:'synthetic-driver'};
const input=()=>({id:'synthetic-order',offerId:'fictional-offer',needId:'fictional-need',quantity:3,parties,at:100,
  bundle:{id:'synthetic-bundle',expiresAt:200,items:['food','cold','truck'].map(resourceId=>({resourceId,quantity:3}))}});
function setup(file=':memory:'){
  const l=new ReservationLedger(file);
  for(const name of ['food','cold','truck'])l.seedResource(name,20);
  const s=new SyntheticOrderStore(l);
  return {l,s,d:new SyntheticDeliverySettlement(s)};
}
const capacity=l=>['food','cold','truck'].map(id=>l.available(id));
const approve=s=>{
  for(const [role,actorId] of Object.entries(parties))
    s.approve({id:'synthetic-order',role,actorId,evidenceRef:'fictional-'+role,at:120});
};
function alterBundleAndHold(l,resourceId,newQuantity) {
  const signature=JSON.parse(l.db.prepare("SELECT signature FROM bundles WHERE id='synthetic-bundle'").get().signature);
  signature.items.find(x=>x.resourceId===resourceId).quantity=newQuantity;
  l.db.prepare("UPDATE bundles SET signature=? WHERE id='synthetic-bundle'").run(JSON.stringify(signature));
  l.db.prepare("UPDATE holds SET quantity=? WHERE id=?").run(newQuantity,'synthetic-bundle:'+resourceId);
}
test('coordinated signed-bundle and hold quantity edits cannot mint capacity on cancellation',()=>{
  const {l,s}=setup();try {
    s.createReserved(input());
    alterBundleAndHold(l,'food',6); // Only three units were actually debited.
    const before=capacity(l);
    assert.deepEqual(before,[17,17,17]);
    assert.throws(()=>s.approve({id:'synthetic-order',role:'donor',actorId:parties.donor,evidenceRef:'fictional',at:120}),/corrupt_order_reservation/);
    assert.throws(()=>s.cancel({id:'synthetic-order',actorId:parties.donor,evidenceRef:'fictional',at:130}),/corrupt_order_reservation/);
    assert.deepEqual(capacity(l),before,'no phantom replenishment');
    assert.equal(s.get('synthetic-order').state,'reserved');
    assert.equal(s.get('synthetic-order').approvals.length,0);
  }finally{l.close();}
});
test('coordinated expiry extension cannot change the source order deadline',()=>{
  const {l,s}=setup();try{
    s.createReserved(input());
    const signature=JSON.parse(l.db.prepare("SELECT signature FROM bundles WHERE id='synthetic-bundle'").get().signature);
    signature.expiresAt=300;
    l.db.prepare("UPDATE bundles SET signature=? WHERE id='synthetic-bundle'").run(JSON.stringify(signature));
    l.db.prepare("UPDATE holds SET expires_at=300 WHERE id LIKE 'synthetic-bundle:%'").run();
    assert.throws(()=>s.approve({id:'synthetic-order',role:'donor',actorId:parties.donor,evidenceRef:'fictional',at:150}),/corrupt_order_reservation/);
    assert.deepEqual(capacity(l),[17,17,17]);
  }finally{l.close();}
});
test('malformed original order signature must not authorize or replenish capacity',()=>{
  const {l,s}=setup();try{
    s.createReserved(input());
    l.db.prepare("UPDATE synthetic_orders SET signature='not-json' WHERE id='synthetic-order'").run();
    assert.throws(()=>s.cancel({id:'synthetic-order',actorId:parties.donor,evidenceRef:'fictional',at:150}),/corrupt_order_reservation/);
    assert.deepEqual(capacity(l),[17,17,17]);
    assert.equal(s.get('synthetic-order').state,'reserved');
  }finally{l.close();}
});
test('picked-up tampered bundle cannot over-credit cold or truck slots on receipt',()=>{
  const {l,s,d}=setup();try{
    s.createReserved(input());approve(s);
    s.pickup({id:'synthetic-order',actorId:parties.transport,evidenceRef:'fictional-manifest',at:130});
    alterBundleAndHold(l,'cold',6);
    const before=capacity(l);
    assert.throws(()=>d.recordReceipt({id:'synthetic-order',receiptId:'fictional-receipt',actorId:parties.receiver,
      evidenceRef:'fictional',foodResourceId:'food',received:3,rejected:0,damaged:0,at:140}),/corrupt_order_reservation/);
    assert.deepEqual(capacity(l),before);
    assert.equal(s.get('synthetic-order').state,'picked_up');
    assert.equal(d.getReceipt('synthetic-order'),null);
  }finally{l.close();}
});
test('untampered pickup extension still settles full receipt with conserved slots',()=>{
  const {l,s,d}=setup();try{
    s.createReserved(input());approve(s);
    s.pickup({id:'synthetic-order',actorId:parties.transport,evidenceRef:'fictional-manifest',at:130});
    const result=d.recordReceipt({id:'synthetic-order',receiptId:'fictional-receipt',actorId:parties.receiver,
      evidenceRef:'fictional',foodResourceId:'food',received:3,rejected:0,damaged:0,at:140});
    assert.equal(result.order.state,'reconciled');
    assert.deepEqual(capacity(l),[17,20,20],'food consumed; slots reusable');
  }finally{l.close();}
});
test('order-origin integrity check remains fail-closed after SQLite restart',()=>{
  const dir=mkdtempSync(join(tmpdir(),'maya-capacity-origin-')),file=join(dir,'test.sqlite');
  try {
    let {l,s}=setup(file);
    s.createReserved(input());
    alterBundleAndHold(l,'truck',7);
    l.close();
    ({l,s}=setup(file));
    try{
      assert.throws(()=>s.cancel({id:'synthetic-order',actorId:parties.donor,evidenceRef:'fictional',at:150}),/corrupt_order_reservation/);
      assert.deepEqual(capacity(l),[17,17,17]);
      assert.equal(s.get('synthetic-order').state,'reserved');
    }finally{l.close();}
  }finally{rmSync(dir,{recursive:true,force:true});}
});
