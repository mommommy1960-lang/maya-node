# Maya Node — server-injected fictional tenant gate at an isolated HTTP boundary
November 8, 2026, approximately 06:03 PST (America/Los_Angeles)

## What was actually implemented

On **draft PR #109 only**, the loopback synthetic demo now contains a separate opt-in `GET/POST /api/tenant-order` route. It wraps the previously standalone `SyntheticTenantOrderGate` so synthetic tenant/actor checks are exercised through **real localhost HTTP and persistent SQLite**, not only direct class calls.

- When no explicit trusted *test harness* resolver is installed, the entire route fails closed with HTTP 403; ordinary demo/browser routes remain unchanged and unauthenticated by design.
- An injected server-side test resolver supplies a fictional principal, isolated per concurrent request with `AsyncLocalStorage`. The protected route never accepts client-supplied `actorId`, `tenantId`, `role`, or `authenticated` fields as identity.
- Tenant-bound `GET` reads only the synthetic order under the caller's fictional tenant/actor role. This response does **not** return the commercial or delivery receipt objects.
- Protected `POST` accepts only role-checked fictional approval, pickup, and pre-pickup cancellation. Pickup additionally requires the existing *local simulated* commercial authorization state; donor/receiver cannot impersonate transporter. No actual money movement or dispatch.
- Tenant bindings are provisioned only by local in-process fixtures, not by HTTP. The test resolver uses a fake request-header lookup and is **not** a real session credential, user authentication, or production integration.
- The original `/api/state` and `/api/action` remain accessible in the **127.0.0.1-only fictional demonstration**. They deliberately impersonate demo actors. Therefore the overall server is **not secured for any public exposure or customer access**. This is isolated validation of a future authorization boundary, not a deployed authentication system.

## Independently observed GitHub CI on exact code commit

Tested source commit: `c348eb5ab688d31c33687da34a16195f4913069c` (preceding source and regression commits `775cac8bae1cf9b812089eace0b3a4c314000134`, `f69d06bee860f250265c7bde07040533e1eb4bd4`).

- [Pantry Node CI run 42487830244](https://github.com/mommommy1960-lang/maya-node/actions/runs/42487830244), job `128753475009`: TAP job log inspected. **167 tests passed, 0 failed, 0 skipped**, five additional actual HTTP negative/positive/restart tests beyond the previous 162.
- [Real Chromium → loopback HTTP → SQLite run 42487830206](https://github.com/mommommy1960-lang/maya-node/actions/runs/42487830206), job `128753475023`: log inspected. Both full fictional journey (`partial=False`) and partial/reconciliation journey (`partial=True`) **PASS**. **Important:** These existing browser journeys use the intentionally unrestricted fictional demo route; they do NOT verify authentic tenant login, nor full tenant-protected commercial flow.
- [Security & Ethics run 42487830208](https://github.com/mommommy1960-lang/maya-node/actions/runs/42487830208): all **five** constituent jobs reported success.
- Test source: `prototypes/pantry-watchtower/synthetic-tenant-http-gate.test.mjs`. Scenarios cover disabled route, absent/wrong-tenant/wrong-actor principals, client identity spoofing, concurrent requests, wrong role, pickup/payment prerequisite, cancellation after pickup, and immutable tenant binding after SQLite restart. These are **synthetic test fixtures**.

## Limits and next highest-impact work

Before any real pilot, the full customer application still needs genuine independently authenticated revocable tenant sessions and least-privilege access for **all** read/write/receipt/payment/administrative routes, with browser and hosted verification, plus written authorization from partners. The old demo's unprotected routes must never be considered production-safe.

Further independently outstanding: provider-origin Stripe **TEST** webhook delivery into an authorized hosted nonproduction endpoint and exact fictional order linkage; hosted deletion and backup retention/isolated restore; actual incident coverage and escalation; written donor/receiver/transport permissions; food-safety and independent counsel review; founder go/no-go decision. No production deployment, real data, external messaging, live billing, physical dispatch or third-party actions occurred.

## Schedule checkpoint

- November 8: verified synthetic test/readiness checkpoint, **not real-pilot readiness**.
- November 10–14: complete *hosted* browser-verified synthetic customer journey remains open; current Chromium demo is local, fictional, and unguarded.
- November 21–December 19: conditional evidence-based limited-real-pilot decision window, not a promised launch.

**Real data, production, live billing, real dispatch, public onboarding: NO-GO.**
