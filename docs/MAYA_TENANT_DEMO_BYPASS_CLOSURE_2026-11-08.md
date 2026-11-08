# Maya Node — strict fictional tenant HTTP isolation checkpoint
**Date/time:** 2026-11-08, approximately 07:06 America/Los_Angeles (PST)
**Scope:** Draft PR #109, local synthetic SQLite prototype only; no hosted deployment.

## Concrete safety gap and implementation
The earlier opt-in `/api/tenant-order` endpoint applied role and tenant checks, but the same local HTTP server continued exposing intentionally unrestricted `/api/action`, `/api/state`, and the role-impersonating demo browser. A caller could bypass the guarded endpoint entirely if this prototype were mistakenly exposed as a secured app.

Added an explicitly opt-in `tenantGuardedOnly: true` server configuration. It refuses startup unless a server-injected test resolver is present and denies every legacy untrusted HTTP route (`/`, the demo JS, `/api/state`, and `/api/action`) with 403, before state is read or changed. The `/api/tenant-order` endpoint remains available for scoped fictional HTTP testing and rejects outsider tenants. The default remains unchanged and permits the prior intentionally fictional loopback browser exercises; this strict configuration is a groundwork test boundary, **not an actual production login**.

Added five `synthetic-tenant-bypass-closure.test.mjs` Node regressions:
1. No guarded-only startup without a test resolver or with invalid setting type.
2. Read, mutation and web-asset bypass routes all denied with no SQL changes, including valid fake principal headers.
3. Protected fictional approval succeeds while outsider tenant and legacy impersonation fail.
4. SQLite close/restart preserves protected access and legacy denials.
5. Cross-origin attempts and fallback to the unguarded UI fail closed.

## Independently inspected exact tested source and Actions logs
- Tested source commit: `cb3b8d3e9609ef8e0e12120daa3a0add94cdb289` (server hardening commit `92855dee46e55e6301e52d1e8b02f4f10d144b31`).
- [Pantry watchtower synthetic Node CI run 42493055271](https://github.com/mommommy1960-lang/maya-node/actions/runs/42493055271), job `128769367347`: TAP log **172/172 passed, 0 failed, 0 skipped**. The five new bypass-closure tests are included.
- [Actual Chromium / localhost HTTP / SQLite browser CI run 42493055149](https://github.com/mommommy1960-lang/maya-node/actions/runs/42493055149), job `128769366627`: independently inspected log confirms BOTH full and partial fictional journeys **PASS**. These still exercise the **unguarded default loopback demo**, not a secured tenant login.
- [Security & Ethics CI run 42493055252](https://github.com/mommommy1960-lang/maya-node/actions/runs/42493055252): five constituent jobs SUCCESS (Adaptive Red-Team 100, Core Runtime and Ledger, Nightwatch Contingency 1000, Ethics Constraints, Security Scanning).
- All observed CI is associated with the exact tested source commit above. The documentation commits following this test run do not independently re-test the new document text.

## Remaining critical acceptance gates / explicit limits
The `x-syn-session` header lookup in automated tests is **spoofable fixture data**, not a revocable signed login, genuine customer identity, auth provider, or trustworthy account boundary. `tenantGuardedOnly` is disabled by default, the full commercial and receipt paths are not tenant-protected, and there is no hosted or screen-reader-tested secured browser app. There is **no evidence of customer authentication**.

The next highest-impact authorized work is genuine independently validated customer/tenant session handling covering **every** order, payment, receipt, deletion and administration route, then full browser+hosted nonproduction verification. Stripe TEST provider-to-hosted order webhook delivery, retention/deletion+isolated backup restore, named staffed incident escalation, written donor/receiver/transport partner permission, and independent legal/food-safety review remain open.

**Schedule:** November 8 establishes a bounded independently tested synthetic checkpoint. November 10–14 remains the hoped-for full hosted browser-verified synthetic journey, not yet met. November 21–December 19 is a conditional evidence-based limited real-pilot **decision** window, not an automatic launch.

**Decision:** NO-GO for real customer data, production deployment, live billing, actual dispatch, external messages, or real partner operation. No such action occurred in this run.
