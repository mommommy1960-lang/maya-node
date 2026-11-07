import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { ReservationLedger } from "./reservation-ledger.mjs";
test("competing claims cannot overbook the same resource",()=>{
 const l=new ReservationLedger();l.seedResource("truck",1);
 assert.equal(l.reserve({id:"one",resourceId:"truck",quantity:1,expiresAt:200},100),true);
 assert.equal(l.reserve({id:"two",resourceId:"truck",quantity:1,expiresAt:200},100),false);
 assert.equal(l.available("truck"),0);l.close();
});
test("retry is idempotent; conflicting retry rejected",()=>{
 const l=new ReservationLedger();l.seedResource("freezer",10);
 const h={id:"h",resourceId:"freezer",quantity:4,expiresAt:200};
 assert.equal(l.reserve(h,100),true);assert.equal(l.reserve(h,100),true);
 assert.equal(l.available("freezer"),6);
 assert.throws(()=>l.reserve({...h,quantity:5},100),/idempotency_conflict/);l.close();
});
test("release and expiry restore capacity once",()=>{
 const l=new ReservationLedger();l.seedResource("lot",8);
 l.reserve({id:"a",resourceId:"lot",quantity:5,expiresAt:200},100);
 assert.equal(l.expire(201),1);assert.equal(l.expire(201),0);
 assert.equal(l.release("a"),false);assert.equal(l.available("lot"),8);l.close();
});
test("hold persists across database restart",()=>{
 const dir=mkdtempSync(join(tmpdir(),"maya-reservation-")),file=join(dir,"ledger.sqlite");
 try{
 let l=new ReservationLedger(file);l.seedResource("truck",1);
 assert.equal(l.reserve({id:"one",resourceId:"truck",quantity:1,expiresAt:200},100),true);l.close();
 l=new ReservationLedger(file);assert.equal(l.available("truck"),0);
 assert.equal(l.reserve({id:"two",resourceId:"truck",quantity:1,expiresAt:200},100),false);
 l.close();
 }finally{rmSync(dir,{recursive:true,force:true});}
});
