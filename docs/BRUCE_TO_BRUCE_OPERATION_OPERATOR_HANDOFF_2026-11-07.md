# Bruce-to-Bruce continuation: Maya Operation Operator — 2026-11-07

## Where to resume
Founder wants a continuously operating pantry-to-pantry logistics operator, a 24/7 "best buddy" that alerts authorized pantry personnel, follows up, and coordinates inventory, needs, freezer/storage capacity, trucks, schedules, human approvals, agreements, service quotes, and eventually payments. The goal is measurable reduction in preventable food waste and unmet needs. Do not claim universal elimination of hunger or automatically accuse "bad actors"; discrepancies trigger evidence-based human review.

## Durable work items
- #76: customer pilot readiness gates; real data/live billing NO-GO pending verification.
- #94: authorization/human approval/audit engineering controls.
- #105: pantry survey and translation staging.
- #108: synthetic Great River watchtower requirements.
- #110: commercial service quote/agreement/sandbox payment requirements.
- Draft PR #109: branch `feature/pantry-watchtower-synthetic-2026-11-07`.

## Actual code on draft branch (not merged/deployed)
- `prototypes/pantry-watchtower/matching.mjs` + `matching.test.mjs`: proposal-only food matching, freshness/cold chain/storage/vehicle constraints, duplicate event handling.
- `alerts.mjs` + `alerts.test.mjs`: consent-gated escalation planner, no real sending.
- `watchtower.mjs` + `watchtower.test.mjs`: synthetic matching + alert view integration.
- `demo.html`: standalone mobile-responsive fictional operations board, 3 fictional pantries, 2 fictional vehicles, 20 fictional offers; step-through capacity/transport changes; not wired to backend.

## Critical accuracy
Code was committed to GitHub, but tests have NOT yet been executed/verified; CI, deployment, Android browser testing and backend integration not established. Demo uses local sample logic and is NOT connected to `watchtower.mjs` or real pantries. No actual 24/7 task, alert delivery, trucks, customer payments or partner contracts were created. Do not say "live" or "customer-ready."

## Next engineering steps
1. Execute Node tests and correct failures; record actual output and CI status.
2. Reconcile demo rules with canonical matching module, add accessibility and scenario tests.
3. Implement durable event persistence and authorization/approval state machine; fail closed.
4. Simulate quotes/agreements and Stripe sandbox only; no live billing.
5. Confirm hosted deletion, backups/recovery, incident backup owner, written pantry permission and security/legal responsibilities before real pilot.
6. Update this handoff with links to exact evidence and completed checks, not promises.

## Scope/permissions
Founder authorizes continuing development, NOT production deployment, real-world outreach, real charges, or use of real customer data without the appropriate gates and approval. Preserve existing project and founder decisions.
