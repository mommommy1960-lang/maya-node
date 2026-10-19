# Maya staging Stripe connectivity — October 18, 2026

Recorded at approximately 22:19 America/Los_Angeles (October 19 UTC). This is a continuity record, not a launch approval.

## Owner-observed result

The owner refreshed the Maya recovery staging page, clicked **Test Stripe Connectivity (Prices Read)**, and supplied screenshots showing the updated button and a green message: Stripe sandbox authenticated successfully (Mode: Test / Sandbox, Account: Connected).

URL: https://maya-recovery-staging.mommommy1960.workers.dev

The same screen shows **Checkout Blocked: Missing STRIPE_PRICE_ID configuration binding**. This establishes the displayed Prices Read connectivity-test success, not completed Checkout, webhook fulfillment, independent customer authentication, or commercial readiness. This recording assistant did not independently inspect Stripe API traffic or execute the deployed test.

## Dashboard AI deployment handoff (reported, not independently verified here)

The Cloudflare dashboard AI reported that the previously deployed handler still used GET /v1/account and the old button label, despite earlier external assistant claims of updates. Repeated refreshes had shown the unchanged page.

It then reported deploying version **20fc3e82-110c-433e-a338-c73bafeec3c7**, version #14, created **2026-10-19T05:16:07Z**, and re-fetching active source to verify:

- Test endpoint now calls GET https://api.stripe.com/v1/prices?limit=1.
- Button label is Test Stripe Connectivity (Prices Read).
- Response success handling was adapted for a Stripe list response rather than a top-level account id.

It reported preserving existing bindings, secrets, authentication, chat history, staging D1 and other handlers through a content-only replacement. It reported no changes to legacy maya-node or live billing. These preservation claims were not independently audited by this recording assistant. Subsequent owner screenshots corroborate the visible button update and green test result.

## Next work and constraints

- Owner is opening Stripe to confirm the same Test mode/sandbox used by the saved restricted key.
- Approved practice amount is **USD $10/month recurring, sandbox only**. It is not an approved public launch price. No real card or real charge is authorized.
- Select/verify an existing matching sandbox price before creating a duplicate; otherwise create the practice product/price in the correct sandbox and record its non-secret price id.
- STRIPE_PRICE_ID is missing according to the observed UI. Webhook destination, signing-secret binding, event handling and end-to-end Checkout remain unverified here.
- Products and Prices permissions were previously set to Read; do not assume the runtime key can create products/prices or broaden permissions merely for the connectivity test.
- Verify sandbox Checkout, verified webhook, correct entitlement, duplicate handling, payment failure/renewal/cancellation and actual bounded AI replies before claiming the payment service works.
- Owner sign-in and historical conversation are visible. A stored pineapple reply alone does not verify current AI inference, per-customer isolation or a complete tester service.
- Preserve STAGING_ACCESS_SECRET and STRIPE_SECRET_KEY; never record their values. Preserve isolated staging storage and legacy production resources.
- Keep live sales/launch and email dispatch disabled during recovery. No API credit purchases or automatic recharge.
- The missing original ChatGPT Sites project is a separate recovery issue; this staging progress does not restore that project's access.
