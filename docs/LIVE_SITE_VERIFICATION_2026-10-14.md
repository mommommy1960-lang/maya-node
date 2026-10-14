# Live contact-site verification — October 14, 2026

Checked the public production URL https://civic-continuum-contact.freshcoin8.chatgpt.site/ after version 7 publication.

- Deployment status: succeeded.
- All six HTML pages and three assets returned HTTP 200 after following canonical URL redirects.
- All nine delivered files exactly matched the published source.
- CSP script/style hashes matched the actual delivered blocks on all six pages.
- 32 internal links/assets had valid local targets; all corresponding published files were retrieved successfully.
- 36 interaction assertions passed against scripts extracted from the live responses in a DOM test harness: four sector selectors, permitted reads, export denial, revocation denial, correction, correction not restoring revoked permission, reset, native-share invocation, clipboard fallback, permission-denied fallback and canceled-share handling.
- Linked Founding Review landing, intake and support pages returned HTTP 200. No purchase was submitted and checkout/payment fulfillment was not tested.
- Contact file had BEGIN:VCARD/END:VCARD delimiters. QR and logo downloads matched source; camera scanning was not tested.
- Site worker error-log query returned no events for the previous 30 minutes; this is not proof there were no client errors.

Limits: no supported rendered-browser QA capability was available. Visual/mobile layout, actual OS contact import, native share/clipboard permissions, camera scanning and external third-party page functionality were not verified. DOM harness assertions do not certify browser CSP enforcement. The contact site's successful deployment does not verify the separate Maya Node Cloudflare worker build or live payment/mail runtime. That separate build failed; PR62 code was merged after passing local and hosted security tests.
