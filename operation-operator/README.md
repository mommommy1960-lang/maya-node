# OPERATION OPERATOR — Maya's food-network coordination integration program
Date: 2026-11-06
Owner: Civic Continuum founder; engineering workstream independent of the Maya website recovery.
Status: SPECIFICATION AND SYNTHETIC DESIGN ONLY. No third-party access, agreements, production integration, or real-data authorization claimed.

## Mission
Maya is an accountable coordination operator *between* authorized food banks, food pantries, donors, dispatchers, and their existing inventory/delivery systems. She identifies surplus-to-need opportunities, obtains required human approvals, sends approved requests through authorized channels, verifies delivery evidence, and maintains an auditable correction trail. Maya is NOT another inventory system and may never infer misconduct from mismatches alone.

## Connector contract (per organization)
- Partner name, software product, data owner, technical contact, named human escalation and backup.
- Written scope/consent: tenant, site, fields, purposes, retention, revocation, permitted outbound actions, access window, deletion agreement.
- Connection mode: supported API + OAuth/scoped token, approved webhook, secure CSV/SFTP export, or manual staff entry. Never bypass controls or scrape private interfaces.
- Capabilities declared separately: read surplus, read requests, read delivery, read inventory, propose match, submit approved transfer, receive confirmation, retrieve receipt. Default all outbound capabilities OFF.
- Health: last successful sync, data freshness, error/retry/backoff, revoked credentials, schema version, source reference.
- No secrets in GitHub, frontend, logs, or handoff. Use encrypted secrets manager, rotate and revoke.

## Shared normalized record (schema proposal)
source_system, partner_id, site_id, source_record_id, record_type, observed_at, source_updated_at, ingested_at, food_category, item_name, quantity, unit, condition, safe_use_by, storage_requirement, location_area, pickup_window, delivery_window, transport_requirement, status, source_evidence_ref, consent_scope_id, confidence, synthetic.
No customer personal data by default. Treat source statements as unverified until confirmed. Store provenance and corrections; avoid silently overwriting.

## Operator state machine
1. INTAKE: receive allowed surplus/need signals, validate schema, consent, tenant isolation, freshness.
2. MATCH_PROPOSED: candidate matching by food type, quantities, expiry, distance, storage, transport, pickup availability, fairness and partner rules. Present explanation, not unsupported guarantees.
3. HUMAN_REVIEW: both sending and receiving organizations confirm independently; dispatch requires a separately authorized person and documented permission.
4. APPROVED: create scoped instruction and immutable audit receipt; idempotency key avoids duplicate orders.
5. DISPATCHED: approved driver/partner confirms collection; record evidence.
6. RECEIVED: recipient independently confirms condition and actual quantity; discrepancies go to human escalation.
7. CLOSED or EXCEPTION: reconcile ledger and preserve corrections, reasons, notifications, receipts.
Revocation or stale/failed connection means PAUSE; no silent fallback to unauthorized action.

## Adapter interface
- describe_capabilities() -> metadata, authorization status, freshness and supported fields
- fetch_surplus(since,cursor) -> normalized records with source refs
- fetch_needs(since,cursor) -> normalized records with source refs
- fetch_delivery_events(since,cursor) -> normalized records with source refs
- propose_transfer(proposal) -> local draft ONLY, never external action
- submit_approved_transfer(approved_instruction, human_approval_receipt) -> explicit allowlist and partner permission required
- verify_receipt(transfer_id) -> independently sourced receiving evidence
- revoke() -> stop access and invalidate pending actions
Each adapter must fail closed, enforce tenant isolation, rate limits, idempotency, expiry, and audit logging. If only CSV/manual data is permitted, implement a read-only adapter.

## Partner discovery checklist
The two previously discussed major food-network platforms are NOT reliably identified in this handoff. Do not guess or claim partnerships. For each candidate, investigate official API docs, integration/partner policy, available exports, webhooks, costs, data ownership, legal terms, pilot permissions, and nonprofit pricing. Begin with two willing pantry sites using fictional data; only proceed to real data after written permission and all production gates.

## Pilot success metrics
Time spent coordinating per transfer, surplus matched to verified needs, pickup success rate, usable food delivered, preventable spoilage (baseline vs pilot), missing receipt rate, exception resolution time, human approval latency, staff satisfaction, and cost per transfer. Record baseline and denominator; no invented impact claims.

## Readiness gates
G0: synthetic-only contract tests, mock adapters, matching scenarios and adversarial cases.
G1: independent security/privacy review, partner-specific permissions, audit and idempotency checks.
G2: hosted staging test: token rotation/revocation, tenant isolation, deletion and receipt persistence after reload, backup restore, escalation coverage, and end-to-end approved mock transfer.
G3: signed pilot data sharing agreement, limited field access, verified source system, supervised pilot and measured outcomes.
G4: real customer operations only with explicit founder approval and separate verified billing mode.
Never connect third-party accounts or move real food without explicit authority.

## Integration handoff for other Bruce
The canonical project name is OPERATION OPERATOR. Work on this separate proposal branch, do not change the founder-confirmed Maya website or Academy design, do not merge into main without review. The current `proposal/operational-competence-survey-2026-11-06` PR #106 remains independent. Coordinate through this document; record actual adapters, permissions, tests, and verification with commits. The deliverable is a tested adapter package and operational runbook ready to integrate with Maya, not a claim that any partner is connected.
