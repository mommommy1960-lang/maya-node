# Maya Node guarded pickup authorization-order regression: November 8, 2026

**Scope:** Localhost-only, opt-in synthetic tenant-gated HTTP test harness. This work has NOT been merged or deployed to Maya's public Sites product. No real actors, data, messages, dispatch, customer payments, or provider Stripe webhook delivery were involved.

## Defect confirmed and fixed

The existing `/api/tenant-order` POST `pickup` path queried the fictional commercial/payment authorization state **before** it asked the synthetic tenant gate to verify the requester's tenant, actor and transport role. A caller who had no permission to access the order could therefore distinguish a mock-unpaid order (HTTP 409 `mock_authorization_required`) from a mock-authorized one (HTTP 403 authorization denial), leaking an internal milestone. This is a synthetic test-boundary information leak, not evidence of an external compromise.

The code now invokes `tenantGate.assertPickupPermission(ORDER)` **first**. Only a scope-authorized fictional transporter may learn whether the mock payment state is authorized. The gate still checks the role and tenant again at the actual pickup transition. An unauthorized requester receives HTTP 403 regardless of commercial state. No production identity, customer authorization or Stripe connection was introduced.

## Independently verified test evidence

- Final tested **code + regression commit**: [9eecb5dbfcface3139cb6d65cc384a52cd32a8c8](https://github.com/mommommy1960-lang/maya-node/commit/9eecb5dbfcface3139cb6d65cc384a52cd32a8c8). Changes: `synthetic-tenant-order-gate.mjs`, `synthetic-local-demo-server.mjs`, `synthetic-tenant-bypass-closure.test.mjs`, plus correcting outdated pre-fix status assertion in `synthetic-tenant-http-gate.test.mjs`.
- [Node CI 42498119876](https://github.com/mommommy1960-lang/maya-node/actions/runs/42498119876), job **128784765803**, **173 passed / 0 failed / 0 skipped**. The TAP log shows the new status-oracle regression passing and total test counts.
- [Real Chromium-to-loopback HTTP-to-SQLite CI 42498119808](https://github.com/mommommy1960-lang/maya-node/actions/runs/42498119808), job **128784765545**, both full and partial fictional browser journeys PASSED. They still exercise the original local demo mode, **not** hosted guarded customer authentication.
- [Security & Ethics 42498119814](https://github.com/mommommy1960-lang/maya-node/actions/runs/42498119814), five jobs completed successfully.
- A preceding [failed Node run 42498065082](https://github.com/mommommy1960-lang/maya-node/actions/runs/42498065082) exposed one old test's expectation of HTTP 409 for an unauthorized donor; the corrected behavior is HTTP 403. The assertion was fixed, with no relaxation of the security change, and CI then passed.

## Regression meaning and limits

The new test creates an isolated fictional reserved order, obtains the three fictional approvals through **trusted in-process fixture setup**, exercises missing, wrong-tenant, wrong-role and wrong-actor HTTP pickup attempts both before and after a fake authorization, verifies each remains HTTP 403 with no order data or mutation, checks a valid transport actor sees HTTP 409 before mock authorization, then allows mock pickup once authorized. Test headers remain **spoofable fixtures**, not credentials.

**Readiness:** Nov 8 synthetic test/readiness checkpoint remains evidence-backed. Publicly hosted/Android browser-complete Nov 10–14 demonstration is NOT verified. Conditional pilot-decision planning remains Nov 21–Dec 19, NOT a promised launch. Real customer use **NO-GO** until independently verifiable authenticated, revocable tenant sessions on every state/action route; nonproduction hosted customer journey; authenticated Stripe TEST webhook-to-order trace; hosted deletion and isolated backup recovery; incident ownership/backups; written partner authority and food-safety/legal review; and explicit founder approval. Next engineering priority is a real identity/session boundary and its full synthetic browser coverage. No production deployment or real-world changes were made.
