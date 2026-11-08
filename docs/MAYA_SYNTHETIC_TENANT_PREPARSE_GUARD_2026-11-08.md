# Maya Node — tenant-first guarded HTTP validation (synthetic-only)

**Date:** 2026-11-08, ~10:01 AM America/Los_Angeles. **Status:** verified in GitHub CI on the exact code/test commit. Draft PR #109 only; no Site deploy or real users.

## Change and reason

The opt-in local `/api/tenant-order` POST previously checked Content-Type and parsed JSON before establishing the request's fictional tenant and actor scope. An unauthenticated, cross-tenant or impersonating caller could receive 415/409 validation responses, or trigger untrusted JSON parsing, before scope denial. This was a fail-closed validation ordering gap in a **local synthetic test harness**, not evidence of a real incident or public exposure.

The HTTP handler now invokes `tenantGate.read(ORDER)` before inspecting Content-Type or parsing POST JSON. The earlier outer 415 short-circuit was relocated inside the scoped tenant route. Existing action-specific role checks still apply: generic read permission never authorizes pickup, receipt or cancellation. No headers, browser fields or JSON identity claims become credentials.

Added `prototypes/pantry-watchtower/synthetic-tenant-preparse-boundary.test.mjs` with two independent regression cases. The first sends parallel malformed or wrong-Content-Type requests from missing, other-tenant and wrong-actor test identities and verifies 403 with no order data or mutation. The second verifies authorized fictional participants still receive 415 (wrong Content-Type), 409 (invalid JSON) and can perform a valid donor approval. These are spoofable test-injected principals, **NOT REAL AUTHENTICATION**.

## Exact saved commits and independent verification

- Source: [`4b805bbeb0c9861d7846a9c667a55fd4dcb4d6b1`](https://github.com/mommommy1960-lang/maya-node/commit/4b805bbeb0c9861d7846a9c667a55fd4dcb4d6b1)
- Source plus regression tests (exact CI head): [`2dea7afa5888f320f0e08c4cf86d56217e6d9cc7`](https://github.com/mommommy1960-lang/maya-node/commit/2dea7afa5888f320f0e08c4cf86d56217e6d9cc7)
- [Node CI run 42507851350](https://github.com/mommommy1960-lang/maya-node/actions/runs/42507851350), job **128814265908**: TAP log inspected, **178 passed, 0 failed, 0 skipped**.
- [Real Chromium → loopback HTTP → SQLite run 42507851357](https://github.com/mommommy1960-lang/maya-node/actions/runs/42507851357), job **128814266285**: both full and partial fictional browser journeys **PASS**, still on the intentionally **unguarded** legacy demo; neither is a hosted browser or protected session.
- [Security & Ethics run 42507851416](https://github.com/mommommy1960-lang/maya-node/actions/runs/42507851416): all **five jobs successful**.

## Limits and next work

The server listens on 127.0.0.1 and its resolver is a spoofable test double. This fix does **not** supply customer login, revocable sessions, durable hosted tenant controls, a protected browser dashboard, payment provider event mapping, or privacy compliance. Real hosted deletion/isolated backup restore, incident staffing, written partner permission and independent legal/food-safety review remain unverified. Draft PR #109 stays unmerged. No production deploy, real customer data, actual dispatch/messages, Stripe financial operations or live billing performed.

**Go/no-go:** synthetic CI evidence **GO for continued isolated development only**; real customers, live billing, external messages and real pilot **NO-GO**. November 8 synthetic checkpoint met. November 10–14 browser-verified goal has local unguarded evidence but **not** protected hosted evidence; November 21–December 19 is a conditional evidence-based pilot *decision*, never a launch promise. Next prioritize independently authenticated and revocable hosted actor/tenant sessions and protected end-to-end browser verification rather than adding unactionable test-count claims.
