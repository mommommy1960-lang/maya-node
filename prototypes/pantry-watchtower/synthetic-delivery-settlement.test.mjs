/** Fictional-only delivery settlement regression tests; no external actions or payments. */
import test from "node:test";
import assert from "node:assert/strict";
import {mkdtempSync,rmSync} from "node:fs";
import {tmpdir} from "node:os";
import {join} from "node:path";
import {ReservationLedger} from "./reservation-ledger.mjs";
import {SyntheticOrderStore} from "./synthetic-order-store.mjs";
import {SyntheticDeliverySettlement} from "./synthetic-delivery-settlement.mjs";

const parties={donor:"demo-donor",receiver:"demo-receiver",transport:"demo-carrier"};
function make(filename=":memory:"){
  const l=new ReservationLedger(filename);
  for(const [id,capacity] of [["food",10],["freezer",10],["truck",1]])l.seedResource(id,capacity);
  const s=new SyntheticOrderStore(l),d=new SyntheticDeliverySettlement(s);
  return {l,s,d};
}
function input(id="order-1"){return {id,offerId:"demo-offer",needId:"demo-need",quantity:5,parties,
  at:100,bundle:{id:"bundle-"+id,items:[{resourceId:"food",quantity:5},{resourceId:"freezer",quantity:5},
    {resourceId:"truck",quantity:1}],expiresAt:300}};}
function prepare(s){
  s.createReserved(input());
  s.approve({id:"order-1",role:"donor",actorId:parties.donor,evidenceRef:"donor-yes",at:120});
  s.approve({id:"order-1",role:"receiver",actorId:parties.receiver,evidenceRef:"receiver-yes",at:121});
  s.approve({id:"order-1",role:"transport",actorId:parties.transport,evidenceRef:"carrier-yes",at:122});
  s.pickup({id:"order-1",actorId:parties.transport,evidenceRef:"pickup-proof",at:150});
}
function receipt(changes={}){return {id:"order-1",receiptId:"receipt-1",actorId:parties.receiver,
  evidenceRef:"receiver-counted",foodResourceId:"food",received:5,rejected:0,damaged:0,at:160,...changes};}
