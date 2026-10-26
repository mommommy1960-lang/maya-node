# Maya Node deletion and receipt coverage map — 2026-10-26

**Status: preliminary source inventory; not an execution report.** This document distinguishes what the repository's existing records say from what was independently inspected or run in this review.

## Evidence reviewed

- `docs/MAYA_HOSTED_ACTIONS_VERIFICATION_2026-10-16.md`: historical report of 17 local SQLite service tests, including deletion, owner isolation, revocation, expiry, replay/concurrency, CSRF, input bounds, missing authentication/storage, and rollback when receipt insertion fails. It also records a hosted authorized action, byte-exact output, revocation block, persisted receipts, and receipt JSON download.
- `docs/MAYA_DELETION_AND_RECEIPT_COMPLETENESS_TEST_PLAN_2026-10-25.md`: eight deletion cases (DEL-01–08) and ten receipt cases (REC-01–10).
- `docs/MAYA_FIVE_CHECK_STATUS_2026-10-20.md`: customer-controlled deletion and isolation are explicitly pending.
- `docs/MAYA_PILOT_READINESS_REVIEW_2026-10-25.md`: current hosted re-verification is blocked; retention/incident decisions and human escalation are unfinished.
- `docs/MAYA_PILOT_DATA_AND_INCIDENT_PROTOCOL_DRAFT_2026-10-25.md`: founder decisions remain placeholders.

## Case-by-case preliminary map

Legend:
- **Historical coverage reported** = older verification record says a related service test exists; source test name and current result were not confirmed here.
- **Not established** = no inspected evidence sufficient to mark the specific case passed.
- **Hosted re-test required** = historical hosted behavior does not establish current deployment behavior.

| Case | Preliminary mapping | Current disposition |
|---|---|---|
| DEL-01 owned request with output and receipt | Historical deletion service test reported; hosted customer UI deletion not verified | Hosted re-test required |
| DEL-02 denied/revoked request without output | Revocation blocking historically demonstrated; deletion behavior for this exact state not established | Not established |
| DEL-03 cross-user deletion attempt | Owner isolation service test reported historically; specific deletion attack/result not confirmed | Not established |
| DEL-04 repeat deletion / missing request | No case-specific evidence inspected | Not established |
| DEL-05 forced storage/transaction failure during deletion | Transactional service tests reported; deletion-failure atomicity not separately confirmed | Not established |
| DEL-06 reload/re-query after deletion | Receipt persistence after ordinary reload was historically demonstrated; post-deletion retrieval was not | Hosted re-test required |
| DEL-07 backup/log/derived-copy purge | Documentation identifies backup/retention policy as unresolved | Founder decision and implementation evidence required |
| DEL-08 unrelated record remains intact | No case-specific evidence inspected | Not established |
| REC-01 successful action receipt/output integrity | Hosted byte-exact output and saved receipt historically demonstrated | Historical evidence only |
| REC-02 denied action receipt/no output | Revoked-action receipt/no output historically demonstrated; missing-permission variant not separately confirmed | Partial historical evidence |
| REC-03 permission revoked before execution | Historically demonstrated | Historical evidence only |
| REC-04 authorization expired | Expiry service test reported historically | Fresh targeted result required |
| REC-05 duplicate/replay | Replay/concurrency service tests reported historically | Fresh targeted result required |
| REC-06 action/storage failure receipt | Missing-storage tests reported historically; full failure receipt schema not confirmed | Not established |
| REC-07 receipt write failure rollback | Explicitly reported historically | Fresh targeted result required |
| REC-08 human handoff receipt | No case-specific evidence inspected | Not established |
| REC-09 cross-user receipt access | Owner isolation service test reported historically; receipt endpoint-specific result not confirmed | Not established |
| REC-10 receipt download/reload consistency | Receipt JSON download and reload persistence historically demonstrated; equality of downloaded vs stored receipt not fully specified | Partial historical evidence |

## Next execution steps

1. Inspect the current test files and service implementation to obtain exact test names and functions for each historical claim. Do not infer a test name from a narrative report.
2. Add only missing service-level tests for gaps confirmed by source inspection.
3. Run targeted tests and the configured GitHub Actions workflow; record actual commit SHA, command/run URL, and pass/fail output.
4. Run DEL-01–08 and REC-01–10 against a dedicated disposable hosted account using synthetic text. Verify server-side state with authorized test-environment access; never test destructive behavior against real customer data.
5. Keep each case open if test access, a disposable account, or administrative evidence is unavailable.

## Current stop conditions

- No current hosted deletion test was executed by this inventory.
- No live account, deployment, database, or backup was changed.
- No new automated test was added or run by this inventory.
- Do not accept real customer data until deletion, isolation, retention, incident contact, and written pilot scope/permission are verified.
