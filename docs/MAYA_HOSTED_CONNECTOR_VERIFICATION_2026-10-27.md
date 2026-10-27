# Hosted Maya Accountable Actions: direct connector verification
Date: 2026-10-27
Environment: Connected signed-in Maya Accountable Actions plugin (owner's workspace)
Scope: **Non-destructive**, existing synthetic test records. No database admin, second account, site editor, deletion API, or production changes.

## Executed and observed
1. `maya_list_requests({})` returned `signedIn:true` with 10 existing requests, request states and associated events. This verifies access to the current owner's workspace only; does not establish another user's isolation.
2. `maya_read_output({id:"59e598c3-0e81-4052-80bb-8c73f27e29b6"})` returned `peer-sample-a.txt`, text `Civic Continuum peer evaluation - sample A.`, SHA-256 `9b72c1ee6565693996699344e66997f3770c5c44e6572905f97423a914f4b268`. Hash matched the owner request listing.
3. `maya_read_output` for revoked synthetic request `a22947bd-fbe4-4f2a-83b4-d52e427dadb2` returned `File not found.`
4. `maya_read_output` for unapproved synthetic request `07e3db86-7598-4f86-a38c-5a1a7af66e0d` returned `File not found.`
5. `maya_prepare_text_file` prepared new harmless request `d3faef81-382d-4711-8f46-276a7abfcfe2`, filename `maya-gate-check-20261027.txt`, text `Synthetic test only. An unapproved request must not create an output.` No authorization was granted. An attempted `maya_execute_authorized_file` call was blocked by tool safety checks, **not** by a confirmed Maya service response. No retry.
6. Existing event history includes `created/current_exact_permission`, `blocked/permission_missing`, `revoked/owner_withdrew_permission`, and `blocked/permission_revoked`. These are observed historic records, not newly executed destructive cases.

## Case status (strict acceptance criteria)
| Case | Current status | Evidence/remaining gap |
|---|---|---|
| DEL-01 | OPEN | No customer delete action, database inspection |
| DEL-02 | OPEN | No delete action for denied/revoked request |
| DEL-03 | OPEN | No second account / cross-owner deletion attempt |
| DEL-04 | OPEN | No repeat-delete endpoint |
| DEL-05 | OPEN | No failure-injection environment |
| DEL-06 | OPEN | No deletion/reload to observe |
| DEL-07 | OPEN | No backup/log/retention evidence |
| DEL-08 | OPEN | No unrelated-record preservation test after deletion |
| REC-01 | PARTIAL | Existing completed file read-back and matching hash; receipt schema/output byte count unverified |
| REC-02 | PARTIAL | Prior blocked event and missing output; receipt schema unverified |
| REC-03 | PARTIAL | Prior revoked and blocked event, missing output; schema unverified |
| REC-04 | OPEN | No expiry execution test |
| REC-05 | OPEN | No replay execution test |
| REC-06 | OPEN | No failure injection |
| REC-07 | OPEN | No receipt-write failure injection |
| REC-08 | OPEN | No human handoff receipt |
| REC-09 | OPEN | No second-user access attempt |
| REC-10 | OPEN | Output read-back is not receipt download/reload comparison |

## Exact next dependencies
- Locate **hosted** app's source/export, deployment configuration and owner, plus a safe test environment. GitHub code search in `maya-node` did not find the hosted deletion implementation.
- Provide authorized staging test database inspection and a second consenting synthetic account.
- Implement or expose customer deletion controls if absent, then run DEL-01..08 and REC-01..10 with per-case output, logs, build SHA and timestamp.
- Confirm retention/backup purge policy, incident contact and backup owner; obtain written partner approval before customer pilot.
- Keep issue #76 OPEN. Do not mistake this record for passing 18 tests or for security certification.

**No customer data deleted, no payment, no website deployment.**
