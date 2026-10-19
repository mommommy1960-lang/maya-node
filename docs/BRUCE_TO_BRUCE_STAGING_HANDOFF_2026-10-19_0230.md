# Bruce-to-Bruce: Maya staging checkpoint

Checkpoint: October 19, 2026, approximately 02:30 America/Los_Angeles. Owner requested no more manual work tonight and asked to preserve this handoff.

## Observed evidence
User screenshot 1000017540.jpg shows the deployed Owner Practice Subscription interface, Stripe sandbox authentication verified, and No practice subscription linked yet. Original conversation history remains visible. Historical model error text is old history, not proof of current inference failure or success. Screenshot 1000017539.jpg shows Cloudflare account home.

## Scope and implementation
Worker: maya-recovery-staging. URL: https://maya-recovery-staging.mommommy1960.workers.dev
Candidate source and tests: experiments/owner-sandbox-billing-2026-10-19/ in this repository. Single-file dist/worker.mjs. Previously executed local tests: 32 passed; hosted Stripe lifecycle is not verified.
Gemini reports additive owner_sandbox_billing, owner_sandbox_events, owner_sandbox_checkouts migration and deployment; screenshot corroborates new UI, not every backend claim. Reported deployment ID: 1d955eb3-e408-438f-942b-201613705415. Exact currently active version was not independently fetched this turn.
STRIPE_PRICE_ID restored according to relay report; current green UI corroborates successful configured-price test. Expected value: price_1US957FFZvHRvAyGMcfwMZd7.
Owner billing is a sandbox demonstration. Owner chat remains available independently of billing. This is not public customer access gating or launch certification.

## Existing milestone
Existing $10/month sandbox subscription and paid practice invoice were observed in earlier Stripe screenshots. No real revenue. Do not create another subscription to recover linkage. Exact subscription ID must be retrieved/validated rather than guessed from an old screenshot.

## Blockers and work remaining
1. Existing practice subscription is still unlinked. Gemini reports its management executor cannot reach api.stripe.com (PERMISSION_DENIED). This is an executor restriction, not proof that the deployed Worker cannot reach Stripe.
2. In this turn the ChatGPT Stripe connector listed only Mya Brown LIVE account context. No sandbox context was available; no live billing query or mutation was performed. Do not silently use live context to find sandbox records.
3. This assistant has no authenticated Cloudflare session. No new login request was imposed on tired owner.
4. STRIPE_WEBHOOK_SECRET was last reported missing; verify binding by name, configure the matching SANDBOX destination securely, never publish secret values.
5. Portal configuration, successful import, verified signed event delivery, retry/idempotency, period-end cancellation and status reconciliation remain hosted-runtime checks, not completed claims.

## Next-session execution
Prefer authorized sandbox connector/account access or a tool with a verified sandbox session to retrieve the existing subscription. If management egress stays blocked, a carefully reviewed owner-authenticated Worker recovery flow could discover candidate sandbox subscriptions server-side; require strict expected-price/test-mode checks and explicit owner linkage, no public discovery endpoint, no auth bypass and no arbitrary direct D1 active flag. This is a possible next implementation, not a deployed feature. Existing import endpoint accepts exact subscription ID and confirmOwnerImport=true in authenticated owner context; Worker itself verifies Stripe data.
Use /api/stripe/access-status to check stored result. Do not claim the integration complete until actual lifecycle checks pass. Current source's supported webhook event list must be read before configuring destination; do not copy earlier contradictory reports.

## Preservation rules
Keep maya-node production and live billing untouched. Preserve all current secrets/bindings and all recovery history. No new charge, checkout, cancellation, destructive migration or public launch. Do not ask owner to keep clicking tonight. No passwords, signing secrets, tokens, or raw personal screenshots are included in this public handoff.

## Owner-requested next task — 02:37 America/Los_Angeles
Queen explicitly requested that we build the Worker-side automatic lookup when work resumes, so she does not have to find or copy a sub_ identifier manually. Record this as planned work, not implemented or deployed. No further work or owner clicking is requested tonight.

Implementation objective: extend the existing owner-authenticated staging recovery flow to query Stripe from the deployed Worker using its bound sandbox key. Identify the existing practice subscription for the configured price; verify livemode=false, USD 1000 monthly, current subscription and paid invoice, and intended owner linkage before using the existing validated import path. Price match alone does not establish ownership. Do not choose arbitrarily if there are multiple or ambiguous matches; return a clear result without linking. Handle pagination and restricted-key permission errors without exposing secrets. Preserve an already-linked different subscription. Add meaningful handler tests for unique verified match, no match, ambiguity, live data rejection, authorization, permission failure, and duplicate recovery. Verify hosted status after deployment. Preserve original owner login and conversation history, all secrets and bindings; keep production maya-node and live billing untouched. Do not create a new checkout, payment, or subscription, and do not cancel anything to perform recovery.
