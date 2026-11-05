# Austin / Iron & Ember: bounded Maya Node v18 technical review plan
Date: 2026-11-03
Status: PROPOSED ONLY — not executed, not externally shared, no access granted.

## Objective
Produce one reproducible, independently inspectable result for Maya Node v18's hosted deletion/authorization/receipt workflow, comparing actual server-side state to receipts. No claims of certification, compliance, or production readiness.

## Scope and preconditions
- Synthetic records and dedicated disposable accounts only. No customer, employee, payment, or other confidential data.
- Written consent from each participating party, named testers, exact hosted environment, timeframe, permitted endpoints and rate limits, incident contact, confidentiality and intellectual-property boundaries.
- Keep customer Site separate from optional Cloudflare Worker staging; never assume they share deployment, data, or revisions.
- Record exact deployed source/build SHA, release ID, sanitized architecture, endpoint descriptions, and receipt schema. No secrets.
- Confirm test environment isolation, backups/retention behavior, recovery procedure, and authority to delete synthetic test data before execution.
- No external account credentials or admin access until scoped written agreement and owner authorization.
- No production fault injection, real billing, cross-account probing outside controlled test accounts, or destructive restore.

## Test matrix
1. Authorized synthetic deletion: create disposable owned record, capture pre-state, authorize deletion, query server-side state afterward; record deletion receipt.
2. Revoke before dispatch: authorize then revoke before execution; prove no side effect and compare denial receipt.
3. Ownership isolation: two controlled accounts A/B; prove B cannot read, delete or authorize A's record; inspect safe denial evidence.
4. Delayed execution: hold synthetic action until after permission expiry/revocation; verify it does not execute.
5. Restart/replay: repeat request after restart/timeout under approved isolated environment; verify idempotence, no duplicate side effects.
6. Receipt integrity: compare server-side state, exact action ID, authority, time and result to receipt; reload and verify persistence, without exposing sensitive payload.
7. Cleanup/retention: verify only expired disposable records removed; avoid touching legacy or customer records.
8. Backup non-resurrection: isolated synthetic restore only after provider recovery and retention guarantees are documented; otherwise mark BLOCKED.

## Evidence template per test
Test ID; environment URL (sanitized); source/build SHA; tester and written authorization; synthetic account labels; request/action IDs (redacted); initial server state; action steps; final server state; receipt/denial contents (sanitized); reload results; timestamp; pass/fail/blocked; reproducibility notes; limitations.

## Existing evidence and gaps
GitHub issue #76 documents 87 automated v18 tests and local D1 integration, plus deployment evidence. It explicitly does not establish fresh hosted end-to-end deletion, receipt persistence, isolated recovery, backup retention, or external peer review. Issue #80 authorizes only a bounded synthetic pilot, not real customer data or live billing. Maya maintenance status read Nov 3 shows a persisted cleanup run and zero pending expired requests; this is not a hosted deletion/restore test.

## Exit gates
A review is complete only when tests actually run with reproducible evidence and a signed/dated peer feedback record. Any missing permission, source revision, access, isolated environment or provider recovery evidence must be marked BLOCKED, not PASS. Real customer processing and live billing remain NO-GO until all production gates are separately verified.

## Reciprocal Pulpo review
Optional separate written agreement: critique consent, delegation, revocation, human authority boundaries; each team retains its own IP. No implied partnership or source sharing.

## Next authorized action
Share this proposed written plan with Austin for scope discussion after founder review. Do not execute tests or send it without approval.
