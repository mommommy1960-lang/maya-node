# Synthetic network-scale pilot selection — 2026-11-07
Founder priority: accelerate practical food-rescue coordination; use sandbox to test many organizations, select the strongest evidence-based operating scenarios, then present only the best verified results. No real pantry partnerships, shipments, data, or charges are implied.

## Candidate scenarios to compare
1. **Urgent surplus rescue:** expiring produce at donor A, verified capacity at recipient B, available truck, both approvals.
2. **Freezer capacity recovery:** recipient freezer full or stale; discover alternate confirmed capacity; do not promise unverified storage.
3. **Truck sharing / contention:** multiple opportunities compete for same truck and window; no double booking, fair selection and expiry.
4. **Chain-of-custody exception:** 200 boxes loaded, 180 confirmed, 20 discrepancy; ask for evidence, no automatic blame.
5. **No-response escalation:** primary authorized contact unavailable; consented backup and deadline; no real messages until connected and approved.
6. **Commercial sandbox:** transparent logistics quote and agreement, simulated payment, cancellation/refund; no real billing.

## Evaluation rubric (synthetic only)
- Safety gates: zero unauthorized dispatch, double booking, spoiled food approvals, or unverified cold-chain claims.
- Reliability: original repo tests, browser module import, concurrency/restart scenarios, and verified CI.
- Value: matched useful food units, avoidable delay, coordinator steps, human response burden, discrepancies resolved.
- Practicality: simple mobile workflow and minimal partner onboarding.

## Recommended first public-facing *demonstration*, after verification
Urgent surplus rescue plus freezer-capacity check, with shipment reconciliation and human approval shown in a 60-second fictional scenario. This illustrates value without claiming real-world outcomes.

## Status
Scale test file `prototypes/pantry-watchtower/network-scale.test.mjs` drafted in PR #109 to simulate 30 pantries, 300 offers, 40 vehicles, and 100 shipment reconciliations. Tests are not yet independently verified; check GitHub CI and fix failures before reporting success. No launch authorization.
