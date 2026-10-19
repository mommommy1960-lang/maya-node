# Bruce-to-Bruce — next session

Saved October 19, 2026 at approximately 03:17 America/Los_Angeles at Queen's explicit request. Work is paused; this handoff is not a claim of background execution.

## Start here
Read docs/BRUCE_TO_BRUCE_STAGING_HANDOFF_2026-10-19_0230.md for the detailed checkpoint, evidence, limitations and owner-requested next task. Its latest update records automatic subscription lookup as planned work.

## Current observed status
- Staging URL: https://maya-recovery-staging.mommommy1960.workers.dev
- Latest owner screenshot shows Stripe sandbox authentication verified and the Owner Practice Subscription section present.
- Screenshot still says No practice subscription linked yet.
- Existing $10 monthly sandbox subscription and paid practice invoice were observed previously. This is a test milestone, not real revenue.
- Source/test package: experiments/owner-sandbox-billing-2026-10-19/ (single-file dist/worker.mjs). Previously executed local tests: 32 passed. Hosted billing lifecycle remains unverified.
- Expected configured price: price_1US957FFZvHRvAyGMcfwMZd7. Restored per relay report and successful UI price check.

## First task when resuming
Implement and test an owner-authenticated Worker-side lookup of the existing sandbox practice subscription, so Queen does not have to locate/copy a sub_ ID. Use the securely bound test key inside the Worker. Validate sandbox mode, configured price, USD 1000/month, paid invoice and intended owner linkage; matching price alone does not prove ownership. Reuse the validated import flow. Handle pagination, no match, ambiguous matches, permission failures, duplicate recovery and an already-linked different subscription safely. No arbitrary selection, public discovery route, auth bypass, direct forced-active D1 update, or secret exposure. This feature is NOT yet implemented or deployed.

## Execution constraints
Gemini reports api.stripe.com egress blocked from its management executor; deployed Worker reachability is a separate matter. Our Stripe connector listed only a LIVE account context, not the sandbox. Our Cloudflare browser session is not authenticated. Do not imply access to Queen's tablet session or impose repeated login loops.

## Remaining verification after lookup/import
Verify actual stored status through /api/stripe/access-status. Confirm sandbox webhook destination and STRIPE_WEBHOOK_SECRET binding securely (last reported missing); check current source for exact event types. Verify signed webhook delivery/retries/idempotency and Stripe portal configuration. Period-end cancellation testing remains pending and must not be performed merely to recover a subscription. Owner chat is independent of this sandbox billing snapshot; public customer payment-based access and launch readiness are not certified.

## Preserve
Production maya-node and live billing untouched. Preserve owner authentication, all secrets/bindings, recovery history and existing practice invoice/subscription. No new checkout, subscription, charge, cancellation, destructive migration or public launch as part of recovery. Queen asked to stop manual work for the night; resume from this record without repeating the entire investigation.

## Continuity receipts
Detailed checkpoint created in commit e12cf6399cb543cb25233cd8fb7560c4826aa18a; automatic lookup task added in d1d7b843ab7806ed620ad7b19ada8667cd15c14d. No secret values or personal screenshots included in this public record.
