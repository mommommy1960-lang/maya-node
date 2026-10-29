# Maya customer-launch execution checkpoint — October 29, 2026 (Pacific)

## Approved continuation — October 29, 2026
This section supersedes the earlier pending-send and pending-deletion statements below.
- Founder explicitly approved sending the prepared support reply and permanently deleting only the two named synthetic test fixtures.
- Sent the existing support draft in case 17489131 successfully. Sent message 1a188741e57b99df, existing thread 1a147f26fa2b85dc, provider returned SENT. No duplicate case created. Hosting facts and isolated recovery remain awaiting provider guidance.
- Deleted completed synthetic request 440f5436-35db-402e-a129-65a5bd07b2d4 and revoked synthetic request 40ebb0a6-ba91-4957-902a-2837f219caf4 through the authenticated hosted UI. Both confirmations accepted under the explicit approval.
- Refreshed hosted records: both fixture articles absent; original peer sample remains.
- Read all live rows in maya_action_requests (11), maya_action_outputs (6) and maya_action_events (31), using bounded pages through Sites. Neither target request ID appears in the request, output or linked event tables. All ten original founder-workspace filenames remain present. These global counts include other preserved account data and are not the founder-only UI totals.
- Connected Maya read_output for the deleted completed request returns File not found, reference d21fd411-532e-4095-aa1b-b66a88c9b5a4. This is expected denial evidence, not an outage.
- This establishes fresh hosted deletion of the completed and revoked synthetic fixtures and linked active rows. It does not establish hosting backup/log expiry, isolated recovery, every session/endpoint case, device-local copy deletion or external customer acceptance.
- Site remains active and public at version 20. No checkout activation, source deployment, restore, real customer processing or charge occurred.
- Next payment step needs selection between the connected Mya Brown test account and New business sandbox, followed by provider setup permissions and secret-only provisioning. Live identity liveness verification, hosting recovery, incident backup/coverage, business terms and external acceptance remain open.

## Stripe test setup — October 29, 2026
- Founder selected the connected Mya Brown test account. All Stripe setup calls use livemode=false and the selected test context; no live charge or live product created.
- Confirmed no existing price for offer lookup key maya-pilot-2026-10-28-v1 and no existing standard webhook endpoints in that test account.
- Created test one-time USD price price_1UVw4NJYOy8NtnKHDYMfH9jR (2500 cents), product prod_VX040oaZNIBtAz; offer marked TEST ONLY with access_days=30.
- Created test webhook we_1UVw4jJYOy8NtnKHFRzIbNoL at the existing Site /api/billing/webhook route. Enabled only checkout.session.completed, checkout.session.async_payment_succeeded, checkout.session.async_payment_failed, checkout.session.expired, charge.refunded and charge.dispute.created. Direct account only.
- Stored webhook signing secret in Sites as a secret, never in this file, source, chat or logs. Stored matching test offer configuration with MAYA_BILLING_ENABLED=false. Existing operator secret preserved. Runtime configuration revision 3.
- STRIPE_SECRET_KEY is still absent. Stripe connector can create test objects but cannot supply the hosted application's server API key. Official Stripe restricted-key guidance reviewed; use server-only restricted test key with price read, checkout session write/read and payment intent/charge read for this implementation; verify provider-required dependencies during rehearsal.
- Opened Stripe Dashboard API-key page. It requires login. Secure browserAuth prompt returned declined; no sign-in, key creation or credential extraction was attempted after that result. Do not retry without the user's renewed request.
- Rehearsal NOT completed: no actual test checkout, payment, webhook delivery, refund or entitlement acceptance. Checkout remains closed. Recovery, human coverage, business requirements, live liveness verification and external acceptance remain separate gates.
- Reapplied saved version 20 successfully with runtime revision 3: deployment appgdep_6ae37310a8f881918d52f14c0315015d, existing URL and MCP preserved. Hosted page still displays disabled checkout. No source or data schema change.

## Stripe Dashboard access recovered — October 29, 2026
- Google one-time security-code path repeatedly returned invalid code. At founder request, opened alternative methods; founder selected device approval through secure browserAuth.
- Google sign-in then proceeded, followed by Stripe's own SMS verification. Fresh browser state confirms signed-in Stripe Dashboard.
- Dashboard initially showed live mode; no live key revealed or changed. Switched the same account to Test mode; visible sandbox banner confirms no real transactions.
- Prepared, but did NOT submit, new restricted test key form named "Maya hosted payment rehearsal — test only". Selected only Checkout Sessions Write; Charges and Refunds Read; Payment Intents Read; Products Read; Prices Read. All other permissions None. No new key exists from this form yet.
- Original Sites editor link routes to a new edit composer; opening the historical editing conversation reports no access in this browser. This is a browser UI limit, not loss of native Sites owner/source access. No secret-entry screen has been staged.
- Server API key provisioning and provider checkout/webhook rehearsal remain incomplete. No passwords, verification codes or API secrets retained in this record. Checkout remains disabled.

