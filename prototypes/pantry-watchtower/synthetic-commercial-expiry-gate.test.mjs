/** Safety regression: a signed-up fictional order cannot quote or mock-charge after expiry. */
import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {ReservationLedger} from './reservation-ledger.mjs';
import {SyntheticOrderStore} from './synthetic-order-store.mjs';
import {SyntheticCommercialRehearsal} from './synthetic-commercial-rehearsal.mjs';

const ID='SYN-EXPIRE-COMMERCIAL', END=2000, TERMS='SYN-TERMS-2026-11-07-v1';
function setup(filename=':memory:') {
  const ledger=new ReservationLedger(filename);
  for (const name of ['food','cold','truck']) ledger.seedResource(name,10);
  const orders=new SyntheticOrderStore(ledger);
  const commercial=new SyntheticCommercialRehearsal(orders);
  return {ledger,orders,commercial,close:()=>ledger.close()};
}
function reserve(app) {
  app.orders.createReserved({id:ID,offerId:'SYN-OFFER',needId:'SYN-NEED',
    quantity:2,parties:{donor:'donor-x',receiver:'receiver-x',transport:'truck-x'},
    bundle:{id:'SYN-BUNDLE-EXPIRE',expiresAt:END,
      items:['food','cold','truck'].map(resourceId=>({resourceId,quantity:2}))},
    at:1000});
  for (const [role,actorId] of [['donor','donor-x'],['receiver','receiver-x'],['transport','truck-x']]) {
    app.orders.approve({id:ID,role,actorId,evidenceRef:'SYN-'+role,at:1100});
  }
}
const quote=(app,at)=>app.commercial.quote({orderId:ID,at});
const accept=(app,at)=>app.commercial.accept({orderId:ID,actorId:'fictional-sponsor',termsVersion:TERMS,at});
const authorize=(app,at)=>app.commercial.authorize({orderId:ID,actorId:'fictional-sponsor',attemptId:'SYN-AUTH-expired-test',mode:'approve',at});

test('quote exactly at expiry is rejected with no phantom quote or debit',()=>{
  const app=setup();
  try {
    reserve(app);
    assert.throws(()=>quote(app,END),/reservation_expired/);
    assert.equal(app.commercial.get(ID),null);
    assert.equal(app.ledger.available('food'),8);
    assert.equal(app.orders.get(ID).state,'approved');
    assert.equal(app.orders.expireDue(END),1);
    assert.equal(app.ledger.available('food'),10);
  } finally {app.close();}
});
test('fictional terms acceptance cannot happen after expiry even before sweeper',()=>{
  const app=setup();
  try {
    reserve(app);
    quote(app,1200);
    assert.throws(()=>accept(app,END+1),/reservation_expired/);
    assert.equal(app.commercial.get(ID).state,'quoted');
    assert.deepEqual(app.commercial.get(ID).events.map(x=>x.kind),['quote_prepared']);
    assert.equal(app.orders.expireDue(END+2),1);
    assert.equal(app.commercial.get(ID).state,'voided');
  } finally {app.close();}
});
test('mock authorization and repeat attempts fail closed after expiry and survive restart',()=>{
  const dir=mkdtempSync(join(tmpdir(),'maya-expiry-finance-'));
  const file=join(dir,'isolated.sqlite');
  try {
    const a=setup(file);
    try {reserve(a);quote(a,1200);accept(a,1300);} finally {a.close();}
    const b=setup(file);
    try {
      assert.throws(()=>authorize(b,END),/reservation_expired/);
      assert.throws(()=>authorize(b,END+1),/reservation_expired/);
      assert.equal(b.commercial.get(ID).state,'accepted');
      assert.equal(b.commercial.get(ID).events.length,2);
      assert.equal(b.orders.expireDue(END+2),1);
      assert.equal(b.commercial.get(ID).state,'voided');
      assert.equal(b.ledger.available('truck'),10);
    } finally {b.close();}
  } finally {rmSync(dir,{recursive:true,force:true});}
});
test('corrupt reservation capacity is not valid payment authorization even before expiry',()=>{
  const app=setup();
  try {
    reserve(app);quote(app,1200);accept(app,1300);
    // Isolated synthetic fault injection; never touch hosted data.
    app.ledger.db.prepare("UPDATE holds SET state='released' WHERE resource_id='truck'").run();
    assert.throws(()=>authorize(app,1400),/corrupt_order_reservation/);
    assert.equal(app.commercial.get(ID).state,'accepted');
  } finally {app.close();}
});
