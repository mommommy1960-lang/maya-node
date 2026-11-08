# Maya Node order-origin capacity conservation — November 8, 2026

**Scope: synthetic, unmerged PR #109, nonproduction, fictional data. Real pilot and billing: NO-GO.**

## Concrete defect and safety fix

The transactional order store previously checked that every mapped reservation hold agreed with the *current bundle signature*. It did **not** independently check that the bundle signature still agreed with the **original durable synthetic order signature**. A simulated database corruption that raised both a hold quantity and its bundle signature from 3 to 6 passed the old consistency check, even though only 3 units had originally been debited. Subsequent cancellation or a delivery receipt could have incorrectly credited 6 units, fabricating availability.

The `SyntheticOrderStore._mappedHolds` guard now cross-checks the source order's recorded offer/need, quantity, original resource items, bundle identity, deadline, timestamp and parties against the current order columns, signed bundle *record* and canonical mapped holds. Before pickup, each hold must have the **exact original expiration**, not an extended deadline. After pickup, each in-transit hold must have the expected `Number.MAX_SAFE_INTEGER` extension; unchanged pickup and full/partial delivery stay supported. A missing/corrupt source signature fails closed, and the existing SQLite write transaction rolls back all credits, approvals and receipt changes.

**These are internal consistency checks, not cryptographic signatures.** Database administrators or an attacker able to rewrite *all* related records could still forge internal state. This does not establish independent tenant identity, source inventory truth, or production tamper evidence.

## Fresh executable tests

Six new regressions in `prototypes/pantry-watchtower/order-origin-capacity-integrity.test.mjs`:
1. Coordinated bundle+hold quantity mutation cannot mint resources through cancellation or approval.
2. Coordinated bundle+hold deadline mutation cannot extend the original order deadline.
3. Malformed original order signature prevents release/approval and preserves allocations.
4. Changed post-pickup capacity cannot mint reusable truck/freezer slots through a delivery receipt.
5. Normal untampered pickup and receipt settle, retaining consumed food and returning only reusable capacity.
6. SQLite restart preserves fail-closed behavior after persistent bundle/hold corruption.

## Independent CI on tested source

- Tested code/test source: `080dafb21ae41906ba574734aa336c58b307e5fa` (source hardening `5e4ba42d5bb9f71fbc58823fc881dea4a4e2ccbf`).
- [Node Actions run 42478480686](https://github.com/mommommy1960-lang/maya-node/actions/runs/42478480686), job `128725006263`: **154 passed, 0 failed, 0 skipped** (TAP summary and six new cases inspected).
- [Chromium-to-loopback-to-SQLite Actions run 42478480733](https://github.com/mommommy1960-lang/maya-node/actions/runs/42478480733), job `128725006423`: **full and partial synthetic customer journeys PASS**, browser logs inspected.
- [Security & Ethics Actions run 42478480681](https://github.com/mommommy1960-lang/maya-node/actions/runs/42478480681): all five jobs **success** (core, red-team 100, Nightwatch 1000, scanning, ethics).
- PR #109 remains draft/unmerged. No public or production deployment, website/QR change, real data, partner dispatch, Stripe live charge, or outbound message.

## Remaining blockers and next priorities

- **Real authenticated actor/tenant authorization**, backed by independent accounts and permission tests. Current fictional actors are button impersonations.
- **Authorized hosted nonproduction Stripe TEST webhook** delivery and order correlation. Existing 154 local tests and read-only signed-fixture checks are not evidence of provider-to-Maya webhook receipt.
- **Hosted deletion, provider backup/retention behavior and isolated restore test**, actual incident escalation/coverage, data minimization and emergency pause.
- Written donor/receiver/carrier permissions, food-safety counsel/insurance/legal review, explicit founder go/no-go before any consequential pilot.
- If a corrupted reservation is detected, prototype now rejects unsafe action but has **no trusted repair procedure**; quarantine, audit and human resolution remain design work.

**Schedule review:** Nov 8 verified synthetic test/readiness checkpoint achieved; Nov 10–14 local browser demonstration evidence exists, but complete hosted, independently authorized journey remains unverified. Nov 21–Dec 19 remains a conditional review window, not a launch commitment. Next safe work: authenticated tenant isolation or approved nonproduction hosted recovery/provider-webhook evidence without bypassing consent.
