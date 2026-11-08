# Maya Node synthetic tenant/actor authorization boundary — November 8, 2026, ~05:05 PST

## Scope and source
- **Draft PR #109**, synthetic-only, no hosted deployment and no real tenant login.
- Source: `prototypes/pantry-watchtower/synthetic-tenant-order-gate.mjs` (commit `44bf13230f7b0eec2256d86417d3ea1d6a8a03df`).
- Eight executable regressions: `prototypes/pantry-watchtower/synthetic-tenant-order-gate.test.mjs` (tested commit `a68d69d11d0f10e09e307a2cb566c8c22389781a`).
- A separate `SyntheticTenantOrderGate` wraps the existing synthetic SQLite store's read, approval, pickup and cancellation methods. It refuses unbound orders, missing/malformed server principal, different tenants, actor mismatch, wrong role and operator impersonation. Principal actor ID is resolved by an injected trusted server boundary, **never copied from an action's actorId field**.
- Explicit, immutable synthetic order-to-tenant bindings remain persistent across SQLite restart. Conflicting rebinds and raw SQL update/delete attempts fail. Successful fictional approvals and role-gated pickup/cancellation still preserve the underlying order-state and reservation safeguards.
- **Crucial limitation**: `resolveServerPrincipal` currently uses test doubles. `authenticated:true` is an internal interface contract, **NOT proof of login, verified identity, signed session, or tenancy**. The gate is **not wired into the demo server**, deployed Sites app, QR website, Stripe provider endpoint or public browser flow. Provisioning is a trusted-local-only operation, not HTTP input. Do not expose this class as an authentication service.

## Exact GitHub CI verification
- [Node test run 42483155328](https://github.com/mommommy1960-lang/maya-node/actions/runs/42483155328), job `128739253752`: inspected TAP summary **162 passed / 0 failed / 0 skipped** (previous 154, eight new).
- [Actual Chromium ↔ localhost ↔ SQLite browser run 42483155389](https://github.com/mommommy1960-lang/maya-node/actions/runs/42483155389), job `128739254202`: inspected logs show full fictional journey `partial=False` PASS and partial journey `partial=True` PASS. The new tenant guard is **not** exercised by these existing browser journeys; it has Node tests.
- [Security & Ethics run 42483155336](https://github.com/mommommy1960-lang/maya-node/actions/runs/42483155336): all five jobs completed successfully (Core Runtime, Adaptive Red-Team 100, Nightwatch 1000, Bandit security scanning, ethics).
- All three runs executed for source/test commit `a68d69d11d0f10e09e307a2cb566c8c22389781a`.

## Remaining gates and next acceptance criteria
1. Integrate verified independent authenticated sessions (server-trusted principal, expiration/revocation/rotation, least-privilege) with a tenant registration/permission model; cross-tenant tests must exercise **real browser and hosted** APIs. Current fictional role impersonation remains restricted to local synthetic demo.
2. Gate all read and mutation routes, including receipt/financial/cancellation flows and admin support, not only the four methods above; enforce cross-organization resource consent, signed evidence and audit.
3. Independently verify Stripe TEST provider-to-authorized-nonproduction hosted webhook and fictional order reconciliation. Local fixtures and signed test doubles are insufficient.
4. Obtain hosted deletion/backup expiry and isolated restoration, incident escalation coverage and tablet-notification evidence, written donor/receiver/transporter permission, food-safety and legal review.
5. Continue using November 8 as a verified *synthetic testing* checkpoint; November 10–14 public hosted synthetic browser experience remains unverified; November 21–December 19 is a conditional **decision window**, not customer launch.

**Real customer data, production deployment, real dispatch, external messages, live billing: NO-GO.** No such operations performed.
