# Maya Node: first tenant-guarded *local* Chromium browser journey

Verified November 8, 2026, approximately 13:02 America/Los_Angeles.

## What was actually implemented

Source [commit 6b5bcf43](https://github.com/mommommy1960-lang/maya-node/commit/6b5bcf43d5275c09f77ea6c3e2926716352f10ea) on draft PR [#109](https://github.com/mommommy1960-lang/maya-node/pull/109), not merged or deployed.

- Opt-in `tenantGuardedOnly` serves `/guarded` plus a separate browser module; the legacy untrusted root, state, and action routes remain unavailable in guarded mode.
- Four real Chromium-to-localhost-to-SQLite runs in CI: two prior full/partial unguarded demonstrations and two newly protected-by-test-boundary full/partial journeys. The new paths use distinct browser contexts and a deliberately **spoofable test header**, so a server-injected fictional principal resolves every HTTP permission check; the UI offers no role selector.
- New browser flow starts with a pre-seeded fictional order in a local Node fixture. It checks anonymous, wrong-tenant and wrong-actor denial; makes three fictional approvals; checks a wrong-role pickup denial; applies fake sponsor state through the test process's **stdin**, never through a privileged HTTP endpoint; then uses transport pickup and receiver full/partial receipt. Partial flow records exception. Browser reload confirms persisted SQLite state, with mobile-width and keyboard reachability checks.
- Visible warning says *synthetic only* and *no customer login*. State changes use server-authorized `POST /api/tenant-order` and reads use `GET /api/tenant-order`. The browser uses textContent, not untrusted HTML interpolation, and the page is served under existing no-store/no-frame and restrictive CSP headers.

## Exact verification

- [GitHub Actions browser run 42523089480](https://github.com/mommommy1960-lang/maya-node/actions/runs/42523089480), browser job 128860660751: successful. Logged old unguarded full + partial and new test-guarded full + partial, all four PASS; no silently skipped Chromium.
- [PR browser rerun 42523096245](https://github.com/mommommy1960-lang/maya-node/actions/runs/42523096245): successful.
- [Node tests 42523089583](https://github.com/mommommy1960-lang/maya-node/actions/runs/42523089583), job 128860661342: 185 passed, 0 failed, 0 skipped.
- [Security and Ethics 42523096269](https://github.com/mommommy1960-lang/maya-node/actions/runs/42523096269): five jobs successful.
- Run locally with Python Playwright + Chromium available: `python prototypes/pantry-watchtower/synthetic-guarded-browser-smoke.py`. Test harness binds only 127.0.0.1, uses only seeded fake tenant/actors; no credentials or real partner data.
- Verified source PR head: `6b5bcf43d5275c09f77ea6c3e2926716352f10ea` at test time.

## What is still NOT done

**All real-customer decisions remain NO-GO**: Browser tests use forgeable fixture headers, not a revocable authenticated human session; HTTP demo is local and not public Maya Site. The fake internal sponsor is neither live billing nor a Stripe test-mode webhook-to-order. Missing independent hosted deletion, isolated backup restore, staffed incident coverage, written partner permission, independent legal/food-safety review, support operations and founder evidence-based release decision. Screen-reader and Android-device testing are not established by Chromium keyboard/mobile checks.

Do not merge the draft or publish this as customer-ready. Keep real data, dispatch, partner integrations, external messages and billing disabled. Next high-value task: authenticated and revocable **nonproduction** tenant session integration plus hosted end-to-end evidence, followed by recovery and sandbox provider verification without bypassing release gates.
