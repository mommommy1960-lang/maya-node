import test from 'node:test';
import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { SandboxStripeWebhookInbox } from './sandbox-stripe-webhook.mjs';
import { reviewTestOrderWithSignedInbox as review } from './sandbox-stripe-observation-review.mjs';

const SECRET='whsec_synthetic_review_123456', NOW=1700000000;
const commercial={ synthetic:true, provider:'LOCAL_SIMULATOR_ONLY_NOT_STRIPE',
  orderId:'SYN-ORDER-REVIEW', sponsorFeeCents:250, receiverFeeCents:0,
  termsVersion:'SYN-TERMS-v1', currency:'USD' };
const checkoutSession={ object:'checkout.session', id:'cs_test_review123',
  client_reference_id:commercial.orderId, amount_total:250, currency:'usd',
  status:'complete', payment_status:'paid', payment_intent:'pi_test_review123',
  livemode:false, customer_email:'NEVER_EXPORT@example.invalid' };
const paymentIntent={ object:'payment_intent', id:'pi_test_review123',
  latest_charge:'ch_test_review123', amount_received:250, currency:'usd',
  status:'succeeded', livemode:false, receipt_email:'NEVER_EXPORT@example.invalid' };
const refund={ object:'refund', id:'re_test_review123', livemode:false,
  payment_intent:paymentIntent.id, charge:paymentIntent.latest_charge,
  amount:250, status:'succeeded' };
