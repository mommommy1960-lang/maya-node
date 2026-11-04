# Maya hosted guided demonstration — November 4, 2026

The founder selected the Morning Sky blue design and authorized publication to the existing Maya demonstration site.

Live site: https://maya-working-workflow-lab.myqueen1960.chatgpt.site

Published Sites version: 21. Source commit: 40b819fa543bf85273b795eb13e505b839234c0f (the separate Sites source repository, not a commit in this GitHub repository).

## Result

One Try the demo button leads to a real, fictional-data workflow: save a sample note, review its exact text, grant five-minute permission, create or revoke, and inspect a plain-language receipt. The original fingerprint and orbit animation remain. The full workspace sits behind My records. The page distinguishes ChatGPT sign-in from separately connected Maya tools, and explains what this release does and does not prove.

## Verification

- 102 existing automated checks passed after installing the locked dependencies; production build passed.
- Published browser: prepare, authorize, create, download. The 195-byte output exactly matched reviewed content; SHA-256 ce612d7931da1be0087a43c9e165ea6534e4a4561c371451202e058d677d03ec.
- Separate published browser request: prepare, authorize, revoke, attempt creation. Server refused with permission_revoked and saved a blocked receipt.
- Completed and revoked requests remained in the full workspace after page reload.
- Existing backend permission logic, public audience and storage bindings were retained. No payment capability was enabled.
- Managed preview browser routing refused the connection; published browser checks were used instead. A new mobile viewport check and native print-dialog check were not performed.

## Boundaries

The file demonstrates execution-time permission checking. It is not proof of invoice integration, stopped financial losses, independently signed audit evidence, or production readiness for customer data or payments. Receipt export includes currently retained account records; deletion removes linked receipts.

Local exported-snapshot recovery was tested separately. Hosted database restoration and provider backup/log retention remain unresolved. No production snapshot restore was attempted. Earlier hosted deletion and download checks remain historical evidence; they were not repeated for this design-only change.
