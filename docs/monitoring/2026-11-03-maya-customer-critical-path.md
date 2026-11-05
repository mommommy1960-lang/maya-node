# Maya customer critical path — 2026-11-03

Scope: evidence review of main-branch `docs/MAYA_READINESS_EXECUTION_2026-10-28.md`, `docs/MAYA_DELETION_AND_RECEIPT_COMPLETENESS_TEST_PLAN_2026-10-25.md`, issues #76 and #80. This is a review/checklist, **not** a fresh hosted test.

## Existing verified baseline
- v18 demonstration deployment and 87 automated tests are documented in issue #76; isolated local workerd/D1 checks and the 18-case matrix are recorded in readiness execution.
- DEL-07 is partial/blocked on backup/log expiry and hosted recovery; local D1 rollback is not hosted recovery.
- Prior hosted verification and current isolated tests are not a new hosted two-account deletion/reload test.
- Existing system is a bounded exact-text-file service, not a general autonomous business agent, payment processor or production customer platform.

## Minimal safe hosted acceptance session (requires access and a disposable synthetic account)
1. Record actual hosted URL, deployed revision, identity, time, and whether environment is production/demo/staging. Avoid touching existing customer records.
2. Create one disposable synthetic request, grant exact scope, execute, download output and receipts; compare bytes, hash, receipt linkage; reload and export again (REC-01/10).
3. Delete only that synthetic request; reload and re-query request/output/receipts; verify absence in active storage and unrelated synthetic request survival (DEL-01/06/08). Distinguish active deletion from backups/logs (DEL-07).
4. With a separate consenting synthetic account, verify cross-account read/export/delete denial (DEL-03/REC-09). Do not perform destructive faults on production.
5. Record actual results, revision, timestamps, redacted evidence and explicit failures. A completed test is not equivalent to customer launch permission.

## Operational blockers requiring external evidence
- Provider response to support case 17489131: backup/PITR/log retention and isolated synthetic restore, including deleted-record non-resurrection.
- Consenting named backup responder, coverage hours, escalation contact and a documented safe handoff drill. Founder primary is previously recorded, backup not.
- Alert receipt on actual device, if relied on for incident response; no assumption from task execution alone.
- Written business pilot scope/permission, participant identities, synthetic-only rules, feedback capture. Existing issue #80 permits synthetic-only pilot preparation, not real data.
- Cloudflare Workers Build exact failed command/logs before configuration change; no guess-based binding changes.

## Go/no-go
Synthetic-only demonstration/pilot preparation: conditional GO within existing permissions. Real customer records, consequential processing, billing and production launch: NO-GO pending the above evidence and founder release decision. BPI 2019 full-dataset benchmark is independent and must not be treated as the sole customer launch blocker. Do not merge PR #98 or alter production as a shortcut.
