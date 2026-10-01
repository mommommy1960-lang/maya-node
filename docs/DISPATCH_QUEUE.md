# Durable dispatch gate

`src/sovereign/dispatch_queue.py` adds an opt-in SQLite queue with immutable approved payloads, durable cancellation, transactional single-worker claims, receipt recording, and no automatic retry of uncertain outcomes.

A trusted authenticated controller enqueues and approves the exact payload. Workers call `dispatch(job_id, sender)`; the sender receives the stored payload and returns a JSON receipt. Use one shared local SQLite database across processes, not separate per-worker copies or a network filesystem. Do not call this module from untrusted agent code with approval privileges.

Cancellation is guaranteed only before the durable dispatch claim. After the claim, cancellation reports `too_late`, even if the provider call has not begun. Provider submission cannot be atomically reversed by SQLite. This is deliberately conservative, not exactly-once delivery.

A timeout becomes `unknown`; a crash after claim remains `dispatch_committed`. Both block all automatic redispatch. An operator must inspect provider history and reconcile them. There is intentionally no blind reset/retry endpoint. A canceled payload requires a new job and explicit fresh approval to send again.

The module is not automatically wired into SovereignRuntime or a Gmail daemon. No production queue daemon exists in this implementation. All send paths must explicitly use this gate before rollout. Existing in-memory consent tokens remain separate; this queue does not persist their cryptographic state or implement authentication.

Validation on October 1, 2026: 10 unittest cases passed: approval required; cancellation survives reopening; eight independent SQLite worker connections produce one claim; timeout blocks retry; crash after claim blocks reclaim; sent receipt survives reopening; changed payload rejected; late cancellation reports too late; cancel/claim race has one winner; wrong receipt attempt rejected. Tests use fake sender callbacks. Prior Gmail connector demonstrations were separate and do not validate this durable module with Gmail.

Run: `python -m unittest discover -s tests/runtime -p test_dispatch_queue.py -v`

## Morning outreach receipt

Four separate $25 founding-review introductions were sent from the authorized Gmail account on October 1: Marc-Tek, Pulsework AI, Click Smith, and Cryudine. No customer workflows were accessed or defects claimed. Replies and sales were unconfirmed at the last mailbox check. Public site sample-review links were removed at the user's request.