const inputs=()=>({commercial,checkoutSession,paymentIntent,confirmedTestAccount:true});
function signed(type,id,eventId) {
  const rawBody=JSON.stringify({id:eventId,type,created:NOW-10,livemode:false,
    data:{object:{id,livemode:false,email:'NEVER_EXPORT@example.invalid'}}});
  const v1=createHmac('sha256',SECRET).update(String(NOW)+'.'+rawBody).digest('hex');
  return {rawBody,signatureHeader:'t='+NOW+',v1='+v1,webhookSecret:SECRET,nowSeconds:NOW};
}
function harness(filename=':memory:') {
  const db=new DatabaseSync(filename);
  const inbox=new SandboxStripeWebhookInbox(db);
  let num=0;
  const add=(type,id)=>inbox.observe(signed(type,id,'evt_review_'+(++num).toString().padStart(6,'0')));
  const addPayment=()=>{
    add('checkout.session.completed',checkoutSession.id);
    add('payment_intent.succeeded',paymentIntent.id);
  };
  return {db,inbox,add,addPayment,close:()=>db.close()};
}
const blocked=(result,reason)=>{
  assert.equal(result.outcome,'BLOCKED');
  assert.ok(result.blockers.includes(reason),JSON.stringify(result.blockers));
  assert.equal(result.providerDeliveryVerified,false);
  assert.equal(result.authorizedToDispatch,false);
};
test('no signed local event evidence means no hypothetical payment match',()=>{
  const h=harness();try {
    blocked(review({...inputs(),inbox:h.inbox}),'verified_checkout_observation_missing');
    assert.equal(h.inbox.count(),0);
  } finally {h.close();}
});
test('two verified local event records + independent same-order facts produce only human review',()=>{
  const h=harness();try {
    h.addPayment();
    const before=h.inbox.count();
    const result=review({...inputs(),inbox:h.inbox});
    assert.equal(result.outcome,'TEST_PAYMENT_EVIDENCE_FOR_HUMAN_REVIEW');
    assert.equal(result.matchedToLocalSignedObservations,true);
    assert.equal(result.providerDeliveryVerified,false);
    assert.equal(result.appliedToOrders,false);
    assert.equal(result.liveBillingPermitted,false);
    assert.equal(result.recipientChargedCents,null);
    assert.equal(h.inbox.count(),before);
    assert.doesNotMatch(JSON.stringify(result),/NEVER_EXPORT|pi_test_|cs_test_|ch_test_/);
  } finally {h.close();}
});
test('out-of-order signed observations cannot bypass corroboration',()=>{
  const h=harness();try {
    h.add('payment_intent.succeeded',paymentIntent.id);
    blocked(review({...inputs(),inbox:h.inbox}),'verified_checkout_observation_missing');
    h.add('checkout.session.completed',checkoutSession.id);
    assert.equal(review({...inputs(),inbox:h.inbox}).blockers.length,0);
  } finally {h.close();}
});
test('wrong order, amount, test account and unrelated event fail closed',()=>{
  const h=harness();try {
    h.addPayment();
    blocked(review({...inputs(),inbox:h.inbox,confirmedTestAccount:false}),
      'test_account_not_independently_confirmed');
    blocked(review({...inputs(),inbox:h.inbox,checkoutSession:{
      ...checkoutSession,client_reference_id:'SYN-OTHER-ORDER'
    }}),'order_not_bound_at_checkout');
    blocked(review({...inputs(),inbox:h.inbox,paymentIntent:{
      ...paymentIntent,amount_received:100
    }}),'payment_not_captured_for_exact_quote');
    const wrong=harness();
    try {
      wrong.add('checkout.session.completed','cs_test_unrelated');
      wrong.add('payment_intent.succeeded','pi_test_unrelated');
      blocked(review({...inputs(),inbox:wrong.inbox}),'verified_payment_observation_missing');
    }finally{wrong.close();}
  } finally {h.close();}
});
test('missing or fake inbox cannot impersonate a signed event store',()=>{
  blocked(review({...inputs()}),'verified_test_inbox_required');
  blocked(review({...inputs(),inbox:{db:{prepare(){return {all(){return []}}}}}}),
    'verified_test_inbox_required');
});
test('duplicate deliveries remain inert and do not create a second observation',()=>{
  const h=harness();try {
    h.addPayment();
    const again=h.inbox.observe(signed('checkout.session.completed',checkoutSession.id,'evt_review_000001'));
    assert.equal(again.duplicate,true);
    assert.equal(h.inbox.count(),2);
    assert.equal(review({...inputs(),inbox:h.inbox}).matchedToLocalSignedObservations,true);
  } finally {h.close();}
});
test('refund cannot be inferred without independent refund and matching charge webhook',()=>{
  const h=harness();try {
    h.addPayment();
    blocked(review({...inputs(),refund,inbox:h.inbox}),'verified_refund_observation_missing');
    h.add('charge.refunded','ch_test_unrelated');
    blocked(review({...inputs(),refund,inbox:h.inbox}),'verified_refund_observation_missing');
    blocked(review({...inputs(),refund:{...refund,charge:'ch_test_unrelated'},inbox:h.inbox}),
      'refund_charge_link_not_verified');
  } finally {h.close();}
});
test('full refund requires charge matching PaymentIntent and signed charge.refunded observation',()=>{
  const h=harness();try {
    h.addPayment();h.add('charge.refunded',refund.charge);
    const result=review({...inputs(),refund,inbox:h.inbox});
    assert.equal(result.outcome,'TEST_REFUND_EVIDENCE_FOR_HUMAN_REVIEW');
    assert.equal(result.appliedToOrders,false);
    blocked(review({...inputs(),refund:{...refund,amount:125},inbox:h.inbox}),
      'refund_not_verified');
  } finally {h.close();}
});
test('signed receipt remains available after SQLite restart, without provider payload persistence',()=>{
  const dir=mkdtempSync(join(tmpdir(),'maya-review-'));
  const file=join(dir,'sandbox.sqlite');
  try {
    const first=harness(file);try {first.addPayment();}finally{first.close();}
    const second=harness(file);try {
      const result=review({...inputs(),inbox:second.inbox});
      assert.equal(result.matchedToLocalSignedObservations,true);
      assert.equal(second.inbox.count(),2);
      assert.doesNotMatch(JSON.stringify(second.db.prepare('SELECT * FROM sandbox_stripe_observations').all()),
        /NEVER_EXPORT|@example|receipt_email/);
    }finally{second.close();}
  }finally{rmSync(dir,{recursive:true,force:true});}
});
test('a signed failed payment is not proof of succeeded payment',()=>{
  const h=harness();try{
    h.add('checkout.session.completed',checkoutSession.id);
    h.add('payment_intent.payment_failed',paymentIntent.id);
    blocked(review({...inputs(),inbox:h.inbox}),'verified_payment_observation_missing');
  }finally{h.close();}
});
