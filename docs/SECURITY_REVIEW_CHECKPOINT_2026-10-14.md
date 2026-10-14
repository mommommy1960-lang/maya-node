# Security review checkpoint — October 14, 2026

This is a bounded review of the public contact site and Maya Node payment/mail worker, not a penetration-test certification or a guarantee against compromise. Other public repositories and account-level settings have not received a complete audit.

## Implemented and verified

- Contact site version 7 deployed successfully: per-page Content Security Policy hashes restrict inline scripts/styles; browser connections, object embeds, forms and base overrides are blocked; referral information is suppressed. These are browser controls, not a WAF, authentication system or network firewall. Frame-ancestor protection requires HTTP headers and is not established by a meta tag.
- PR62 replaces full-body buffering with byte-limited streaming for Stripe webhooks (262144 bytes) and authenticated controller requests (24000 bytes). Invalid lengths and malformed UTF-8 are rejected; excessive streams are canceled. Raw valid text remains unchanged for signature verification.
- 22 local Node test entries passed, including six new request-limit regressions. The new hosted payment-worker security check passed at c1c76557a7af4844bc1c74479a7741ede0610341. Deployment/build status must be checked separately.
- Existing regressions passed for signed payment events, paid/live/allowed-link/USD2500 restrictions, duplicate-event handling, ambiguous delivery requiring review, dispatch races, header injection and disabled email.
- SEND_ENABLED remains false in the committed worker configuration. No live worker configuration or deployed runtime state is certified here.
- Existing inspected Maya Node workflows use pinned action commits and contents-read permissions; the new payment workflow also disables retained checkout credentials and has a five-minute timeout.

## Documented failures and applicable defenses

| Primary evidence | What failed or abuse pattern | Applicable defense and present limit |
| --- | --- | --- |
| [NASA OIG IG-19-022](https://oig.nasa.gov/docs/IG-19-022.pdf), June 2019 | Incomplete asset inventory and insufficient partner-access segmentation contributed to exposure; compromised external access enabled unauthorized mission-network access. | Inventory domains, accounts, deployed workers, databases, tokens and responsible owners; isolate public demos from private research and production customer data. Full inventory/access audit remains open. |
| [AWS security investigation](https://aws.amazon.com/blogs/security/cryptomining-campaign-targeting-amazon-ec2-and-amazon-ecs/), December 2025 | Compromised customer IAM credentials with broad privileges enabled cryptomining. This was not proof of an AWS platform breach. | Least privilege, temporary credentials, MFA/passkeys, credential revocation, usage alerts and service quotas. Account settings and budget controls remain unverified. |
| [GitHub supply-chain protections](https://github.blog/security/supply-chain-security/disrupting-supply-chain-attacks-on-npm-and-github-actions/) | Malicious packages/actions can expose tokens and compromise builds. | Pin actions, limit tokens, separate untrusted PR execution from secrets, inspect dependency changes. Pinning is not proof pinned code is safe; complete dependency audit remains open. |
| [Stripe card-testing guidance](https://docs.stripe.com/disputes/prevention/card-testing) | Automated attempts test stolen cards, often across many identities/IPs. | Hosted Checkout, layered processor fraud controls, request/attempt limits, alerting and manual review. Processor settings are not inspected or changed here. |
| [Stripe webhook guidance](https://docs.stripe.com/webhooks) | Forged, duplicate and out-of-order events can cause false fulfillment or repeat delivery. | Verify raw signatures; validate exact paid event; deduplicate by order; require manual review after uncertain delivery. Existing local regression tests pass. |
| [Cloudflare trial-abuse discussion](https://developers.cloudflare.com/turnstile/tutorials/fraud-detection-with-ephemeral-ids/) | Automated account creation and rotating identities undermine email-only trial eligibility. | Email verification is not proof of a unique person. Any scarce live session needs verified organization eligibility and an operator ledger; a future paid-compute trial needs server-enforced expiry/quotas and layered abuse checks. Neither is activated on the current browser demo. |
| [FTC free-trial guidance](https://consumer.ftc.gov/articles/getting-and-out-free-trials-auto-renewals-and-negative-option-subscriptions) | Unclear renewal terms and unauthorized charges generate complaints and chargebacks. | Keep the current demo free and the $25 review a separate affirmative purchase. No automatic conversion. Terms/refund/service scope need professional review; disclaimers do not replace controls or waive statutory rights. |

## Trial policy boundary

The existing self-guided browser demonstration has no trial login and no metered AI backend. Repeated visits therefore do not create a hosted AI-compute allowance. This does not eliminate hosting traffic or staff-time costs.

A one-hour staffed trial is not launched. Before launching it, publish its scope and eligibility, track bookings against a verified organization, restrict operator time, enforce any server expiry and quotas, and provide a review path for legitimate shared organizations/networks. Email, IP address and cookies alone cannot reliably establish a unique person. Do not collect government IDs or intrusive device fingerprints by default.

Do not upload private research, credentials, medical/student/banking records or other sensitive customer data to the demonstration. Public records and labeled test grants do not establish production customer authorization.

## Open verification gates

1. Account MFA/passkeys, recovery protection, active sessions and collaborator access across GitHub, Gmail, domain registrar, hosting and Stripe.
2. GitHub classic branch protection and secret scanning/push protection. Ruleset read returned an empty list; classic protection is not established, and this connector lacks administrative control.
3. Live Cloudflare worker build/deployment, production bindings, mail-disabled status, WAF/rate limits, spend alerts and request timeouts. Code merge is not a deployment claim.
4. HTTP security headers, public-site visual/browser behavior under the new CSP and independent traffic/abuse tests.
5. Dependency review, secret/history scanning and access audit across the other public repositories.
6. Private encrypted backup and a tested restore; incident owner, credential-revocation and customer-notification procedure.
7. Clear service scope, affirmative purchase, refund/cancellation, privacy/data retention, acceptable-use and IP/license terms reviewed for the actual business/jurisdiction; insurance and registration are separate gates.

The adviser/business checklist follows these security gates, as requested. No registration, certification, advisor endorsement, legal sufficiency or universal security guarantee is claimed.
