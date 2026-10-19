# Owner sandbox billing candidate — October 19, 2026

**NOT DEPLOYED. This is an owner-demo billing increment, not customer authentication or a public launch.**

The owner supplied the working staging source in chat after tablet editor copying succeeded. That source uses bearer tokens, recovery_sessions, recovery_messages, two-hour owner sessions, the fp8 AI model, and /api/stripe/checkout. The rejected external v2 rewrote these assumptions. This candidate preserves them instead.

## Files

- payments.mjs: isolated billing module; signed webhook, canonical subscription/invoice verification, explicit owner-only import, status, portal, and period-end cancellation.
- migration.sql: additive owner_sandbox_* tables only.
- build_candidate.py: applies narrow insertion points to a separate copy of the actual source. Decodes only the clipboard serialization seen in the supplied message. Fails on missing/nonunique anchors. Does not deploy or modify the input file.
- test/payments.test.mjs: executable Node tests importing the real module, with mocked Stripe and stores.

## Scope and behavior

Owner chat remains available regardless of sandbox billing state. Billing status is separate and explicitly labeled owner_sandbox_only. No customer login, customer isolation, or customer entitlement enforcement is claimed. A stable internal owner ID is used; no email search or bearer token is sent to Stripe as a linkage identifier.

New checkout creation records its sandbox Checkout Session ID in D1 before returning its URL. Only these recorded sessions can initially link billing through webhook delivery. Existing paid subscription import requires an authenticated owner request with an explicit subscription ID and confirmOwnerImport=true; the Worker fetches that subscription and its invoice from Stripe and verifies the configured $10 monthly sandbox price. This is an owner administrative operation, not a customer self-service ownership claim.

All outbound Stripe requests reject live keys. Subscription/invoice snapshots require livemode=false, matching customer/subscription identity, an explicit valid paid-through end, exactly one quantity-one expected USD 1000 monthly recurring item, and a paid USD 1000 invoice with zero remaining. This intentionally narrow practice policy rejects discounts, trials, proration, or other amounts for review.

Supported webhook events: checkout.session.completed, checkout.session.async_payment_succeeded, invoice.paid, invoice.payment_failed, customer.subscription.updated, customer.subscription.deleted. Pending checkout does not grant access. Subscription events trigger a fresh canonical fetch, not blind application of historical payloads. D1Store uses one transactional D1 batch, unique event IDs, and revision guards. A failed fetch/commit remains retryable. It handles item-level current_period_end with a legacy subscription-level fallback and invoice.parent.subscription_details.subscription with a legacy fallback.

POST /api/stripe/cancel schedules cancel_at_period_end=true. It does not immediately revoke paid access. The verified webhook reconciles state. POST /api/stripe/portal uses the stored owner customer and a Stripe-hosted URL. Neither route accepts arbitrary customer IDs. GET /api/stripe/access-status returns billing state without changing the owner demo.

## Validation and limits

Run `node --test test/payments.test.mjs` (no npm dependencies). Initial run before the explicit owner import route: 19 tests passed, 0 failed. Re-run after any changes; see actual final test output in the accompanying handoff.

Tests cover actual handler behavior for signed/invalid/old signatures, unpaid checkout, ownership linkage, live rejection, expiry, exact price and invoice checks, duplicate delivery, upstream failure/retry, commit failure/retry, out-of-order state, overlapping updates, nested invoice linkage, cancellation behavior and owner authorization. D1 SQL is exercised separately with real local SQLite; it is not a substitute for hosted D1 verification.

No Cloudflare/Stripe runtime test, registered webhook, secret binding, portal configuration, existing subscription import, or deployed candidate has been verified here. The full assembled candidate cannot be claimed syntax-checked until the copied baseline is available as a local source file and the builder has run. This module is not a replacement Worker: uploading it alone would break the service.

## Remaining integration

1. Assemble candidate from actual active source; inspect the narrow diff and syntax-check both files. Keep current successful deployment available for rollback.
2. Review/apply additive SQL to the isolated staging D1 only. Add STRIPE_WEBHOOK_SECRET privately; preserve all existing bindings. Register the exact /api/stripe/webhook URL and seven event types in the matching sandbox. This step requires authorized account access.
3. Configure a sandbox Billing Portal and only the minimum additional restricted-key read/portal permissions reported necessary by actual Stripe errors. Do not broaden live permissions.
4. Add owner-only controls to the existing UI for status, explicit subscription-ID import, portal and cancellation. The backend candidate has these routes; UI wiring is not yet implemented. The already-paid subscription must be explicitly imported; it has no recorded checkout linkage.
5. Deploy only after assembled integration review; verify owner signin/history/chat are unchanged, then exercise actual sandbox event delivery, retry, import, portal, cancellation and expiry.
6. Separate customer authentication and server-enforced customer entitlements remain a later implementation, with independent identity and isolation tests. Do not gate owner chat or market this as a customer-ready system.

Never place Stripe keys, owner secrets, bearer tokens, or webhook signing secrets in GitHub. Preserve maya-node and live billing.
