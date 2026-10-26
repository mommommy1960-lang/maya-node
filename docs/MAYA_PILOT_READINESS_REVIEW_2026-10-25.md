# Maya Node Pilot Readiness Gate Review — 2026-10-25

This review distinguishes prior documented evidence from checks re-run during this review. It does not certify production readiness.

## Gate status

| Gate | Status | Evidence / remaining work |
|---|---|---|
| 1. Verify hosted deployment and exact end-to-end path | **Previously documented; current re-verification blocked** | The October 16 hosted verification record documents sign-in, exact authorization, saved output, byte-exact download, revocation blocking, persistent receipts, and receipt download. On October 25 the hosted URL could not be opened through the available verification channel, so current uptime and current deployment state are not independently confirmed. Repeat on founder's Galaxy tablet and capture a fresh receipt. |
| 2. Customer-controlled record review and deletion | **Open** | The October 16 service-test record says deletion is covered by a service test. That is not the same as confirming a customer can review and delete records through the live UI and verify associated output/receipt removal. Complete the full hosted UI test. |
| 3. Data minimization, access, retention, deletion, incident contact | **Partial** | Existing public evidence says use non-sensitive text, records are identity-scoped, text persists until owner deletion, deletion removes request/output/receipt history, and the operator has database access. There is no automatic retention/SLA guarantee. Before live customer data: publish a concise pilot privacy notice, name a monitored incident contact, define retention/deletion timing, support access controls, and explain incident reporting. |
| 4. Authorization, revocation, duplicate, failure, receipt-completeness tests | **Partially evidenced; rerun required** | The October 16 hosted verification record reports 17 service tests covering revocation, expiry, replay/concurrency, owner isolation, authentication/storage failure, CSRF, input bounds, deletion, and receipt-insertion rollback. Older local tests also cover real file writes and revocation. The current test suite was not rerun as part of this review; add/verify an explicit receipt-completeness assertion and retain fresh CI evidence before pilot. |
| 5. Named human owner and escalation route | **Not finalized for pilot** | Founder is project owner, but a pilot-specific on-call/backup contact, response expectations, and escalation procedure are not documented. Name them in writing before the pilot. |
| 6. Written scope and explicit business permission | **Not started** | No pilot business is confirmed in this review. Do not process live business data or imply customer approval. Obtain signed/recorded scope and explicit permission. |
| 7. Synthetic/redacted data first | **Required before any pilot** | Use synthetic or redacted content until all gates above pass. Do not place real customer or sensitive data in the current early-access workflow. |
| 8. Baseline and outcome record | **Not started** | Define baseline workflow time, error/rework rate, authorization coverage, receipt completeness, and owner feedback before pilot; report actual results including failures. |

## What was independently checked in this review

- Read the repository's October 16 hosted verification record, local file-action record, and public due-diligence page.
- Confirmed GitHub Actions workflow Security & Ethics Checks completed successfully for documentation commit 097db19e352ddcd052a61e72bb5168ff1819e964. This is a documentation/security-ethics workflow result, not proof that all pilot readiness tests ran.
- Attempted to open the hosted site through the available browser verification channel; the site was not accessible through that channel. This is not proof that the site is down; current deployment status remains unverified.

## Next execution order

1. Founder performs hosted workflow and deletion checks on the Galaxy tablet; capture fresh non-sensitive evidence.
2. Inspect and run the current test suite; add explicit receipt-completeness coverage if absent.
3. Write the pilot privacy notice and incident/escalation protocol; name primary and backup human owners.
4. Only then recruit/confirm one design partner and get written scope and permission.
5. Run the pilot with synthetic/redacted data, record baseline and results, and only consider live data after all gates pass.

## Outreach

The outreach message remains a draft. No email was sent by this review: an authenticated mailbox and verified recipient addresses were not available in the current session. Appropriate first contacts are the already documented business-advising/reviewer threads, not a mass email. Ask for a short discovery/review conversation; do not claim a customer pilot or independent endorsement.
