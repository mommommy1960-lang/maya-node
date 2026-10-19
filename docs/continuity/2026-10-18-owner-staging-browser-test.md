# Maya recovery staging — October 18, 2026

## Owner-observed results
During guided testing, the owner reported opening the staging UI, signing in using her newly configured staging secret, submitting `Reply with the word pineapple.`, receiving `pineapple`, and refreshing the page with the prompt and reply still visible. These are owner-reported browser observations, not independently executed HTTP or database tests by ChatGPT. Persistence across refresh does not alone prove server-side D1 persistence.

## Recovery changes reported by Gemini
Gemini reported deploying the separate maya-recovery-staging Worker with Workers AI and dedicated staging D1 storage, correcting an initial production DB binding mismatch, removing a fallback access code, expiring sessions after two hours, restricting access to a single owner, and preserving the owner-configured secret on subsequent deployment. Gemini reported that production resources were unchanged; this has not been independently audited by ChatGPT.

The first owner test returned provider error 5028 for retired model @cf/meta/llama-3-8b-instruct. Gemini subsequently reported replacing it with @cf/meta/llama-3.1-8b-instruct-fp8 and returning model failures as errors rather than assistant replies. The owner then reported the successful response above.

## Scope and limitations
This is an owner-only chat demo. It does not establish restoration of the original ChatGPT Sites project or the original Maya application behavior. It does not establish full security certification, verified email ownership, multi-user isolation, billing integration, or production readiness. No passwords, tokens, or customer data are recorded here.

## Authorized next work
1. Prepare external tester access with individual credentials or verified identity, expiring/revocable sessions, scoped data access, request limits and clear test-data terms. Verify rejected unauthenticated access and cross-user isolation using two test identities before inviting collaborators. Never share the owner credential.
2. Inspect existing Stripe products, prices, checkout and customer portal configuration before changing commercial terms. Prepare isolated sandbox checkout, server-verified payment fulfillment and customer billing-management tests. The existing mail Worker's /cancel route cancels queued mail jobs, not Stripe subscriptions.
3. Preserve the working owner demo, its secret and separate test storage. Keep live charges and outbound mail disabled during preparation. Do not interpret the older $25 human-delivered Founding Review as an approved price or entitlement for AI access.
4. Confirm actual saved conversation data via authenticated server retrieval or a fresh browser session, and record executed checks separately from code inspection and third-party reports.