test("complete fictional delivery is reconciled atomically, food consumed, truck/storage returned",()=>{
  const {l,s,d}=make();try{
    prepare(s);
    const result=d.recordReceipt(receipt());
    assert.equal(result.order.state,"reconciled");assert.equal(result.receipt.discrepancy,false);
    assert.deepEqual([l.available("food"),l.available("freezer"),l.available("truck")],[5,10,1]);
    assert.deepEqual(l.db.prepare("SELECT resource_id,state FROM holds ORDER BY resource_id").all().map(x=>[x.resource_id,x.state]),
      [["food","consumed"],["freezer","released"],["truck","released"]]);
    assert.deepEqual(result.order.events.slice(-2).map(x=>x.kind),["delivered","reconciled"]);
    assert.equal(l.releaseBundle("bundle-order-1"),false);
    assert.equal(l.expireBundles(999),0);
  }finally{l.close();}
});
test("partial delivery records shortage without returning missing food to available inventory",()=>{
  const {l,s,d}=make();try{
    prepare(s);
    const result=d.recordReceipt(receipt({received:3}));
    assert.equal(result.order.state,"exception");
    assert.equal(result.receipt.missing,2);
    assert.equal(result.receipt.discrepancy,true);
    assert.deepEqual([l.available("food"),l.available("freezer"),l.available("truck")],[5,10,1]);
    assert.throws(()=>d.recordDisposition({id:"order-1",actorId:"stranger",evidenceRef:"x",resolutionCode:"shortage_recorded",explanation:"demo discrepancy",at:165}),/unauthorized_receiver/);
    const corrected=d.recordDisposition({id:"order-1",actorId:parties.receiver,evidenceRef:"documented-shortage",
      resolutionCode:"shortage_recorded",explanation:"Fictional two units remain unaccounted for",at:165});
    assert.equal(corrected.order.state,"reconciled");
    assert.equal(corrected.receipt.missing,2);
    assert.equal(corrected.receipt.disposition.code,"shortage_recorded");
    assert.equal(l.available("food"),5);
    assert.throws(()=>d.recordDisposition({id:"order-1",actorId:parties.receiver,evidenceRef:"twice",
      resolutionCode:"shortage_recorded",explanation:"repeat",at:166}),/disposition_requires_exception/);
  }finally{l.close();}
});
test("damaged or rejected receipts cannot silently count as fully delivered",()=>{
  const {l,s,d}=make();try{
    prepare(s);const x=d.recordReceipt(receipt({received:3,rejected:1,damaged:1}));
    assert.equal(x.order.state,"exception");
    assert.deepEqual([x.receipt.received,x.receipt.rejected,x.receipt.damaged,x.receipt.missing],[3,1,1,0]);
    assert.equal(l.available("food"),5);
  }finally{l.close();}
});
test("exact retry is idempotent; different quantities or evidence are refused",()=>{
  const {l,s,d}=make();try{
    prepare(s);
    const result=d.recordReceipt(receipt());
    const second=d.recordReceipt(receipt());
    assert.equal(second.order.events.length,result.order.events.length);
    assert.equal(l.available("truck"),1);
    assert.throws(()=>d.recordReceipt(receipt({evidenceRef:"new-evidence"})),/receipt_replay_conflict/);
    assert.throws(()=>d.recordReceipt(receipt({received:4})),/receipt_replay_conflict/);
    assert.equal(l.db.prepare("SELECT COUNT(*) AS n FROM synthetic_delivery_receipts").get().n,1);
  }finally{l.close();}
});
test("unauthorized receiver and forged food resource cannot settle a trip",()=>{
  const {l,s,d}=make();try{
    prepare(s);
    assert.throws(()=>d.recordReceipt(receipt({actorId:"other"})),/unauthorized_receiver/);
    assert.throws(()=>d.recordReceipt(receipt({foodResourceId:"truck"})),/invalid_food_allocation/);
    assert.equal(d.getReceipt("order-1"),null);
    assert.equal(s.get("order-1").state,"picked_up");
    assert.deepEqual([l.available("food"),l.available("freezer"),l.available("truck")],[5,5,0]);
  }finally{l.close();}
});
test("over-received, negative and noninteger quantities fail without side effects",()=>{
  const {l,s,d}=make();try{
    prepare(s);
    assert.throws(()=>d.recordReceipt(receipt({received:6})),/receipt_quantity_exceeds_order/);
    assert.throws(()=>d.recordReceipt(receipt({received:-1})),/invalid_delivery_receipt/);
    assert.throws(()=>d.recordReceipt(receipt({received:2.5})),/invalid_delivery_receipt/);
    assert.equal(d.getReceipt("order-1"),null);
    assert.equal(l.available("truck"),0);
  }finally{l.close();}
});
test("pickup and chronological evidence required, canceled orders cannot be delivered",()=>{
  const {l,s,d}=make();try{
    s.createReserved(input());
    assert.throws(()=>d.recordReceipt(receipt()),/delivery_requires_pickup/);
    s.cancel({id:"order-1",actorId:parties.donor,evidenceRef:"cancel",at:130});
    assert.throws(()=>d.recordReceipt(receipt()),/delivery_requires_pickup/);
    assert.equal(l.available("food"),10);
  }finally{l.close();}
});
test("backdated delivery fails and leaves live reservation intact",()=>{
  const {l,s,d}=make();try{
    prepare(s);
    assert.throws(()=>d.recordReceipt(receipt({at:149})),/out_of_order_event/);
    assert.equal(l.available("truck"),0);
    assert.equal(s.get("order-1").state,"picked_up");
  }finally{l.close();}
});
test("receipt, dispositions and events reject silent modification or deletion",()=>{
  const {l,s,d}=make();try{
    prepare(s);d.recordReceipt(receipt({received:4}));
    d.recordDisposition({id:"order-1",actorId:parties.receiver,evidenceRef:"reviewed",
      resolutionCode:"exception_documented",explanation:"Documented shortage",at:165});
    assert.throws(()=>l.db.exec("DELETE FROM synthetic_delivery_receipts"),/append_only_receipts/);
    assert.throws(()=>l.db.exec("UPDATE synthetic_delivery_receipts SET received=5"),/append_only_receipts/);
    assert.throws(()=>l.db.exec("DELETE FROM synthetic_receipt_dispositions"),/append_only_dispositions/);
    assert.throws(()=>l.db.exec("UPDATE synthetic_receipt_dispositions SET resolution_code='changed'"),/append_only_dispositions/);
  }finally{l.close();}
});
test("failed hold update rolls back receipt, order state and restored capacity together",()=>{
  const {l,s,d}=make();try{
    prepare(s);
    l.db.exec(`CREATE TRIGGER simulate_failed_hold_settlement
      BEFORE UPDATE ON holds WHEN NEW.state='released'
      BEGIN SELECT RAISE(ABORT,'simulated_resource_failure'); END;`);
    assert.throws(()=>d.recordReceipt(receipt()),/simulated_resource_failure/);
    assert.equal(d.getReceipt("order-1"),null);
    assert.equal(s.get("order-1").state,"picked_up");
    assert.deepEqual([l.available("food"),l.available("freezer"),l.available("truck")],[5,5,0]);
  }finally{l.close();}
});
test("restart preserves receipt, exception and correction without restoring consumed food",()=>{
  const dir=mkdtempSync(join(tmpdir(),"maya-receipt-")),file=join(dir,"state.sqlite");
  try{
    let {l,s,d}=make(file);prepare(s);d.recordReceipt(receipt({received:4}));l.close();
    ({l,s,d}=make(file));
    try{
      assert.equal(s.get("order-1").state,"exception");assert.equal(d.getReceipt("order-1").missing,1);
      d.recordDisposition({id:"order-1",actorId:parties.receiver,evidenceRef:"recount",
        resolutionCode:"shortage_recorded",explanation:"Unaccounted fictional unit",at:170});
      assert.equal(s.get("order-1").state,"reconciled");
      assert.deepEqual([l.available("food"),l.available("freezer"),l.available("truck")],[5,10,1]);
      assert.equal(l.expireBundles(999),0);
    }finally{l.close();}
  }finally{rmSync(dir,{recursive:true,force:true});}
});
test("generic bundle release and expiry cannot bypass order transitions before or during pickup",()=>{
  const {l,s}=make();try{
    s.createReserved(input());
    assert.throws(()=>l.releaseBundle("bundle-order-1"),/order_bundle_requires_order_lifecycle/);
    assert.equal(l.expireBundles(350),0);
    assert.equal(s.get("order-1").state,"reserved");
    assert.equal(s.expireDue(350),1);
    assert.equal(s.get("order-1").state,"expired");
    assert.deepEqual([l.available("food"),l.available("freezer"),l.available("truck")],[10,10,1]);
  }finally{l.close();}
});
test("generic release blocked during trip even after original expiry time",()=>{
  const {l,s}=make();try{
    prepare(s);
    assert.throws(()=>l.releaseBundle("bundle-order-1"),/order_bundle_requires_order_lifecycle/);
    assert.equal(l.expireBundles(500),0);
    assert.equal(s.get("order-1").state,"picked_up");
    assert.deepEqual([l.available("food"),l.available("freezer"),l.available("truck")],[5,5,0]);
  }finally{l.close();}
});
