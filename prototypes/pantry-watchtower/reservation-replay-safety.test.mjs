/** Synthetic-only reservation replay gates. No production data or actual dispatch. */
import test from "node:test";
import assert from "node:assert/strict";
import {mkdtempSync,rmSync} from "node:fs";
import {tmpdir} from "node:os";
import {join} from "node:path";
import {ReservationLedger} from "./reservation-ledger.mjs";
import {SyntheticOrderStore} from "./synthetic-order-store.mjs";

const items=[{resourceId:"food",quantity:4},{resourceId:"freezer",quantity:4},{resourceId:"truck",quantity:1}];
const parties={donor:"fake-donor",receiver:"fake-pantry",transport:"fake-truck"};
const order=()=>({id:"fake-order",offerId:"fake-offer",needId:"fake-need",quantity:4,parties,at:100,
  bundle:{id:"fake-bundle",items,expiresAt:300}});
function setup(file=":memory:"){
  const ledger=new ReservationLedger(file);
  ledger.seedResource("food",10);ledger.seedResource("freezer",10);ledger.seedResource("truck",1);
  return {ledger,orders:new SyntheticOrderStore(ledger)};
}
test("a single-hold replay at expiry never reports capacity",()=>{
  const l=new ReservationLedger();
  try {
    l.seedResource("truck",1);
    const hold={id:"old",resourceId:"truck",quantity:1,expiresAt:200};
    assert.equal(l.reserve(hold,100),true);
    assert.equal(l.reserve(hold,199),true);
    assert.equal(l.reserve(hold,200),false);
    assert.equal(l.available("truck"),0,"no premature reclamation");
    assert.equal(l.expire(200),1);
    assert.equal(l.reserve(hold,100),false,"released idempotency key is terminal");
    assert.equal(l.available("truck"),1);
  }finally{l.close();}
});
test("an order-owned bundle cannot be reconfirmed after expiry, even after restart",()=>{
  const dir=mkdtempSync(join(tmpdir(),"maya-replay-gate-")),file=join(dir,"test.sqlite");
  try {
    let {ledger:l,orders:s}=setup(file);
    s.createReserved(order());
    assert.equal(l.reserveBundle(order().bundle,200),true);
    assert.equal(l.reserveBundle(order().bundle,300),false,"generic sweep must not free order-owned capacity");
    assert.equal(l.available("truck"),0);
    l.close();
    ({ledger:l,orders:s}=setup(file));
    try {
      assert.equal(l.reserveBundle(order().bundle,301),false,"no stale capacity after restart");
      assert.equal(s.expireDue(301),1);
      assert.equal(l.reserveBundle(order().bundle,200),false);
      assert.deepEqual(["food","freezer","truck"].map(x=>l.available(x)),[10,10,1]);
    }finally{l.close();}
  }finally{rmSync(dir,{recursive:true,force:true});}
});
test("picked-up order cannot be reconfirmed as available reservation",()=>{
  const {ledger:l,orders:s}=setup();
  try {
    s.createReserved(order());
    s.approve({id:"fake-order",role:"donor",actorId:parties.donor,evidenceRef:"fake-donor-approval",at:120});
    s.approve({id:"fake-order",role:"receiver",actorId:parties.receiver,evidenceRef:"fake-pantry-approval",at:121});
    s.approve({id:"fake-order",role:"transport",actorId:parties.transport,evidenceRef:"fake-truck-approval",at:122});
    s.pickup({id:"fake-order",actorId:parties.transport,evidenceRef:"fake-manifest",at:150});
    assert.equal(l.reserveBundle(order().bundle,200),false);
    assert.deepEqual(["food","freezer","truck"].map(x=>l.available(x)),[6,6,0]);
  }finally{l.close();}
});
test("corrupted missing bundle-hold mapping rejects replay without restoring resources",()=>{
  const l=new ReservationLedger();
  try {
    l.seedResource("food",10);l.seedResource("truck",1);
    const bundle={id:"broken",items:[{resourceId:"food",quantity:3},{resourceId:"truck",quantity:1}],expiresAt:300};
    assert.equal(l.reserveBundle(bundle,100),true);
    l.db.prepare("DELETE FROM bundle_holds WHERE bundle_id=? AND resource_id=?").run("broken","truck");
    assert.throws(()=>l.reserveBundle(bundle,150),/corrupt_bundle_ownership/);
    assert.equal(l.available("truck"),0);
    assert.equal(l.available("food"),7);
  }finally{l.close();}
});
test("cancelled order cannot be re-presented as fresh reserved order",()=>{
  const {ledger:l,orders:s}=setup();
  try {
    s.createReserved(order());
    s.cancel({id:"fake-order",actorId:parties.donor,evidenceRef:"fake-cancel",at:150});
    assert.throws(()=>s.createReserved(order(),200),/inactive_order_idempotency_replay/);
    assert.deepEqual(["food","freezer","truck"].map(x=>l.available(x)),[10,10,1]);
  }finally{l.close();}
});
test("malformed synthetic clocks cannot bypass expiry validation",()=>{
  const l=new ReservationLedger();
  try {
    l.seedResource("food",10);
    const hold={id:"h",resourceId:"food",quantity:1,expiresAt:300};
    const bundle={id:"b",items:[{resourceId:"food",quantity:1}],expiresAt:300};
    for (const now of [-1,NaN,Infinity,100.5]) {
      assert.throws(()=>l.reserve(hold,now),/invalid_hold/);
      assert.throws(()=>l.reserveBundle(bundle,now),/invalid_bundle/);
    }
    assert.equal(l.available("food"),10);
  }finally{l.close();}
});
