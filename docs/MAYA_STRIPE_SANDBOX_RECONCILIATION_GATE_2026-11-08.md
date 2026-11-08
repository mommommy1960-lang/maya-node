# Stripe TEST-only evidence-to-fictional-order reconciliation gate
2026-11-08 (America/Los_Angeles). **Read-only engineering checkpoint. Not production authorization.**

## Verified on this run

- The connected **Mya Brown** Stripe *test-mode* account (not the live account with the same name) was selected based on the account tool's `livemode=false` result. Three enabled webhook endpoint records currently target paths under `maya-working-workflow-lab.myqueen1960.chatgpt.site`, NOT the localhost PR #109 receiver. Merely enabling endpoints is **not** evidence of delivery or order fulfillment. No endpoint was changed.
- Read-only Stripe event listing included two `checkout.session.completed`, `payment_intent.succeeded`, and a later `charge.refunded` test event. This is provider-account event existence, **not** verified endpoint HTTP response, event replay, or Maya persistence. No real funds or new Stripe transactions were used in this run. No provider/customer identifier is needed in this public evidence.
- Existing PR #109 commercial terms include an illustrative **$2.50 sponsor fee, $0 fictional food recipient fee**. Prior verified Stripe checkout rehearsals were **$1.00 test payments without proven per-order binding**. They must **NOT** be booked against the $2.50 fictional quote.

## New implementation and CI

- Added `prototypes/pantry-watchtower/sandbox-stripe-order-evidence.mjs` plus eight tests. This is a **pure read-only comparison helper**, not a backend integration: the caller must independently fetch the objects from the correct test account and confirm account mode; the code itself does not connect to Stripe or guarantee authenticity.
- Before reporting a hypothetical TEST payment/refund match **for human review only**, it demands: real TEST-labeled checkout session and TEST PaymentIntent, exact fictional order `client_reference_id`, matching PaymentIntent linkage, exact sponsor amount/currency, paid/completed checkout, succeeded PaymentIntent and received amount; an optional refund requires succeeded/full amount and same PaymentIntent. The fictional recipient's *actual* charged amount is deliberately unknown, not asserted zero.
- Guards fail closed for missing test-account confirmation, live objects, cross-order mismatches, $1 vs $2.50 mismatch, partial refunds, missing or declined intents. Output includes only a synthetic order ID and reason codes, not provider/customer payloads. It cannot dispatch, authorize, change order/payment state, store records, or permit live billing.
- **Verified 122/122 synthetic Node CI** (0 failed), source commit `a83248f935570e7345f1d8859f37784bdccc947a`: [run 42457078917](https://github.com/mommommy1960-lang/maya-node/actions/runs/42457078917), [job 128658282777](https://github.com/mommommy1960-lang/maya-node/actions/runs/42457078917/job/128658282777), TAP totals inspected. [Real Chromium↔localhost↔SQLite browser run 42457078989](https://github.com/mommommy1960-lang/maya-node/actions/runs/42457078989) passed both fictional full/partial paths. [Security & Ethics run 42457078923](https://github.com/mommommy1960-lang/maya-node/actions/runs/42457078923) passed five jobs.
- This code remains in **unmerged draft PR #109**, not published to the original Maya Sites app, QR destination, or customer service. Vercel status cannot replace site source/route validation.

## Remaining critical gates and specific next experiment

1. On an authorized **isolated nonproduction endpoint**, verify signed *provider-delivered* Stripe TEST webhook HTTP delivery, retries/duplicates/out-of-order and response receipts, WITHOUT accepting live events/credentials. The current localhost receiver only has signed fixture evidence.
2. Add an **account-verified, server-generated TEST Checkout session with a fictional order reference**, capture exact amount/currency from Stripe's TEST API, use a data-minimizing binding and event sequence, and compare TEST refund evidence. Do not expose PII or change real Maya orders.
3. Align actual endpoint-subscription event types and the receiver's allowlist (the three configured TEST endpoints subscribe to checkout completion/async/expiry and refund/dispute events; the local verifier currently accepts only completion, two PaymentIntent statuses and refund).
4. Independently prove hosted deletion, downstream retention and **isolated backup restore** on the intended Maya hosted system; verify incident coverage, authenticated tenant permissions and safe rollback. Do not touch live data during rehearsals.
5. Written donor/receiver/transporter permissions, privacy and food-safety/legal review, independent outcome evidence, founder sign-off.

**Decision:** real-customer data, dispatch, external messages, production deployment and live billing **NO-GO**. Nov 8 technical/test checkpoint met; local browser scenario verified, hosted end-to-end not verified. Nov 10–14 demonstration and Nov 21–Dec 19 limited-pilot decision are targets, never proof or launch dates.
