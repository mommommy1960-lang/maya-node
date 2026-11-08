import test from 'node:test';
import assert from 'node:assert/strict';
import { compareStripeTestOrderEvidence as check } from './sandbox-stripe-order-evidence.mjs';
const commercial = Object.freeze({ synthetic: true, provider: 'LOCAL_SIMULATOR_ONLY_NOT_STRIPE',
  orderId: 'SYN-ORDER-3', termsVersion: 'SYN-TERMS-2026-11-07-v1', sponsorFeeCents: 250,
  receiverFeeCents: 0, currency: 'USD' });
const checkoutSession = Object.freeze({ object: 'checkout.session', id: 'cs_test_order3', livemode: false,
  client_reference_id: commercial.orderId, amount_total: 250, currency: 'usd', status: 'complete',
  payment_status: 'paid', payment_intent: 'pi_test_order3', customer_email: 'PRIVATE@example.invalid' });
const paymentIntent = Object.freeze({ object: 'payment_intent', id: 'pi_test_order3', livemode: false,
  amount_received: 250, currency: 'usd', status: 'succeeded', receipt_email: 'PRIVATE@example.invalid' });
const refund = Object.freeze({ object: 'refund', id: 're_test_order3', livemode: false,
  payment_intent: paymentIntent.id, status: 'succeeded', amount: 250 });
const args = () => ({ commercial, checkoutSession, paymentIntent, confirmedTestAccount: true });
const blocked = (overrides, reason) => {
  const res = check({ ...args(), ...overrides });
  assert.equal(res.outcome, 'BLOCKED'); assert.ok(res.blockers.includes(reason));
  assert.equal(res.appliedToOrders, false); assert.equal(res.authorizedToDispatch, false);
  return res;
};
test('valid independent test-mode fictional quote match is REVIEW ONLY, not fulfillment', () => {
  const res = check(args());
  assert.equal(res.outcome, 'TEST_PAYMENT_MATCH_FOR_HUMAN_REVIEW');
  assert.equal(res.blockers.length, 0);
  assert.equal(res.appliedToOrders, false);
  assert.equal(res.authorizedToDispatch, false);
  assert.equal(res.liveBillingPermitted, false);
  assert.equal(res.recipientChargedCents, null);
  assert.doesNotMatch(JSON.stringify(res), /PRIVATE|pi_test|cs_test/);
});
test('existing unlinked $1 Stripe test checkout cannot be inferred to pay the $2.50 sample quote', () => {
  const result = blocked({ checkoutSession: { ...checkoutSession, client_reference_id: null,
    amount_total: 100 } }, 'order_not_bound_at_checkout');
  assert.ok(result.blockers.includes('checkout_amount_or_currency_mismatch'));
});
test('fails closed for unconfirmed account, live events and non-test checkout', () => {
  blocked({ confirmedTestAccount: false }, 'test_account_not_independently_confirmed');
  blocked({ checkoutSession: { ...checkoutSession, livemode: true } }, 'test_checkout_required');
  blocked({ checkoutSession: { ...checkoutSession, id: 'cs_live_order3' } }, 'test_checkout_required');
  blocked({ paymentIntent: { ...paymentIntent, livemode: true } }, 'test_payment_intent_required');
});
test('won\'t equate test checkout paid flag with provider evidence', () => {
  blocked({ paymentIntent: null }, 'test_payment_intent_required');
  blocked({ paymentIntent: { ...paymentIntent, status: 'requires_payment_method' } }, 'payment_not_captured_for_exact_quote');
  blocked({ checkoutSession: { ...checkoutSession, payment_status: 'unpaid' } }, 'checkout_not_paid');
});
test('binds one exact order and intent; rejects cross-order and other-currency data', () => {
  blocked({ checkoutSession: { ...checkoutSession, client_reference_id: 'SYN-ORDER-4' } }, 'order_not_bound_at_checkout');
  blocked({ checkoutSession: { ...checkoutSession, payment_intent: 'pi_other' } }, 'payment_intent_not_bound_to_checkout');
  blocked({ paymentIntent: { ...paymentIntent, amount_received: 249 } }, 'payment_not_captured_for_exact_quote');
  blocked({ checkoutSession: { ...checkoutSession, currency: 'cad' } }, 'checkout_amount_or_currency_mismatch');
});
test('succeeded full test refund matches only with independent refund evidence', () => {
  const res = check({ ...args(), refund });
  assert.equal(res.outcome, 'TEST_REFUND_MATCH_FOR_HUMAN_REVIEW');
  blocked({ refund: { ...refund, amount: 100 } }, 'refund_not_verified');
  blocked({ refund: { ...refund, payment_intent: 'pi_other' } }, 'refund_not_verified');
  blocked({ refund: { ...refund, livemode: true } }, 'test_refund_required');
});
test('rejects unsafe/absent fictional quote and never reports actual recipient charge', () => {
  const res = blocked({ commercial: { ...commercial, receiverFeeCents: 100 } }, 'fictional_quote_required');
  assert.equal(res.recipientChargedCents, null);
  blocked({ commercial: null }, 'fictional_quote_required');
});
test('pure, read-only and idempotent for repeated provider evidence; no PII is echoed', () => {
  const before = JSON.stringify(args());
  const a = check(args()), b = check(args());
  assert.deepEqual(a, b);
  assert.equal(JSON.stringify(args()), before);
  assert.doesNotMatch(JSON.stringify(a), /PRIVATE|@example|receipt_email/);
});
