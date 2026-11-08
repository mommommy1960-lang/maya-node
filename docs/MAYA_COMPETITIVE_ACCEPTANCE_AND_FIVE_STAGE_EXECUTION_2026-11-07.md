# Competitive gap-to-build acceptance matrix — 2026-11-07

## Verified baseline
GitHub Actions run 42424175778, job 128558775510, on PR #109 head 3652cf650d528674b35f043a57462f7c9936ee9d: **30 Node tests passed, 0 failed**, including 30 fictional pantries/300 offers/40 trucks and 100 synthetic shipment reconciliations. Security & Ethics workflow run 42424175695: success. This verifies only synthetic unit/integration assertions, not live concurrency, throughput, browser behavior, or production safety.

## Common evaluation scenario (use identical inputs for each vendor demo)
- Donor has 200 boxes chilled produce; receiver A capacity 180, receiver B capacity 50; one refrigerated truck; deadline 90 minutes.
- A and B submit competing requests concurrently.
- One receiving contact is unreachable; a consented backup is available.
- Load 200, receipt confirms 180, 20 unaccounted.
- One request is canceled after tentative hold; restart service mid-workflow.
- Test no duplicate reservation, authorized actions, clear escalation, evidence trail, correct cancellation/refund behavior, data export and deletion.

## Comparative evaluation rubric (unknown until demonstrated)
For MealConnect, Food Rescue Hero, Food Rescue US, Goodr, Spoiler Alert, Share My Meals and Maya: record product demo date, evidence URL, API availability, verified capacity freshness, atomic reservation, pickup proof, partial delivery reconciliation, escalation, cancellation, export, data deletion, pricing, accessibility. Mark unknown rather than assuming absence.

## Five engineering stages ahead
1. Durable transactional resource ledger (offer units, truck/time slots, receiving storage), idempotency keys, expiration and crash recovery. Synthetic concurrency tests must show one winner under two simultaneous claims.
2. Human-approved order state machine with append-only event audit, quote/terms, cancellation, corrections and evidence-grade receipts. Invalid transitions fail closed.
3. Sandbox billing and refund simulation only, with replay-safe webhook processing, reconciliation, no live Stripe mode.
4. Browser-tested Android-accessible full synthetic journey with failure injection, stale data and offline/retry scenarios; no fake partner claims.
5. Hosted deletion/backup restore, named escalation and written partner permission, then narrow controlled pilot only after explicit founder go/no-go.

## Current decision
**NO-GO for real customer data, live billing, actual truck dispatch or public production launch.** Synthetic development may proceed. No rival feature is marked missing without direct evidence.