import test from "node:test";
import assert from "node:assert/strict";
import {ReservationLedger} from "./reservation-ledger.mjs";
const items=[{resourceId:"food",quantity:5},{resourceId:"freezer",quantity:5},{resourceId:"truck",quantity:1}];
test("food, freezer and truck commit together",()=>{
 const l=new ReservationLedger();l.seedResource("food",10);l.seedResource("freezer",10);l.seedResource("truck",1);
 assert.equal(l.reserveBundle({id:"transfer",items,expiresAt:200},100),true);
 assert.equal(l.available("food"),5);assert.equal(l.available("freezer"),5);assert.equal(l.available("truck"),0);l.close();
});
test("truck contention rolls back food and freezer debits",()=>{
 const l=new ReservationLedger();l.seedResource("food",10);l.seedResource("freezer",10);l.seedResource("truck",0);
 assert.equal(l.reserveBundle({id:"transfer",items,expiresAt:200},100),false);
 assert.equal(l.available("food"),10);assert.equal(l.available("freezer"),10);assert.equal(l.available("truck"),0);l.close();
});
test("bundle idempotency and release restore exactly once",()=>{
 const l=new ReservationLedger();l.seedResource("food",10);l.seedResource("freezer",10);l.seedResource("truck",1);
 const req={id:"transfer",items,expiresAt:200};
 assert.equal(l.reserveBundle(req,100),true);assert.equal(l.reserveBundle(req,100),true);
 assert.equal(l.releaseBundle("transfer"),true);assert.equal(l.releaseBundle("transfer"),false);
 assert.equal(l.available("food"),10);assert.equal(l.available("freezer"),10);assert.equal(l.available("truck"),1);l.close();
});
