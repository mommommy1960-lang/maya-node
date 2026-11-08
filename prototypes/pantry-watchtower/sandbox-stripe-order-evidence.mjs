/**
 * Read-only, synthetic-only Stripe TEST-mode checkout evidence comparator.
 * It never reads secrets, calls Stripe, stores provider payloads, authorizes a
 * payment, marks a delivery complete, or changes customer/order balances.
 * The caller MUST independently fetch these objects from the verified test
 * account. A screen, webhook event ID, or a whsec_ prefix is not enough.
 */
const fail = (errors, code, ok) => { if (!ok) errors.add(code); };
const obj = v => !!v && typeof v === 'object' && !Array.isArray(v);
const textId = v => typeof v === 'string' && /^[A-Za-z0-9_-]{3,180}$/.test(v);
const amount = v => Number.isSafeInteger(v) && v >= 0;

/** Compare independent test-provider facts to a fictional Maya quote, WITHOUT settlement. */
export function compareStripeTestOrderEvidence({
  commercial, checkoutSession, paymentIntent, refund = null,
  confirmedTestAccount = false,
} = {}) {
  const errors = new Set();
  fail(errors, 'test_account_not_independently_confirmed', confirmedTestAccount === true);
  fail(errors, 'fictional_quote_required', obj(commercial) && commercial.synthetic === true &&
    commercial.provider === 'LOCAL_SIMULATOR_ONLY_NOT_STRIPE' &&
    textId(commercial.orderId) && amount(commercial.sponsorFeeCents) &&
    commercial.sponsorFeeCents > 0 && commercial.receiverFeeCents === 0 &&
    commercial.currency === 'USD' && typeof commercial.termsVersion === 'string');
  fail(errors, 'test_checkout_required', obj(checkoutSession) && checkoutSession.object === 'checkout.session' &&
    textId(checkoutSession.id) && checkoutSession.id.startsWith('cs_test_') &&
    checkoutSession.livemode === false);
  fail(errors, 'test_payment_intent_required', obj(paymentIntent) &&
    paymentIntent.object === 'payment_intent' && textId(paymentIntent.id) &&
    paymentIntent.id.startsWith('pi_') && paymentIntent.livemode === false);
  if (obj(refund)) fail(errors, 'test_refund_required', refund.object === 'refund' &&
    textId(refund.id) && refund.id.startsWith('re_') && refund.livemode === false);
  // Never trust a UI assertion of 'paid'. The independent test PaymentIntent
  // and the checkout object must agree on identity and amount.
  if (obj(commercial) && obj(checkoutSession)) {
    fail(errors, 'order_not_bound_at_checkout', checkoutSession.client_reference_id === commercial.orderId);
    fail(errors, 'checkout_amount_or_currency_mismatch', amount(checkoutSession.amount_total) &&
      checkoutSession.amount_total === commercial.sponsorFeeCents &&
      checkoutSession.currency === String(commercial.currency).toLowerCase());
    fail(errors, 'checkout_not_paid', checkoutSession.status === 'complete' &&
      checkoutSession.payment_status === 'paid');
  }
  if (obj(checkoutSession) && obj(paymentIntent)) {
    fail(errors, 'payment_intent_not_bound_to_checkout',
      checkoutSession.payment_intent === paymentIntent.id);
  }
  if (obj(commercial) && obj(paymentIntent)) {
    fail(errors, 'payment_not_captured_for_exact_quote', paymentIntent.status === 'succeeded' &&
      amount(paymentIntent.amount_received) &&
      paymentIntent.amount_received === commercial.sponsorFeeCents &&
      paymentIntent.currency === String(commercial.currency).toLowerCase());
  }
  if (obj(refund) && obj(paymentIntent) && obj(commercial)) {
    fail(errors, 'refund_not_verified', refund.payment_intent === paymentIntent.id &&
      refund.status === 'succeeded' && amount(refund.amount) &&
      refund.amount === commercial.sponsorFeeCents);
  }
  const blockers = Object.freeze([...errors].sort());
  return Object.freeze({
    scope: 'FICTIONAL_STRIPE_TEST_EVIDENCE_ONLY',
    outcome: blockers.length ? 'BLOCKED' : refund ? 'TEST_REFUND_MATCH_FOR_HUMAN_REVIEW' : 'TEST_PAYMENT_MATCH_FOR_HUMAN_REVIEW',
    blockers,
    orderId: textId(commercial?.orderId) ? commercial.orderId : null,
    recipientChargedCents: null, // no real recipient ledger, NEVER invent a zero actual charge
    appliedToOrders: false,
    authorizedToDispatch: false,
    liveBillingPermitted: false,
  });
}
