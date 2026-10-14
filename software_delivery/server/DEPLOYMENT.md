# Maya Node runtime integration

## Product decision, October 14

Recommendation selected for implementation: **$25 USD buys 30 days of access**,
100 bounded AI replies, one authenticated account. One-time payment at launch;
no automatic renewal or trial-to-paid charge. Free trial: one hour and up to ten
replies, whichever is exhausted first. Large institutional integrations and
unlimited autonomous work are not part of this starter offer.

Rationale: repeated access fits an ongoing software assistant. Zapier uses monthly
task allowances (Professional $19.99/month with annual billing), supporting a
monthly allowance structure, not proving Maya's willingness-to-pay or capability.
https://zapier.com/blog/zapier-pricing/

Published reference model rates: GPT-4.1 mini $0.40/1M input, $1.60/1M output:
https://developers.openai.com/api/docs/models/gpt-4.1-mini
That model is marked deprecated in the current official documentation; do not
select it for a new deployment without confirming availability. Runtime model is
configurable. Under the illustrative rates, 100 replies averaging 2,000 input
and 600 output tokens would cost $0.176 in model tokens alone. This is an estimate,
not a measured cost or profit. Hosting, abuse, failed calls, processor fees,
taxes, support and future model rates are additional costs. No unlimited offer.

## Mounting

`createService` handles `/api/status`, `/api/trial`, `/api/maya`, `/api/checkout`,
and `/api/stripe/webhook`. Supply `new D1Store(env.DB)` behind Sites dispatch.
Dispatch owns identity headers; never expose the Worker through an alternate
public origin where callers can forge them. Use the Sites top-level sign-in link:
`/signin-with-chatgpt?return_to=%2Fmaya.html`. Do not implement custom OAuth.

Apply `schema.sql` as an immutable deployment migration, not request-time table
creation. This is prepared code, not a confirmed hosted migration.

Required secret/runtime keys:
- `OPENAI_API_KEY`, `OPENAI_MODEL`
- `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
- `STRIPE_SOFTWARE_PRICE_ID`, `STRIPE_MODE` (`test` first; `live` after validation)
- `STRIPE_ACCOUNT_ID` if handling connected-account events

The software price must be a new one-time USD 25.00 price with clear 30-day terms.
Do not reuse the human-review payment link. Configure webhook events for paid
Checkout completion/asynchronous success, refunds and disputes. Store session
mapping before presenting Checkout to the browser. Grant access only after
verified payment; a redirect grants nothing. Future automatic renewal requires
a separately implemented subscription lifecycle and explicit customer consent.

## Scope and verification

The model request is a real provider adapter, tested with stubbed HTTP responses;
no live inference was run. It supports bounded workflow analysis and organizing
redacted information, not school/bank database operations. No external tool calls
or email sending are provided. Quota reservations count attempts, including
upstream failures; disclose this during the pilot and add reconciled credits
before general commercial release. Prompts are limited to 4,000 characters,
outputs to 600 tokens, with provider storage disabled by request. That flag is
not a claim of zero provider retention or end-to-end encryption.

Open gates: connected Stripe account and approved model credentials; actual
provider calls and sandbox purchases; hosted D1 migration and integration;
browser/mobile click-through; rate limiting/account-abuse protection beyond
per-account quotas; privacy/refund terms and quota credit handling.

Do not publish a working paid-service claim or enable checkout until these gates
pass. Current confirmed contact Site has no configured runtime secrets. Stripe
and OpenAI Developers were offered for connection, not confirmed connected.
