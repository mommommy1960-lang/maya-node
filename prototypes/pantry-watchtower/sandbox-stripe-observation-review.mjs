/**
 * LOCAL SYNTHETIC TEST ONLY. Read-only join of verified Stripe TEST event
 * metadata already recorded in the inert SQLite inbox with separately fetched
 * test Checkout/PaymentIntent/refund objects and a fictional Maya quote.
 *
 * This is NOT a processor-delivery receipt: fixture-signed events also pass
 * the local inbox. A matching observation cannot authorize money, fulfillment,
 * customer contact or real-world dispatch.
 */
import { SandboxStripeWebhookInbox } from './sandbox-stripe-webhook.mjs';
import { compareStripeTestOrderEvidence } from './sandbox-stripe-order-evidence.mjs';

const safeCharge = id => typeof id === 'string' &&
  /^ch_[A-Za-z0-9_-]{3,177}$/.test(id);

/** All returned data is minimal, read-only, and deliberately non-actionable. */
export function reviewTestOrderWithSignedInbox({
  inbox, commercial, checkoutSession, paymentIntent, refund = null,
  confirmedTestAccount = false,
} = {}) {
  const comparison = compareStripeTestOrderEvidence({
    commercial, checkoutSession, paymentIntent, refund, confirmedTestAccount,
  });
  const blockers = new Set(comparison.blockers);
  if (!(inbox instanceof SandboxStripeWebhookInbox)) {
    blockers.add('verified_test_inbox_required');
  } else {
    // Only records previously checked using the raw-body HMAC verifier may be
    // joined. This is a SELECT: NEVER mutate payment or order states here.
    const rows = inbox.db.prepare(
      'SELECT event_type, object_id FROM sandbox_stripe_observations'
    ).all();
    const observed = (type, id) => typeof id === 'string' &&
      rows.some(row => row.event_type === type && row.object_id === id);
    if (!observed('checkout.session.completed', checkoutSession?.id))
      blockers.add('verified_checkout_observation_missing');
    if (!observed('payment_intent.succeeded', paymentIntent?.id))
      blockers.add('verified_payment_observation_missing');
    if (refund != null) {
      // charge.refunded refers to a CHARGE, not the refund object or PaymentIntent.
      // Do not infer a refunded order from an unrelated charge-level event.
      const chargeId = refund?.charge;
      if (!safeCharge(chargeId) || paymentIntent?.latest_charge !== chargeId)
        blockers.add('refund_charge_link_not_verified');
      if (!observed('charge.refunded', chargeId))
        blockers.add('verified_refund_observation_missing');
    }
  }
  const reasons = Object.freeze([...blockers].sort());
  return Object.freeze({
    scope: 'SIGNED_LOCAL_TEST_OBSERVATION_REVIEW_ONLY',
    outcome: reasons.length ? 'BLOCKED' :
      refund ? 'TEST_REFUND_EVIDENCE_FOR_HUMAN_REVIEW' :
        'TEST_PAYMENT_EVIDENCE_FOR_HUMAN_REVIEW',
    blockers: reasons,
    orderId: comparison.orderId,
    matchedToLocalSignedObservations: reasons.length === 0,
    providerDeliveryVerified: false,
    recipientChargedCents: null,
    appliedToOrders: false,
    authorizedToDispatch: false,
    liveBillingPermitted: false,
  });
}
