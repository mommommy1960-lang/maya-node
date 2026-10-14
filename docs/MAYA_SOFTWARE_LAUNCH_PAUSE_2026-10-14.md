# Maya Node software launch — pause and resume
Updated October 14, 2026, 10:20 AM Pacific. Prepared for Civic Continuum's public review routes.

## Intended offer
| Setting | Proposed value |
|---|---|
| Product | Maya Node — 30-day software access |
| Price | $25 USD, one-time payment |
| Included | One account, 30 days, up to 100 bounded AI workflow-analysis replies |
| Renewal | No automatic renewal |
| Free trial | One hour or 10 replies, whichever ends first |
| Work performed by | Maya Node software; Mya P. Brown is the founder |

## Completed
- Existing contact Site migrated to the supported server runtime; Sites version 10 deployment succeeded.
- Existing branding, contact download, QR and public pages preserved.
- Added authenticated route mounting, persistent D1 schema/migrations, Maya customer page and service-scope page.
- 26 local tests passed, including checks that disabled launch blocks purchases and inference. Provider calls in this suite are simulated.
- Build and build-output secret scan passed. Hosted source commit: f311f64e59581e73c129548082ac87df93a081c4 in the Sites source repository.
- [Contact hub](https://civic-continuum-contact.freshcoin8.chatgpt.site) · [Maya page](https://civic-continuum-contact.freshcoin8.chatgpt.site/maya.html) · [Service scope](https://civic-continuum-contact.freshcoin8.chatgpt.site/maya-terms.html).
- [Runtime preparation PR #63](https://github.com/mommommy1960-lang/maya-node/pull/63) remains a draft; deployed Site source and this PR are distinct.

## Current blockers — no completed-service claim
| Area | Observed state |
|---|---|
| OpenAI API | Key authentication worked, but a real inference attempt returned billing_not_active. Billing activation was not completed. |
| Hosted provider secret | Local key exists securely; it was not installed on the hosted Site. |
| Stripe | Sandbox offer exists. Live reads work; new offer creation failed for missing connection write permissions, including after reconnect. No new live software product or price was created by these attempts. |
| Dashboard sign-in | Founder reached the Dashboard on her own device. The separate agent browser remained at email verification. A device sign-in does not establish the other browser's session. |
| Runtime payments | Restricted runtime key and verified webhook remain unconfigured. |
| Live checks | Direct test-client probes received HTTP 403 / Cloudflare 1010. This does not establish that ordinary visitors are blocked. Browser/mobile and purchase-to-reply verification remain open. |
| Launch | MAYA_LAUNCH_ENABLED remains false. Trial, real replies and checkout are disabled. |

Earlier references to a $25 human-delivered review are superseded for this software offer. Old review-service purchase links were removed from corrected pages; the inaccessible legacy service itself was not confirmed disabled. No live school/bank connection, external action, certification, adviser endorsement or completed registration is implied.

## Resume in this order
1. Reconcile any product the founder may have created manually before creating another.
2. Configure a sandbox restricted Stripe runtime key and signed webhook securely; never place secrets in source, screenshots or chat.
3. Complete API funding with the founder's approved amount; no automatic recharge by default. Verify the API key's organization/project and one actual reply.
4. Configure hosted secrets, then verify identity, persistent access, bounded trial and a real sandbox purchase-to-reply flow, expiry and refund/dispute revocation.
5. Finish abuse controls, failed-reply quota reconciliation, privacy and refund terms, and mobile button/link testing.
6. Configure and verify live payments, then enable launch only when the service delivers the advertised offer.

Paused at the founder's request. No customer charges or new adviser emails were sent during this pause update.
