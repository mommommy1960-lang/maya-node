# Maya Node — local-only fictional customer journey (2026-11-07, 7 PM PST)

## Independently verified checkpoint
- Source commit: `483e0872e440250bf99a513ba0a08560b2de04ca`
- Pantry Watchtower CI: [run 42441241879](https://github.com/mommommy1960-lang/maya-node/actions/runs/42441241879), job [128610717633](https://github.com/mommommy1960-lang/maya-node/actions/runs/42441241879/job/128610717633). **86/86 synthetic Node tests passed, 0 failed, 0 skipped**, inspected TAP totals.
- [Security & Ethics run 42441241859](https://github.com/mommommy1960-lang/maya-node/actions/runs/42441241859): five jobs passed.
- Added twelve route/API integration tests to the prior 74, including simulated purchase-free order journey, all-three-approval gate, full/partial receipts, capacity accounting, cancellation, replay, cross-origin refusal and persisted SQLite recovery. These are local Node HTTP API tests, not real partner or hosted production tests.
- A genuine local Chromium UI smoke check, with **stubbed** `/api/state` and `/api/action` responses (not the real SQLite server), completed the visible mobile-size button flow from reserve through reconciliation and rendered the expected fictional receipts/capacity. This is **UI-only smoke evidence**, not an end-to-end real-browser-to-SQLite proof. The browser environment blocked direct loopback navigation, so real browser↔SQLite integration remains OPEN.

## Developer-only run
Requires Node.js 22+ with built-in `node:sqlite`; run from the repository root:

```bash
node --test prototypes/pantry-watchtower/*.test.mjs
node prototypes/pantry-watchtower/synthetic-local-demo-server.mjs
```

On the **same computer**, open `http://127.0.0.1:8789/`. The server binds only to 127.0.0.1 and has no live provider connections. A fresh run uses an in-memory SQLite database by default. For isolated persistence/crash-recovery tests, `createLocalDemo({filename})` accepts a local test database file. Never reuse a customer or production database file.

## Synthetic journey
1. Start an eight-unit fictional order. Debits eight units apiece from fictional food, cold-storage and truck capacities in one SQLite transaction.
2. Use the three **simulated** role buttons, which impersonate fictional donor, receiver and transporter identities. No actual sign-in or consent is checked.
3. Attempted pickup is denied until all three simulated approvals are saved.
4. Simulate pickup, then full receipt (8 received) or partial receipt (6 received, 1 rejected, 1 missing).
5. Full receipt reconciles. Partial receipt enters exception and requires separate fictional discrepancy disposition. Consumed/missing/rejected food never automatically becomes available, while reusable cold/truck slots return.
6. The browser exposes fictional event records, current resource counts, cancellation before pickup, refusal reasons and a high-contrast status notice.

## Trust and scope
- Origin/host protections, no-store/CSP/anti-framing, action allowlist, JSON-only writes, loopback binding. These **do not** replace authentication/authorization; the local demo intentionally uses fixed fictional actors and no multi-tenant model.
- No actual staff identities, signed evidence, food provenance, external messages, live inventory, payments, refunds or third-party connections.
- The UI is accessible-minded (labels, live status regions, keyboard focus, touch-sized buttons), but accessibility auditing, Android device validation and keyboard/screen-reader testing remain open.
- No hosted deletion, backup isolation/restore test, privacy/security assessment, written partner permission, named staffed incident escalation, legal review, or production launch authorization.
- **Real customer data, onboarding, external dispatch, real communications and live billing: NO-GO.**

## Next critical path (Nov 10–14 demonstration target)
1. Reproducible real browser↔SQLite end-to-end demonstration, with keyboard, narrow viewport and Android checks, including negative paths and restart.
2. Explicitly fake quote/terms, sandbox-only payment authorization/refund/webhook replay protection, never real keys or charges.
3. Hosted deletion, backup restore and incident-owner evidence; separate founder/legal/partner decision before any real pilot.

This is a development checkpoint, not an externally accessible customer website or a promised pilot release.
