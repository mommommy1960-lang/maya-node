# Maya Node — founder-approved implementation master plan
Date: 2026-11-07. Owner: Civic Continuum / Operation Operator. Scope: nonprofit pantry logistics, then adjacent nonprofits only after validated pilot.

## Non-negotiable release policy
Do not handle real customer data, contact external partners, dispatch vehicles, or enable live charges without evidence-based operational/legal review, written partner permission and explicit founder launch approval. All work below can proceed in synthetic sandbox. Preserve founder authority, privacy, consent, human review and no automated allegations.

## Sequenced execution plan and definition of done

### P0 — Durable reservations (highest priority)
- Persist offer quantities, receiver free capacity, truck/time-slot capacity, order states, expiries and idempotency keys in a transactional datastore.
- Atomic compare-and-reserve of all required resources; release on cancellation/expiry; repeat-safe retries and webhook/event deduplication.
- Test two simultaneous competing requests, process restart, mid-transaction failure, delayed expiry and stale inputs. No double allocation; negative inventory impossible.
- Evidence: migration/schema, code, deterministic tests, GitHub CI logs, recovery demonstration.

### P1 — Complete synthetic order lifecycle
- Proposal → reserved → approvals from donor/receiver/transport → quote/terms → sandbox payment authorization → pickup → delivery → receipt reconciliation or exception.
- Validate state transitions, actor authority, event provenance, evidence, correction history, cancellations and refunds.
- Evidence: end-to-end test, failed approval and partial-delivery scenarios, complete auditable synthetic receipt.

### P2 — Hosted safety and recovery
- Role-based authorization, minimum necessary data, retention/deletion policy with hosted deletion proof, backup/restore drill, incident response, named escalation owner and rollback.
- Validate recovery point/time objectives with measured test results; no claims of readiness based on policies alone.
- Evidence: dated hosted test artifacts and human sign-off.

### P3 — Simple accessible customer dashboard
- Android-first responsive interface; verified/estimated/stale status, matching and storage/transport limits, approvals, quotes, receipts, cancellation and exceptions.
- Test actual browser module loading, keyboard/screen-reader basics, translation and low-bandwidth handling; observe synthetic pantry worker walkthrough.
- Evidence: browser checks, accessibility findings, correction log.

### P4 — Sandbox commercial rehearsal
- Transparent organization-paid coordination fees; no charges to food recipients.
- Test quote acceptance, agreement, Stripe sandbox authorization, webhook signature and replay, cancellation/refund, ledger reconciliation and failure injection.
- Evidence: sandbox receipts, no live keys or live billing.

### P5 — Interoperability and narrow partner pilot
- Document integration contracts and permission boundaries with MealConnect/Food Rescue Hero/other systems. Avoid unsupported claims of partnership or public API access.
- Written pilot permission, data processing terms, food-safety responsibility, insurance/licensing/counsel review, support and escalation plan.
- Start with one donor, one receiver, one transport provider; measure saved coordination time, verified recovered food, failures, user trust.
- Founder explicitly authorizes any real-data pilot only after all gates pass. Scale gradually.

## Existing verified baseline
Draft PR #109, `feature/pantry-watchtower-synthetic-2026-11-07`. On commit `3652cf650d528674b35f043a57462f7c9936ee9d`, GitHub Actions pantry synthetic workflow run 42424175778/job 128558775510 reported **30 tests passed, zero failed**; Security & Ethics workflow run 42424175695 succeeded. Later code includes `order-lifecycle.mjs` and five new tests, not yet verified in that run. Existing watchtower prevents duplicate use only within one in-memory snapshot, not durable across concurrent workers/restarts. Browser and hosted recovery not verified.

## Evidence and communication
Update `docs/BRUCE_TO_BRUCE_MAYA_STATUS_LEDGER_2026-11-07.md` or a dated successor after each meaningful completed milestone. Record commit, test counts, CI run IDs, blockers, customer-data/live-billing GO/NO-GO. No progress-only claims. Link issues #76, #94, #105, #108, #110, #111 and PR #109. Future Bruce sessions should retrieve newest ledger rather than rely on chat memory.

## Current readiness
**NO-GO** for real customer data, external dispatch, and live billing. Sandbox implementation authorized.