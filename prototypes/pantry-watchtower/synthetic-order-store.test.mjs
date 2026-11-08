/** All records, identities, approval references and times are fictional. */
import test from "node:test";
import assert from "node:assert/strict";
import {mkdtempSync,rmSync} from "node:fs";
import {tmpdir} from "node:os";
import {join} from "node:path";
import {ReservationLedger} from "./reservation-ledger.mjs";
import {SyntheticOrderStore} from "./synthetic-order-store.mjs";

const participants={donor:"fictional-donor",receiver:"fictional-pantry",transport:"fictional-driver"};
function setup(filename=":memory:"){
  const l=new ReservationLedger(filename);
  l.seedResource("food",10);l.seedResource("freezer",10);l.seedResource("truck",1);
  return {l,s:new SyntheticOrderStore(l)};
}
const input=(id="fictional-order",expiresAt=300)=>({
  id,offerId:"fictional-offer",needId:"fictional-need",quantity:5,parties:participants,at:100,
  bundle:{id:"bundle-"+id,items:[{resourceId:"food",quantity:5},{resourceId:"freezer",quantity:5},{resourceId:"truck",quantity:1}],expiresAt}
});
const approve=(s,id="fictional-order",start=120)=>{
  s.approve({id,role:"donor",actorId:participants.donor,evidenceRef:"donor-consent",at:start});
  s.approve({id,role:"receiver",actorId:participants.receiver,evidenceRef:"receiver-consent",at:start+1});
  return s.approve({id,role:"transport",actorId:participants.transport,evidenceRef:"driver-confirm",at:start+2});
};
test("new order and all three capacity debits persist atomically",()=>{
  const {l,s}=setup();try{
    const o=s.createReserved(input());assert.equal(o.state,"reserved");assert.deepEqual([l.available("food"),l.available("freezer"),l.available("truck")],[5,5,0]);
    assert.deepEqual(o.events.map(x=>x.kind),["proposed","reserved"]);
    assert.equal(o.synthetic,true);assert.equal(o.paymentEnabled,false);assert.equal(o.dispatchEnabled,false);
  }finally{l.close();}
});
test("missing vehicle cannot leave partial order or debit capacity",()=>{
  const {l,s}=setup();try{
    l.reserve({id:"truck-alone",resourceId:"truck",quantity:1,expiresAt:500},100);
    assert.throws(()=>s.createReserved(input()),/insufficient_capacity/);
    assert.equal(s.get("fictional-order"),null);
    assert.equal(l.available("food"),10);assert.equal(l.available("freezer"),10);
  }finally{l.close();}
});
test("idempotent exact retry does not create duplicate orders or holds",()=>{
  const {l,s}=setup();try{
    s.createReserved(input());const o=s.createReserved(input());
    assert.equal(o.events.length,2);assert.deepEqual([l.available("food"),l.available("truck")],[5,0]);
    assert.throws(()=>s.createReserved({...input(),quantity:7}),/order_idempotency_conflict/);
  }finally{l.close();}
});
test("all three named human roles must approve, unapproved pickup fails",()=>{
  const {l,s}=setup();try{
    s.createReserved(input());
    assert.throws(()=>s.approve({id:"fictional-order",role:"donor",actorId:"other",evidenceRef:"x",at:110}),/unauthorized_party/);
    assert.throws(()=>s.pickup({id:"fictional-order",actorId:participants.transport,evidenceRef:"manifest",at:111}),/pickup_requires_approvals/);
    assert.equal(approve(s).state,"approved");
    assert.equal(s.get("fictional-order").approvals.length,3);
    const picked=s.pickup({id:"fictional-order",actorId:participants.transport,evidenceRef:"manifest",at:150});
    assert.equal(picked.state,"picked_up");assert.equal(picked.events.at(-1).kind,"picked_up");
    assert.equal(l.expireBundles(1000),0,"in-transit hold cannot be reclaimed by ordinary expiry");
  }finally{l.close();}
});
test("conflicting duplicate approval is rejected without a duplicate event",()=>{
  const {l,s}=setup();try{
    s.createReserved(input());
    const a={id:"fictional-order",role:"donor",actorId:participants.donor,evidenceRef:"consent1",at:110};
    s.approve(a);s.approve({...a,at:111});
    assert.equal(s.get(a.id).approvals.length,1);
    assert.throws(()=>s.approve({...a,evidenceRef:"changed",at:112}),/approval_replay_conflict/);
    assert.equal(s.get(a.id).events.length,3);
  }finally{l.close();}
});
test("expiry boundary fails closed, sweeper releases all resources once",()=>{
  const {l,s}=setup();try{
    s.createReserved(input());
    assert.throws(()=>s.approve({id:"fictional-order",role:"donor",actorId:participants.donor,evidenceRef:"late",at:300}),/reservation_expired/);
    assert.equal(s.expireDue(300),1);assert.equal(s.expireDue(301),0);
    assert.equal(s.get("fictional-order").state,"expired");
    assert.deepEqual([l.available("food"),l.available("freezer"),l.available("truck")],[10,10,1]);
  }finally{l.close();}
});
test("pre-pickup cancellation is atomic, terminal, repeat-safe",()=>{
  const {l,s}=setup();try{
    s.createReserved(input());approve(s);
    assert.throws(()=>s.cancel({id:"fictional-order",actorId:"stranger",evidenceRef:"x",at:150}),/unauthorized_party/);
    s.cancel({id:"fictional-order",actorId:participants.receiver,evidenceRef:"changed-plans",at:150});
    assert.deepEqual([l.available("food"),l.available("freezer"),l.available("truck")],[10,10,1]);
    assert.throws(()=>s.cancel({id:"fictional-order",actorId:participants.receiver,evidenceRef:"again",at:151}),/cancellation_requires_pre_pickup/);
    assert.throws(()=>s.pickup({id:"fictional-order",actorId:participants.transport,evidenceRef:"late",at:152}),/pickup_requires_approvals/);
  }finally{l.close();}
});
test("file restart retains order, approvals and stops expired stale pickup",()=>{
  const dir=mkdtempSync(join(tmpdir(),"maya-order-")),file=join(dir,"state.sqlite");
  try{
    let {l,s}=setup(file);s.createReserved(input());s.approve({id:"fictional-order",role:"donor",actorId:participants.donor,evidenceRef:"yes",at:110});l.close();
    ({l,s}=setup(file));
    try{
      assert.equal(s.get("fictional-order").approvals.length,1);
      assert.equal(s.expireDue(350),1);
      assert.equal(s.get("fictional-order").state,"expired");
      assert.deepEqual([l.available("food"),l.available("freezer"),l.available("truck")],[10,10,1]);
    }finally{l.close();}
  }finally{rmSync(dir,{recursive:true,force:true});}
});
test("append-only order events reject silent rewrite and deletion",()=>{
  const {l,s}=setup();try{
    s.createReserved(input());
    assert.throws(()=>l.db.exec("DELETE FROM synthetic_order_events"),/append_only_events/);
    assert.throws(()=>l.db.exec("UPDATE synthetic_order_events SET kind='approved'"),/append_only_events/);
  }finally{l.close();}
});
test("backdated and post-pickup cancellation are refused",()=>{
  const {l,s}=setup();try{
    s.createReserved(input());approve(s);
    assert.throws(()=>s.pickup({id:"fictional-order",actorId:participants.transport,evidenceRef:"early",at:101}),/out_of_order_event/);
    s.pickup({id:"fictional-order",actorId:participants.transport,evidenceRef:"signed-pickup",at:150});
    assert.throws(()=>s.cancel({id:"fictional-order",actorId:participants.donor,evidenceRef:"late",at:151}),/cancellation_requires_pre_pickup/);
  }finally{l.close();}
});
