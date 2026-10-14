# Maya Node software delivery — October 14, 2026

Mya P. Brown is the founder. Maya Node is the software performing the supported
work. This replaces the old human-review product direction; it does not activate
or retroactively change historical purchases.

## Implemented and tested locally

`software_access.py` is a server-only, persistent SQLite access core. A verified
account gets a single 3,600-second trial. Restarting or concurrent start requests
cannot extend it. Access is evaluated on every protected operation. Verified
orders are customer-bound and idempotent; recorded refunds/revocations also block
late payment events from resurrecting an order. Suspended accounts are denied.

Run from this directory: `python -m unittest discover -s tests -v`.
Observed October 14: **10 tests passed**. This is local validation, not deployed
service, hosted CI, security certification, or an end-to-end purchase test.

## Required adapters and open decisions

1. Verified sign-in and a stable server-side subject. An email string or browser
   cookie alone does not establish trial eligibility or prevent multiple accounts.
2. Deployable server and durable database. The current contact Site is static and
   has no configured runtime environment. This SQLite implementation needs a
   Python host, or a reviewed port to the hosting provider's database API.
3. Connect the trial to the actual supported Maya operations and check access on
   every server request. A client-side timer alone is bypassable. Current browser
   demonstrations use invented records and are not live customer integrations.
4. Create/configure a **software** Stripe product, price and checkout session.
   The historical $25 review link must not grant software access. The founder has
   requested paid software at $25, but paid duration and recurring versus one-time
   terms are not yet settled. Do not invent a monthly subscription or charge.
5. Verify raw webhook signatures, exact price/product, currency, paid status,
   account/mode, and a server-created order-to-subject mapping before invoking
   `grant_verified_order`. A browser success redirect is not payment evidence.
6. Authenticated refund/dispute/cancellation handling, protected administrative
   suspension, request quotas, abuse controls and reconciliation for uncertain
   payment delivery. No application mail sending is enabled by this change.
7. End-to-end sandbox purchase, expiration, refund, replay and cross-account tests;
   then a production release with published access terms and support/refund path.

## Existing routes

Current demo: https://civic-continuum-contact.freshcoin8.chatgpt.site/demo.html

Legacy human-review site:
https://maya-node-founding-review.myqueen1960.chatgpt.site
It is not editable through the current Sites account. Its purchase links have
been removed from the corrected contact/demo pages; that is not proof the legacy
site or its checkout has been disabled.

No checkout, customer charge, hosted entitlement or live Maya service is activated
by this preparation. Next release must connect verified identity, payment and
Maya execution rather than advertising a working subscription prematurely.
