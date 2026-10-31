# Owner sandbox billing candidate — October 19, 2026

**Integrated candidate locally tested, NOT DEPLOYED. Owner sandbox billing only; separate customer authentication and a public launch are not implemented.**

The owner supplied the working staging source in chat after tablet editor copying succeeded. That source uses bearer tokens, recovery_sessions, recovery_messages, two-hour owner sessions, the fp8 AI model, and /api/stripe/checkout. The rejected external v2 rewrote these assumptions. This candidate preserves them instead.

## Integrated files added

- worker.mjs: integrated candidate based on the owner-supplied active source, retaining bearer owner login, original tables, local storage keys and fp8 model. Reassembled source, not byte-identical.
- ui.mjs: owner login/chat plus subscription status, explicit ID import, portal and period-end cancellation controls.
- dist/worker.mjs: dependency-free single-file bundled Worker for future dashboard upload.
- bundle.py: deterministic bundler; run python bundle.py.
- test/worker.test.mjs and test/sqlite_bridge.py: tests of the actual bundled Worker against real temporary local SQLite and mocked Stripe.

Changes also preserve history on session expiry, reject malformed session timestamps, implement server-side signout, bound messages and directly verify the configured sandbox price.

Final validation: **32 tests passed, 0 failed** with node --test test/payments.test.mjs test/worker.test.mjs. Bundled Worker syntax check passed. No hosted Cloudflare/Stripe or browser visual test performed.

## Earlier module files

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

No Cloudflare/Stripe runtime test, registered webhook, secret binding, portal configuration, existing subscription import, or deployed candidate has been verified here. The integrated single-file dist/worker.mjs has now passed syntax checks and request-flow tests. It is based on the supplied source and must be compared with fresh active source before deployment. payments.mjs alone is not a replacement Worker.

## Remaining integration

1. Assemble candidate from actual active source; inspect the narrow diff and syntax-check both files. Keep current successful deployment available for rollback.
2. Review/apply additive SQL to the isolated staging D1 only. Add STRIPE_WEBHOOK_SECRET privately; preserve all existing bindings. Register the exact /api/stripe/webhook URL and seven event types in the matching sandbox. This step requires authorized account access.
3. Configure a sandbox Billing Portal and only the minimum additional restricted-key read/portal permissions reported necessary by actual Stripe errors. Do not broaden live permissions.
4. Add owner-only controls to the existing UI for status, read-only subscription discovery, explicit confirmed import, portal and cancellation. `GET /api/stripe/discover` looks up the exact configured owner email in the Stripe test account, lists that customer's subscriptions, selects only one exact configured practice-price match, then re-fetches the canonical subscription and paid invoice. It rejects multiple customer/subscription matches, incomplete pagination, non-sandbox objects, customer mismatches and subscriptions that are not currently paid and active. It performs GET requests only and does not write D1 or create billing objects. The UI exposes a separate Link action that requires an explicit confirmation and then calls the existing owner import route; that route is the only step that writes the owner billing record. UI wiring is in `ui.mjs` and bundled in `dist/worker.mjs`; browser visual verification remains pending. The already-paid subscription must be explicitly imported; it has no recorded checkout linkage.
5. Deploy only after assembled integration review; verify owner signin/history/chat are unchanged, then exercise actual sandbox event delivery, retry, import, portal, cancellation and expiry.
6. Separate customer authentication and server-enforced customer entitlements remain a later implementation, with independent identity and isolation tests. Do not gate owner chat or market this as a customer-ready system.

Never place Stripe keys, owner secrets, bearer tokens, or webhook signing secrets in GitHub. Preserve maya-node and live billing.

## Read-only subscription discovery review

The owner-authenticated `GET /api/stripe/discover` endpoint is intentionally separate from the state-changing import endpoint. It uses the configured owner email only to locate exact-email Stripe test-mode customer records, then reads that customer's subscriptions and canonical subscription/invoice. It does not use a bearer token as a Stripe identifier, create a customer/subscription/checkout, or write D1. Multiple matches and incomplete pagination fail closed. The UI keeps the discovered subscription ID in page memory only and exposes a separate confirmation dialog before calling the existing explicit import route. Automated tests mock Stripe and use temporary local SQLite; they do not contact a real Stripe account or hosted D1.

## Deployment blocker observed

The agent cloud browser is at Cloudflare login. No authenticated deployment is available. No source, D1 data, secret or Stripe configuration was changed in the accounts. Account access, webhook registration/signing secret, matching sandbox portal configuration and actual runtime tests remain necessary. Do not confuse the 32 local tests with hosted verification.

## Continuous integration

The `Owner Sandbox Billing Integration Tests` workflow checks that `dist/worker.mjs` matches the deterministic bundle, validates JavaScript syntax, and runs both Stripe payment and Worker integration suites on pull requests touching this candidate. These tests do not deploy to Cloudflare or contact live Stripe.
