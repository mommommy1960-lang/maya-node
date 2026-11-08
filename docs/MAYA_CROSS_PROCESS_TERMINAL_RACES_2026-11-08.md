# Maya Node — independent SQLite-process expiry and terminal-action races
2026-11-08, approximately 12:05 PM America/Los_Angeles. Synthetic-only engineering checkpoint; NOT a real-customer release.

## Source and concrete change
On draft PR #109, added:
- `prototypes/pantry-watchtower/reservation-race-worker.mjs` — genuinely separate Node operating-system processes, each opening the same file-backed SQLite ledger and order store.
- `prototypes/pantry-watchtower/reservation-cross-process-terminal-races.test.mjs` — three fresh contention tests.

The regressions simultaneously exercise: **(1)** six separate processes claiming the same food/freezer/truck after one bundle's deadline; **(2)** two independent order-expiry sweepers competing with four claimers while preserving exactly one audited expiry and one new reservation, including retry after the sweeper; **(3)** separate-process pickup versus pre-pickup cancellation at the same logical time, with exactly one terminal winner, no phantom replenishment and a restart recheck. These are distinct from earlier single-process expiry checks and six-process unexpired claim tests. Workers reject unexpected SQLite locking/infrastructure faults instead of silently treating them as ordinary capacity denial.

## Verified CI evidence for exact source commit
- [Code/test commit `90ddf22f8d08aaf5c68ab9b3cda94fbe5a784dde`](https://github.com/mommommy1960-lang/maya-node/commit/90ddf22f8d08aaf5c68ab9b3cda94fbe5a784dde). Worker commit `de9107f68970e9948c8cc125ee3e9a658db5fde5`.
- [Pantry synthetic Node CI run 42518273482](https://github.com/mommommy1960-lang/maya-node/actions/runs/42518273482), job **128845964108**: inspected TAP, **185/185 passing, zero failures**. All three new independent-process tests explicitly reported `ok` (#46–48).
- [Real Chromium → loopback → SQLite run 42518273489](https://github.com/mommommy1960-lang/maya-node/actions/runs/42518273489), job **128845963997**: two full/partial fictional journeys PASS; these still use the **unguarded** local demonstration, not hosted or authenticated sessions.
- [Security & Ethics run 42518273431](https://github.com/mommommy1960-lang/maya-node/actions/runs/42518273431): 5/5 jobs successful.

## Honest limitations and next gate
These tests support the invariant that the *tested local SQLite model* serializes overlapping reservations, expiry, pickup and cancellation under independent processes. They do **not** verify a server with real identity, network partitions, held locks across crash power loss, multi-host database semantics or an externally hosted pilot. Shared-file SQLite is not a drop-in distributed database. The 50- and 60-step backlogs are **acceptance plans**, not automatically checked-off milestones: independent reviewer, negative testing and hosted proof remain pending.

Prioritize real server-authenticated revocable tenant identities and a browser-verified protected end-to-end **synthetic** journey; next Stripe TEST provider webhook-to-order evidence, hosted deletion and isolated restore, incident owner/backup, and signed partner/legal/food-safety approval. Current Maya site and PR remain untouched by deployments/merges.

## Founder decision
Nov 8 engineering evidence target: established for local synthetic scope. Nov 10–14 protected hosted-browser target: still **unverified**. Nov 21–Dec 19: conditional founder go/no-go decision window, not a launch promise. Real user records, external messages, live dispatch, live payments and public production release: **NO-GO** until the separate controls, permissions, independent verification and founder authorization exist.
