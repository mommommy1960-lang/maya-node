import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { ReservationLedger } from './reservation-ledger.mjs';
import { SyntheticOrderStore } from './synthetic-order-store.mjs';
import { SyntheticDeliverySettlement } from './synthetic-delivery-settlement.mjs';
import { SyntheticCommercialRehearsal } from './synthetic-commercial-rehearsal.mjs';

const ID='SYN-O', SPONSOR='fictional-sponsor', TERMS='SYN-TERMS-2026-11-07-v1';
function create(filename=':memory:') {
  const ledger=new ReservationLedger(filename);
  for(const r of ['food','cold','truck']) ledger.seedResource(r,12);
  const orders=new SyntheticOrderStore(ledger);
  const delivery=new SyntheticDeliverySettlement(orders);
  const finance=new SyntheticCommercialRehearsal(orders);
  return {ledger,orders,delivery,finance,close:()=>ledger.close()};
}
function reserve(app) {
  app.orders.createReserved({id:ID,offerId:'offer',needId:'need',quantity:8,
    parties:{donor:'d',receiver:'r',transport:'t'},
    bundle:{id:'bundle',expiresAt:999_999,items:['food','cold','truck'].map(resourceId=>({resourceId,quantity:8}))},
    at:1000});
}
function approve(app) { for(const [role,actorId] of [['donor','d'],['receiver','r'],['transport','t']])
  app.orders.approve({id:ID,role,actorId,evidenceRef:'SYN-'+role,at:1010}); }
