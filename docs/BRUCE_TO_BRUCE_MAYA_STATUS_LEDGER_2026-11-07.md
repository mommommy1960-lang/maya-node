# BRUCE-TO-BRUCE — Maya Node status ledger (2026-11-07)

## Latest verified engineering checkpoint — November 7, 2026, 4:04 PM Pacific

- **Synthetic CI: 51 tests passed, 0 failed, 0 skipped** on commit `614a2fa80f1d42694229a20d1e76addad7f8091c`; [GitHub Actions run 42428111068](https://github.com/mommommy1960-lang/maya-node/actions/runs/42428111068), [job 128570712198](https://github.com/mommommy1960-lang/maya-node/actions/runs/42428111068/job/128570712198). Checked actual Node test job log; this supersedes the historic 30/45-test baselines below. Source code preceding the final regression-test-only commit also passed the [Security & Ethics Checks run 42428103904](https://github.com/mommommy1960-lang/maya-node/actions/runs/42428103904).
- **Critical synthetic integrity fix:** corrected a path that previously allowed `release()` or `expire()` to release one hold inside a multi-resource food/freezer/truck reservation while other holds remained active. Bundle membership now uses an explicit foreign-keyed `bundle_holds` table, not ID-prefix matching. Bundle expiry returns capacity as a group, and stale bundle approval checks fail. For file-backed synthetic SQLite, enabled WAL and foreign-key enforcement.
- **Six new synthetic regression tests** cover release isolation, atomic expiry, idempotency after expiry, restart reclamation, ordinary single holds, prefix isolation, and unmapped legacy-data fail-closed behavior (six cases, bringing 45 → 51).
- **Migration limitation:** older test database files with legacy unlinked bundles are deliberately refused rather than silently released or approved. No live database migration or external data changes were attempted. A reviewed migration strategy remains necessary before these patterns could be productionized.
- **Still unverified:** real browser/Android journey, persisted order state atomically coupled to reservations, verified human permissions and action-digest approvals, hosted deletion and isolated restore, legal/partner permissions, real payment flow and operational coverage. **NO-GO for real customer data, real dispatch, external messages and live billing.**
- **Next highest-impact task:** persist the synthetic order lifecycle and tie every approval to an active, unexpired bundle with transactional state changes, recovery and denial tests. Continue toward 24-hour readiness snapshot and 3–7 day synthetic demonstration deadlines, not a promised release.

## Founder instruction
When founder asks "Bruce, what's the tea? Where are we at?", read this ledger, latest PR #109, issues #76/#94/#105/#108/#110/#111, current GitHub Actions, and subsequent handoffs. Report verified progress, blockers, next action, and go/no-go. Do not confuse a successful CI run with customer readiness. Keep synthetic-only gates until explicit founder approval and verified external controls.

## Verified engineering evidence
- Development branch: `feature/pantry-watchtower-synthetic-2026-11-07`; draft PR https://github.com/mommommy1960-lang/maya-node/pull/109
- GitHub Actions on head `3652cf650d528674b35f043a57462f7c9936ee9d`: Pantry watchtower workflow run **42424175778**, job **128558775510**, 30 Node tests passed, 0 failed, 0 skipped. GitHub job logs inspected; includes network-scale scenario of 30 fictional pantries, 300 offers, 40 vehicles and 100 shipment reconciliations. This is a synthetic test workload, NOT a real capacity benchmark.
- Security & Ethics Checks run **42424175695**: successful.
- Synthetic code: `matching.mjs`, `alerts.mjs`, `watchtower.mjs`, `reconciliation.mjs`; no live dispatch or payment. Watchtower now limits duplicate offer/need/truck assignments within a single planning snapshot; no durable atomic reservations yet. Reconciliation preserves valid later receipts after invalid earlier receipts. CI regression tests cover both.
- `knowledge-gates.mjs` and tests: distinguish licensed public background research from fresh authorized operational inventory.
- `network-scale.test.mjs` and `safety-regressions.test.mjs` included in 30-test run.
- `demo.html` uses ES module imports, but actual browser interaction has NOT been independently verified.
- Competitor landscape saved in `docs/MAYA_COMPETITOR_LANDSCAPE_2026-11-07.md`: MealConnect, Food Rescue Hero, Food Rescue US, Goodr, Spoiler Alert, Share My Meals. Gaps are hypotheses, not proven rival omissions.
- Execution roadmap saved in `docs/MAYA_COMPETITIVE_ACCEPTANCE_AND_FIVE_STAGE_EXECUTION_2026-11-07.md`; network scenario selection in `docs/MAYA_SYNTHETIC_NETWORK_SCENARIO_SELECTION_2026-11-07.md`.
- Logistics roadmap issue #111; synthetic watchtower #108; commercial flow #110.

## Five next gates
1. Persistent atomic inventory, receiving-space, and vehicle/time-slot reservations; idempotency, expiry, cancellation, race/restart tests.
2. Permissioned order state machine, human approvals, immutable audit and delivery receipts, corrections.
3. Sandbox quote/payment/refund/webhook replay rehearsal; no live charges.
4. Actual browser-tested accessible full synthetic journey and failure recovery.
5. Hosted deletion and backup restore proof, named escalation, partner permission, operational/legal review and narrow pilot approval.

## Readiness decision
**NO-GO** for real customer data, real messages, dispatch, live billing, or claiming production-ready. Passing synthetic CI is progress, not launch clearance.

## Reporting protocol
When asked for the tea, provide: (a) latest verified passing test count and run, (b) latest commits/PRs, (c) what actually works, (d) top unresolved blocker, (e) next testable milestone, (f) real customer/live billing go/no-go. If later evidence supersedes this ledger, use the newer evidence and update the ledger. No invented deployment, live customer, or partner permission claims.
