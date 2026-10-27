# Maya cross-account isolation: evidence review and next execution gate (2026-10-27)

## What was inspected
GitHub files `docs/MAYA_HOSTED_ACTIONS_VERIFICATION_2026-10-16.md` and `docs/MAYA_DELETION_RECEIPT_COVERAGE_MAP_2026-10-26.md` state 17 historical local SQLite service tests included owner isolation, auth failures, CSRF, deletion, and rollback when receipt insertion fails. These are historical narrative claims, not fresh results from the current deployed app. They explicitly say a second real-user isolation test remains open.

## Actual current live evidence
The connected Maya interface `maya_list_requests` only accesses the signed-in owner's requests. Prior live checks verified owner-scoped draft and completed-file deletion. It offers no second-identity switching, cross-account inspection, deletion API, test-environment fault injection, or backup inspection. No second-account attack was performed here. DEL-03 and REC-09 remain OPEN.

## Two-account acceptance test (safe disposable accounts only)
1. Create separate consenting test identities A and B, distinct sessions, and synthetic files `isolation-a.txt`, `isolation-b.txt`. Capture non-sensitive IDs only.
2. With A's session, list/read/download A's records. With B's session, list/read/download B's records. Neither listing should include the other's entries.
3. Using B's authenticated session and A's disposable request ID, attempt owner-scoped read/download and delete through documented test API, without modifying production users. Expect safe denial and no leakage. Repeat A against B.
4. Check receipts for denied attempts and verify original A/B records intact.
5. Try logged-out access and stale session; expect denial. Verify post-refresh and preserve redacted evidence.
6. If no second-account access or documented test API exists, mark BLOCKED, not PASS.

## Other blockers
DEL-07 backups/retention, DEL-05 forced deletion failure, REC-06/07 fault injection require staging backend access and operator retention policy. Never run fault injection on live customer data.

## Status
Source inventory done; historical local coverage identified. No new cross-user test was executed and no hosted source code was modified. Next dependency is two consenting distinct test accounts and authorized staging/API access. Do not accept real customer data or charge for security assurances until gates pass.
