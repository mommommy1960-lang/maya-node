# Maya Node — Deletion and Receipt-Completeness Test Plan
**Prepared:** 2026-10-25  
**Purpose:** Close the specific readiness gap without duplicating the passing general CI suite.

## Evidence baseline

The historical hosted verification record dated 2026-10-16 reports 17 service tests using SQLite transactions, including deletion and rollback when receipt insertion fails. It also says deleting a request removes its associated output and receipt history. This is useful prior evidence, but it is not a fresh test run and does not establish that the current hosted customer UI exposes and correctly completes deletion.

The current CI run at https://github.com/mommommy1960-lang/maya-node/actions/runs/40255591764 passed five configured jobs. Its workflow file runs Python runtime/ledger tests, adversarial suites, Bandit, and ethics checks. It does not exercise the hosted customer deletion journey.

## Test safety and setup

- Use a dedicated disposable test account and synthetic text only.
- Never run destructive tests against real customer records.
- Record commit SHA, environment, test account identifier (non-sensitive alias), timestamp, result, and redacted evidence.
- Do not treat a UI success message alone as proof of deletion. Verify the server-side request record, output payload, and receipt history are absent for that request, using authorized test-environment inspection.
- Verify ownership boundaries: one test user cannot inspect or delete another user's request, output, or receipt.
- Do not erase global security/audit events that policy or law requires retaining. If such events remain, document their scope, purpose, access control, and retention separately from user-visible request receipts.

## A. Customer-controlled deletion cases

| ID | Scenario | Required pass condition |
|---|---|---|
| DEL-01 | Delete an owned request with a saved output and receipt history | UI confirms the specific target; request, linked output, and user-visible receipt history are removed from active storage; unrelated requests remain |
| DEL-02 | Delete a request with no output (denied/revoked action) | Request and associated user-visible receipt history follow the documented deletion policy; no output exists |
| DEL-03 | Attempt to delete another user's request by changing an identifier | Denied; no target data changes; safe denial event recorded without leaking target contents |
| DEL-04 | Repeat deletion for an already deleted/missing request | Safe, deterministic response; no unrelated deletion and no server error |
| DEL-05 | Force storage/transaction failure during deletion | Atomic behavior: either all in-scope records are removed or none are; no misleading success receipt |
| DEL-06 | Reload/re-query after successful deletion | Deleted request/output/receipt are not recoverable through normal customer UI/API paths |
| DEL-07 | Inspect documented backups/logs/derived copies | Retention and eventual purge behavior is documented accurately; do not claim immediate total erasure if backups or legally retained security events remain |
| DEL-08 | Verify unrelated request remains after deletion | Other owned requests, outputs, and receipts remain intact |

## B. Receipt-completeness cases

For each receipt, assert the required schema fields are present and internally consistent: unique receipt/request identifier; owner scope; action type; outcome (success, denied, revoked, failed, or human_handoff as applicable); authorization/grant reference; timestamps; reason/result code; output reference or explicit none; and correlation/idempotency key where applicable. Do not place secrets or full sensitive payloads in receipts.

| ID | Scenario | Required pass condition |
|---|---|---|
| REC-01 | Authorized successful file action | Receipt identifies the exact authorized request and output; recorded byte count/hash agrees with the produced payload where supported |
| REC-02 | Missing permission / denied action | Denial receipt exists; no output is created; reason is safe and specific enough to audit |
| REC-03 | Permission revoked before execution | Action is blocked; receipt says revoked/blocked; no output exists |
| REC-04 | Authorization expired | Action is blocked; receipt records expiry/denial; no output exists |
| REC-05 | Duplicate request / replay | Idempotent outcome or explicit replay denial; never create unintended duplicate output; receipt linkage remains unambiguous |
| REC-06 | Action/storage failure | Failure is recorded; no success receipt; partial output is rolled back or explicitly reconciled |
| REC-07 | Receipt write fails after action preparation | Transaction rolls back safely; no unreceipted successful action is left behind |
| REC-08 | Human handoff required | Receipt records handoff state and reason; does not claim action completion |
| REC-09 | Cross-user receipt access | Other user cannot read, download, or delete the receipt |
| REC-10 | Receipt download and reload | Downloaded receipt matches the stored receipt and remains tied to the correct request |

## C. Execution order

1. Inspect existing service/UI implementation and test fixtures before coding; map each case to existing coverage to avoid duplicate tests.
2. Add missing automated service tests in the correct test suite. Run targeted tests first.
3. Run the relevant GitHub Actions workflow and retain its URL and job logs. A test plan or code change is not a test result.
4. On the hosted staging/test environment, run DEL-01 through DEL-08 with the disposable account and verify server-side state.
5. Run REC-01 through REC-10 and inspect receipt fields and output linkage.
6. Update the execution record with actual pass/fail/skipped results, commit SHA, and evidence. Leave a case OPEN if the environment or permissions prevent testing.

## Acceptance gate

Deletion and receipt-completeness are **not passed** until the relevant tests have actually executed and results are recorded. Historical tests and general CI are supporting evidence only. Keep live customer data out of scope until hosted deletion, access isolation, retention policy, incident contact, and pilot authorization are verified.
