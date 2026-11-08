# Maya Node signed TEST observation-to-fictional-order review gate
2026-11-08, America/Los_Angeles. **Synthetic-only, read-only, not a hosted integration.**

## Implementation
- New `sandbox-stripe-observation-review.mjs` joins **already-verified local TEST-mode event observations** held in `SandboxStripeWebhookInbox` with independently supplied Stripe TEST Checkout / PaymentIntent / refund objects, plus Maya's fictional $2.50 sponsor quote. It delegates precise quote/account/order/currency/payment/refund comparison to the existing fail-closed helper.
- Before indicating a **human-review-only** potential test payment match, require persisted `checkout.session.completed` and `payment_intent.succeeded` event-object identifiers that exactly match the independent Checkout and PaymentIntent objects. A signed `payment_intent.payment_failed` event does not substitute for `succeeded`; unrelated events cannot qualify.
- For a hypothetical full refund, also require a `charge.refunded` observation tied to the **charge ID** shown by independent PaymentIntent `latest_charge` and refund `charge`. A refund's ID is not the charge ID. Missing, mismatched or partially refunded provider evidence fails closed.
- Handles out-of-order event arrival, repeat delivery, independent SQLite restart and absent/test-mode-unconfirmed evidence. This is a **SELECT-only** view, never a payment processor, delivery trigger, order mutation or user messaging process; never emits provider object identifiers, customer emails or contents.
- Verified only against synthetic HMAC-signed local fixtures and the existing local SQLite inbox. **Do not treat the presence of a signed-local observation as proof of external Stripe provider delivery**. Provider webhook receipt at the original Maya Sites URL and order correlation there remain unverified.

## Independent CI evidence (source commit `16e6c5d46920a4d2356673e6661207658a0738d3`)
- [Pantry watchtower Node run 42461519146](https://github.com/mommommy1960-lang/maya-node/actions/runs/42461519146), job 128671616835: **132 passed, 0 failed, 0 skipped**, TAP log inspected. Ten additional regression cases from 122: missing/mismatched events, out-of-order, wrong order/amount/account, fake inbox, duplicate retry, refund charge linkage, restart persistence, failure event not success and no PII output.
- [Chromium browser-to-HTTP-to-SQLite run 42461519117](https://github.com/mommommy1960-lang/maya-node/actions/runs/42461519117), job 128671616917: real Chromium completed full and partial **fictional local** paths, explicit PASS lines.
- [Security & Ethics run 42461519125](https://github.com/mommommy1960-lang/maya-node/actions/runs/42461519125): all five jobs successful, including runtime/ledger, adversarial and scanning. Verified job status via GitHub API.

## Readiness and next highest-impact gate
**Real customers/data, actual dispatch, external messages, live billing and production deployment: NO-GO.** This is NOT Stripe-hosted webhook delivery evidence; no customer credentials, webhook endpoint settings, real charge or production database were touched. The current public QR/contact and ChatGPT Sites customer path are not proven to serve PR #109.

Next engineering priority: an authorized nonproduction, independently confirmed Stripe TEST webhook event delivered from provider to authenticated hosted receiver, with replay/status/read-only reconciliation to a distinct **fictional** order reference. Do not expose the local-only receiver or install test secrets on production. Separately: hosted deletion/isolated backup restore; authenticated tenant/role controls; incident backup/coverage; written pilot donor/receiver/transporter approvals, food-safety/legal/insurance reviews, founder go/no-go. Nov 10–14 remains a target for browser-verified synthetic journey, not public hosting. Nov 21–Dec 19 remains an evidence-based limited pilot decision window, not launch authorization.

## Workflow
Research → implement → independently test → save code/CI IDs/blockers → verify saves → Bruce-to-Bruce. No production action.