function quoteAndAgree(app) {
  app.finance.quote({orderId:ID,at:1020});
  app.finance.accept({orderId:ID,actorId:SPONSOR,termsVersion:TERMS,at:1030});
}
function authorize(app,mode='approve',attemptId='SYN-AUTH-1',at=1040) {
  return app.finance.authorize({orderId:ID,actorId:SPONSOR,mode,attemptId,at});
}
function delivered(app) {
  app.orders.pickup({id:ID,actorId:'t',evidenceRef:'SYN-pickup',at:1050});
  app.delivery.recordReceipt({id:ID,receiptId:'receipt',actorId:'r',evidenceRef:'SYN-receipt',
    foodResourceId:'food',received:8,rejected:0,damaged:0,at:1060});
}
test('fictional quote declares sponsor-only $2.50 fee, zero receiver cost and no provider',()=>{
  const app=create();
  try {
    reserve(app);
    assert.throws(()=>app.finance.quote({orderId:ID,at:1005}),/quote_requires_fictional_approvals/);
    approve(app);
    const q=app.finance.quote({orderId:ID,at:1020});
    assert.equal(q.sponsorFeeCents,250);
    assert.equal(q.receiverFeeCents,0);
    assert.equal(q.currency,'USD');
    assert.equal(q.provider,'LOCAL_SIMULATOR_ONLY_NOT_STRIPE');
    assert.equal(q.state,'quoted');
    assert.equal(app.finance.quote({orderId:ID,at:1020}).events.length,1);
  } finally { app.close(); }
});
test('terms are versioned, agreement cannot be impersonated and authorize requires agreement',()=>{
  const app=create();
  try{
    reserve(app);approve(app);app.finance.quote({orderId:ID,at:1020});
    assert.throws(()=>authorize(app),/authorization_requires_fictional_agreement/);
    assert.throws(()=>app.finance.accept({orderId:ID,actorId:'receiver',termsVersion:TERMS,at:1030}),/fictional_agreement_mismatch/);
    assert.throws(()=>app.finance.accept({orderId:ID,actorId:SPONSOR,termsVersion:'SYN-OLD',at:1030}),/fictional_agreement_mismatch/);
    app.finance.accept({orderId:ID,actorId:SPONSOR,termsVersion:TERMS,at:1030});
    assert.equal(app.finance.accept({orderId:ID,actorId:SPONSOR,termsVersion:TERMS,at:1030}).events.length,2);
    assert.equal(authorize(app).state,'authorized');
  }finally{app.close();}
});
test('mock decline records an immutable attempt and allows separately keyed retry',()=>{
  const app=create();
  try{
    reserve(app);approve(app);quoteAndAgree(app);
    const decline=authorize(app,'decline','SYN-AUTH-first',1040);
    assert.equal(decline.state,'accepted');
    assert.equal(decline.events.at(-1).kind,'mock_declined');
    assert.equal(authorize(app,'decline','SYN-AUTH-first',1040).events.length,3);
    assert.throws(()=>authorize(app,'approve','SYN-AUTH-first',1040),/mock_attempt_conflict/);
    assert.equal(authorize(app,'approve','SYN-AUTH-retry',1041).state,'authorized');
    assert.throws(()=>authorize(app,'approve','SYN-AUTH-another',1042),/authorization_requires_fictional_agreement/);
  }finally{app.close();}
});
test('no mock capture before reconciled delivery; capture and refund replay safely',()=>{
  const app=create();
  try{
    reserve(app);approve(app);quoteAndAgree(app);authorize(app);
    assert.throws(()=>app.finance.capture({orderId:ID,actorId:SPONSOR,at:1041}),/capture_requires_reconciled_delivery/);
    assert.throws(()=>app.finance.refund({orderId:ID,actorId:SPONSOR,at:1042}),/refund_requires_mock_capture/);
    delivered(app);
    const captured=app.finance.capture({orderId:ID,actorId:SPONSOR,at:1070});
    assert.equal(captured.state,'captured'); assert.equal(captured.simulatedNetCents,250);
    assert.equal(app.finance.capture({orderId:ID,actorId:SPONSOR,at:1070}).events.length,4);
    assert.throws(()=>app.finance.refund({orderId:ID,actorId:'r',at:1080}),/unauthorized_fictional_sponsor/);
    const refund=app.finance.refund({orderId:ID,actorId:SPONSOR,at:1080});
    assert.equal(refund.state,'refunded');assert.equal(refund.simulatedNetCents,0);
    assert.equal(app.finance.refund({orderId:ID,actorId:SPONSOR,at:1080}).events.length,5);
    assert.deepEqual(app.ledger.available('food'),4);
  }finally{app.close();}
});
test('pre-pickup order cancellation voids mock authorization within same SQLite transaction',()=>{
  const app=create();
  try{
    reserve(app);approve(app);quoteAndAgree(app);authorize(app);
    app.orders.cancel({id:ID,actorId:'d',evidenceRef:'SYN-cancel',at:1045});
    const q=app.finance.get(ID);
    assert.equal(q.state,'voided');
    assert.equal(q.events.at(-1).kind,'authorization_voided');
    assert.equal(q.simulatedNetCents,0);
    assert.equal(app.ledger.available('food'),12);
    assert.throws(()=>app.finance.capture({orderId:ID,actorId:SPONSOR,at:1060}),/capture_requires_reconciled_delivery/);
  }finally{app.close();}
});
test('expiry voids fictional authorization but not real charges',()=>{
  const app=create();
  try{
    reserve(app);approve(app);quoteAndAgree(app);authorize(app);
    assert.equal(app.orders.expireDue(1_000_000),1);
    assert.equal(app.finance.get(ID).state,'voided');
    assert.equal(app.ledger.available('truck'),12);
  } finally {app.close();}
});
test('append-only commercial evidence cannot be altered and timestamps are monotone',()=>{
  const app=create();
  try{
    reserve(app);approve(app);quoteAndAgree(app);
    assert.throws(()=>app.finance.authorize({orderId:ID,actorId:SPONSOR,attemptId:'SYN-AUTH-2',mode:'approve',at:1029}),/out_of_order_commercial_event/);
    assert.throws(()=>app.finance.authorize({orderId:ID,actorId:SPONSOR,attemptId:'bad',mode:'approve',at:1040}),/invalid_mock_attempt/);
    assert.throws(()=>app.ledger.db.exec("DELETE FROM synthetic_commercial_events"),/append_only_commercial_events/);
    assert.throws(()=>app.ledger.db.exec("UPDATE synthetic_commercial_events SET kind='x'"),/append_only_commercial_events/);
    assert.equal(app.finance.get(ID).state,'accepted');
  }finally{app.close();}
});
test('file-backed commercial proof survives restart, refund leaves zero simulated net',()=>{
  const dir=mkdtempSync(join(tmpdir(),'maya-syn-commerce-'));
  const filename=join(dir,'fictional.sqlite');
  try{
    const a=create(filename);
    try{reserve(a);approve(a);quoteAndAgree(a);authorize(a);delivered(a);}finally{a.close();}
    const b=create(filename);
    try{
      assert.equal(b.finance.get(ID).state,'authorized');
      assert.equal(b.orders.get(ID).state,'reconciled');
      b.finance.capture({orderId:ID,actorId:SPONSOR,at:1070});
      b.finance.refund({orderId:ID,actorId:SPONSOR,at:1080});
      assert.equal(b.finance.get(ID).simulatedNetCents,0);
    }finally{b.close();}
  }finally{rmSync(dir,{recursive:true,force:true});}
});
