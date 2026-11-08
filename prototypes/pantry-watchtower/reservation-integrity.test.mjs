/** Synthetic-only regression tests for durable bundle ownership and expiry. */
import test from "node:test";
import assert from "node:assert/strict";
import {mkdtempSync,rmSync} from "node:fs";
import {tmpdir} from "node:os";
import {join} from "node:path";
import {ReservationLedger} from "./reservation-ledger.mjs";

const items=[{resourceId:"food",quantity:5},{resourceId:"freezer",quantity:5},{resourceId:"truck",quantity:1}];
const req=(id,expiresAt=200)=>({id,items,expiresAt});
const seed=l=>{l.seedResource("food",10);l.seedResource("freezer",10);l.seedResource("truck",1);};

test("individual release cannot break an all-or-nothing bundle",()=>{
  const l=new ReservationLedger();try{
    seed(l);assert.equal(l.reserveBundle(req("b"),100),true);
    assert.throws(()=>l.release("b:food"),/bundle_hold_requires_group_release/);
    assert.equal(l.expire(201),0,"ordinary expiry must not split bundle holds");
    assert.equal(l.available("food"),5);
    assert.equal(l.available("freezer"),5);
    assert.equal(l.available("truck"),0);
    assert.equal(l.releaseBundle("b"),true);
    assert.equal(l.available("food"),10);
    assert.equal(l.available("freezer"),10);
    assert.equal(l.available("truck"),1);
  }finally{l.close();}
});

test("bundle expiry is group-atomic, idempotent and refuses stale approval",()=>{
  const l=new ReservationLedger();try{
    seed(l);assert.equal(l.reserveBundle(req("b"),100),true);
    assert.equal(l.isBundleActive("b",199),true);
    assert.equal(l.isBundleActive("b",200),false,"expiry boundary blocks authorization");
    assert.equal(l.expireBundles(200),1);
    assert.equal(l.expireBundles(201),0);
    assert.equal(l.isBundleActive("b",199),false);
    assert.equal(l.reserveBundle(req("b"),100),false,"expired idempotency key must not resurrect");
    assert.deepEqual(["food","freezer","truck"].map(x=>l.available(x)),[10,10,1]);
  }finally{l.close();}
});

test("reopened SQLite file restores expired capacity before a competing claim",()=>{
  const dir=mkdtempSync(join(tmpdir(),"maya-restart-")),file=join(dir,"claims.sqlite");
  try{
    let l=new ReservationLedger(file);seed(l);
    assert.equal(l.reserveBundle(req("old",200),100),true);
    l.close();
    l=new ReservationLedger(file);
    try{
      assert.equal(l.isBundleActive("old",201),false);
      assert.equal(l.reserveBundle(req("new",400),201),true);
      assert.equal(l.isBundleActive("new",202),true);
      assert.equal(l.isBundleActive("old",199),false);
      assert.deepEqual(["food","freezer","truck"].map(x=>l.available(x)),[5,5,0]);
      assert.equal(l.releaseBundle("new"),true);
      assert.deepEqual(["food","freezer","truck"].map(x=>l.available(x)),[10,10,1]);
    }finally{l.close();}
  }finally{rmSync(dir,{recursive:true,force:true});}
});

test("single holds still release and expire normally",()=>{
  const l=new ReservationLedger();try{
    l.seedResource("food",10);
    assert.equal(l.reserve({id:"single",resourceId:"food",quantity:3,expiresAt:200},100),true);
    assert.equal(l.expire(201),1);
    assert.equal(l.expire(201),0);
    assert.equal(l.available("food"),10);
  }finally{l.close();}
});

test("bundle identifier with colon cannot hijack adjacent bundle releases",()=>{
  const l=new ReservationLedger();try{
    l.seedResource("food",12);
    const a={id:"x",items:[{resourceId:"food",quantity:2}],expiresAt:200};
    const b={id:"x:y",items:[{resourceId:"food",quantity:3}],expiresAt:200};
    assert.equal(l.reserveBundle(a,100),true);
    assert.equal(l.reserveBundle(b,100),true);
    assert.equal(l.releaseBundle("x"),true);
    assert.equal(l.available("food"),9);
    assert.equal(l.isBundleActive("x:y",150),true);
    assert.equal(l.releaseBundle("x:y"),true);
    assert.equal(l.available("food"),12);
  }finally{l.close();}
});

test("unmapped pre-migration synthetic bundle fails closed instead of partially releasing",()=>{
  const l=new ReservationLedger();try{
    l.seedResource("food",10);
    const legacyItems=[{resourceId:"food",quantity:2}];
    const signature=JSON.stringify({items:legacyItems,expiresAt:200});
    l.db.prepare("INSERT INTO bundles(id,signature,state) VALUES(?,?,'active')").run("legacy",signature);
    l.db.prepare("INSERT INTO holds(id,resource_id,quantity,state,expires_at) VALUES(?,?,?,'active',?)").run("legacy:food","food",2,200);
    l.db.prepare("UPDATE resources SET available=available-2 WHERE id='food'").run();
    assert.equal(l.expire(201),0,"legacy bundle must not be split by ordinary expiry");
    assert.throws(()=>l.release("legacy:food"),/bundle_hold_requires_group_release/);
    assert.throws(()=>l.reserveBundle({id:"legacy",items:legacyItems,expiresAt:200},100),/legacy_bundle_requires_migration/);
    assert.throws(()=>l.releaseBundle("legacy"),/corrupt_bundle_ownership/);
    assert.equal(l.available("food"),8,"do not guess how to recover legacy durable holds");
  }finally{l.close();}
});
