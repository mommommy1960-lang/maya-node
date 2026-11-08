/** Synthetic-only regression: durable bundle mapping must never mint/release wrong capacity. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { ReservationLedger } from './reservation-ledger.mjs';
import { SyntheticOrderStore } from './synthetic-order-store.mjs';

const items=['food','cold','truck'].map(resourceId=>({resourceId,quantity:3}));
const bundle=id=>({id,items,expiresAt:200});
function ledger() {
  const db=new ReservationLedger();
  for(const id of ['food','cold','truck'])db.seedResource(id,15);
  return db;
}
const capacity=l=>['food','cold','truck'].map(id=>l.available(id));

test('a different active hold cannot be substituted into a bundle for release or approval',()=>{
  const l=ledger();
  try{
    assert.equal(l.reserveBundle(bundle('a'),100),true);
    assert.equal(l.reserve({id:'rogue-food',resourceId:'food',quantity:3,expiresAt:200},100),true);
    const before=capacity(l);
    l.db.prepare("UPDATE bundle_holds SET hold_id='rogue-food' WHERE bundle_id='a' AND resource_id='food'").run();
    assert.equal(l.isBundleActive('a',150),false);
    assert.throws(()=>l.releaseBundle('a'),/corrupt_bundle_ownership/);
    assert.throws(()=>l.reserveBundle(bundle('a'),150),/corrupt_bundle_ownership/);
    assert.deepEqual(capacity(l),before,'failure must roll back any resource credits');
    assert.equal(l.db.prepare("SELECT state FROM holds WHERE id='a:food'").get().state,'active');
    assert.equal(l.db.prepare("SELECT state FROM holds WHERE id='rogue-food'").get().state,'active');
  }finally{l.close();}
});

test('deleted mapped hold fails closed and does not partially replenish resources',()=>{
  const l=ledger();
  try{
    assert.equal(l.reserveBundle(bundle('a'),100),true);
    l.db.prepare("DELETE FROM bundle_holds WHERE bundle_id='a' AND resource_id='truck'").run();
    const before=capacity(l);
    assert.equal(l.isBundleActive('a',150),false);
    assert.throws(()=>l.releaseBundle('a'),/corrupt_bundle_ownership/);
    assert.deepEqual(capacity(l),before);
  }finally{l.close();}
});

test('changed quantity or expiry fails both group release and approval without credits',()=>{
  for(const changed of [
    "UPDATE holds SET quantity=2 WHERE id='a:truck'",
    "UPDATE holds SET expires_at=300 WHERE id='a:truck'"
  ]){
    const l=ledger();
    try{
      assert.equal(l.reserveBundle(bundle('a'),100),true);
      l.db.exec(changed);
      const before=capacity(l);
      assert.equal(l.isBundleActive('a',150),false);
      assert.throws(()=>l.releaseBundle('a'),/corrupt_bundle_ownership/);
      assert.deepEqual(capacity(l),before);
    }finally{l.close();}
  }
});

test('malformed signature fails closed instead of making a quantity-only release',()=>{
  const l=ledger();
  try{
    l.reserveBundle(bundle('a'),100);
    l.db.prepare("UPDATE bundles SET signature='not-json' WHERE id='a'").run();
    const before=capacity(l);
    assert.equal(l.isBundleActive('a',150),false);
    assert.throws(()=>l.releaseBundle('a'),/corrupt_bundle_ownership/);
    assert.deepEqual(capacity(l),before);
  }finally{l.close();}
});

test('order approval refuses swapped hold identity even when quantity, resource and expiry match',()=>{
  const l=ledger();
  try {
    const orders=new SyntheticOrderStore(l);
    const parties={donor:'donor-a',receiver:'receiver-a',transport:'transport-a'};
    orders.createReserved({id:'order-a',offerId:'offer-a',needId:'need-a',quantity:3,parties,
      bundle:bundle('owned-a'),at:100});
    l.reserve({id:'rogue-food',resourceId:'food',quantity:3,expiresAt:200},100);
    l.db.prepare("UPDATE bundle_holds SET hold_id='rogue-food' WHERE bundle_id='owned-a' AND resource_id='food'").run();
    assert.throws(()=>orders.approve({id:'order-a',role:'donor',actorId:'donor-a',evidenceRef:'synthetic-evidence',at:120}),/corrupt_order_reservation/);
    assert.equal(orders.get('order-a').state,'reserved');
    assert.equal(orders.get('order-a').approvals.length,0);
  }finally{l.close();}
});

test('normal mapping accepts valid retries but not a picked-up order with extended leases',()=>{
  const l=ledger();
  try{
    const orders=new SyntheticOrderStore(l);
    const parties={donor:'donor-a',receiver:'receiver-a',transport:'transport-a'};
    orders.createReserved({id:'order-a',offerId:'offer-a',needId:'need-a',quantity:3,parties,
      bundle:bundle('owned-a'),at:100});
    assert.equal(l.isBundleActive('owned-a',110),true);
    for(const [role,actorId] of Object.entries(parties))
      orders.approve({id:'order-a',role,actorId,evidenceRef:'synthetic-'+role,at:120});
    assert.equal(l.isBundleActive('owned-a',121),true);
    orders.pickup({id:'order-a',actorId:'transport-a',evidenceRef:'synthetic-pickup',at:130});
    assert.equal(l.isBundleActive('owned-a',131),false,'in-transit hold is not fresh reservable capacity');
    assert.equal(l.reserveBundle(bundle('owned-a'),131),false,'stale key remains rejected');
  }finally{l.close();}
});