## Decision
Customer launch is not complete. Synthetic-only boundary and closed checkout remain in place. This checkpoint records fresh hosted evidence and concrete external dependencies; no real customer data, charge, restore, production code change, DNS change or access expansion occurred.

## Current application
Native Sites get_site confirms existing project appgprj_6ad2958158e88191a37abacacbfe1f45 is active, public, founder-owned and latest saved version 20. Hosted page displays the selected $25 USD once / 30-day offer, free 50-record path and paid 250-record capacity. Paid checkout visibly disabled. Supported source helper reopened the existing managed checkout at commit 226f24435a0ff579e0ead38f8895c33195970c0b.

## Fresh hosted acceptance
- Signed-in founder browser loaded the existing workspace: initial baseline 10 requests, five completed outputs and four recorded refusals.
- Prepared maya-launch-check-20261029.txt, request 440f5436-35db-402e-a129-65a5bd07b2d4, with wholly invented text: "Synthetic launch acceptance check. No customer information. Disposable test record created October 29, 2026."
- Observed draft with no output; explicitly authorized the exact synthetic file on the website; executed on the website; observed completed state and download link.
- Connected Maya read_output returned the exact intended text and SHA-256 02ec60e00e9486f8edea3101d530d463313c8f8f539438ebe1a0b2969f6aab59. Independent expected-text hash matches; content length 108 UTF-8 bytes.
- Browser reported download event/path, but the artifact was not available through the supported shared-file paths. Do not claim an independent downloaded-file byte comparison or physical Android acceptance.
- Prepared separate maya-launch-revoke-20261029.txt, request 40ebb0a6-ba91-4957-902a-2837f219caf4. Authorized, revoked, attempted creation. Hosted UI shows revoked, permission_revoked block, no download control, refusal reference 96c15df1-f401-4cf7-b5be-a279ec4c983f.
- Neither new synthetic record has been deleted. Permanent hosted deletion needs action-time user confirmation. All pre-existing records preserved.
- No fresh independent customer account, all-endpoint isolation matrix or external tester acceptance established.

## Current maintenance
Operator maintenance response confirms last run a15b69c2-73f6-4278-8f6b-5aebeffe01dd, completed_at 1793286076213, removed counts zero across requests/outputs/events/notices, zero pending expiry, legacy records preserved. backups=not_inspected. No extra cleanup invoked.

## Hosting dependency advanced
Read actual latest Support reply in case 17489131, received October 28 at 5:33 PM Pacific. Support requests the email associated with the ChatGPT account creating/managing the Site. Site ownership confirms that email. Support explicitly cannot yet confirm Site-specific backups, retention or restoration, and distinguishes code rollback from database/file restoration.
Prepared an unsent reply in the existing support thread with confirmed owner email, exact Site/project, and the existing backup/log retention, deletion non-resurrection and isolated synthetic restore questions. Draft ID r4234694992434338421; message 1a1887193f6e578f. Not sent: current request does not explicitly authorize sending an email. No duplicate case or production restore.

## Payment/business dependencies
Read current existing live Mya Brown Stripe account. charges_enabled=true, payouts_enabled=true, details_submitted=true. Nevertheless requirements include currently_due and past_due individual.verification.proof_of_liveness. This owner-only verification is not complete; flags alone do not close payment readiness.
Connected Stripe account inventory now includes the existing live account and two test accounts. No sandbox selected, credentials provisioned, test checkout/webhook/refund run, provider object created or real-money transaction attempted.
No banking/identity details copied into this report. No current licensing confirmation found in a focused recent-email search; absence of matching email is not proof of no registration.
Offer refund terms, applicable tax handling, billing-record retention and full provider payment-to-entitlement acceptance remain open in source documentation.

## Remaining executable sequence
1. With explicit send authorization, send the prepared owner-email correction in existing Support case; review provider procedure and obtain required approvals before any isolated hosted recovery drill. Never restore into live DB.
2. With explicit permanent-deletion confirmation for the two named synthetic fixtures only, exercise hosted owner deletion, re-query file URLs and receipt export, confirm their linked records disappear while original records remain. Keep backup/log deletion separately open.
3. Founder completes provider proof-of-liveness and selects the intended Stripe sandbox; obtain supported narrow test setup access and secret-only provisioning. Register/rehearse matching provider test checkout/webhook, owner entitlement, cancellation, failed payment, retry, duplicate events, expiry/refund/dispute behavior before live activation.
4. Confirm accepted backup responder and coverage, written external synthetic pilot scope, independent hosted account/mobile acceptance, finalized commercial/privacy terms and business readiness.
5. Launch only the reviewed bounded service after evidence closes the applicable gates. Existing founder Q28-A tablet-alert receipt in issue #80 remains valid within its scope; do not repeat completed baseline CI or source recovery.

No whole-pilot readiness claim or external permission is created by this checkpoint.
