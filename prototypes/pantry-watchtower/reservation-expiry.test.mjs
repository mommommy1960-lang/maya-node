import test from "node:test";
import assert from "node:assert/strict";
import {ReservationLedger} from "./reservation-ledger.mjs";
const items=[{resourceId:"food",quantity:4},{resourceId:"freezer",quantity:4},{resourceId:"truck",quantity:1}];
test("bundle expiration restores all three capacities exactly once",()=>{
 const l=new ReservationLedger();
 for(const [id,n] of [["food",10],["freezer",10],["truck",1]])l.seedResource(id,n);
 assert.equal(l.reserveBundle({id:"bundle",items,expiresAt:200},100),true);
 assert.equal(l.expireBundles(199),0);assert.equal(l.expireBundles(201),1);
 assert.equal(l.expireBundles(201),0);assert.equal(l.available("food"),10);
 assert.equal(l.available("freezer"),10);assert.equal(l.available("truck"),1);l.close();
});
test("release of one bundle cannot affect similarly prefixed bundle",()=>{
 const l=new ReservationLedger();l.seedResource("food",10);
 const a={id:"a",items:[{resourceId:"food",quantity:2}],expiresAt:200};
 const ab={id:"ab",items:[{resourceId:"food",quantity:3}],expiresAt:200};
 assert.equal(l.reserveBundle(a,100),true);assert.equal(l.reserveBundle(ab,100),true);
 assert.equal(l.releaseBundle("a"),true);assert.equal(l.available("food"),7);
 assert.equal(l.releaseBundle("ab"),true);assert.equal(l.available("food"),10);l.close();
});
