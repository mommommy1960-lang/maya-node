# Accountability Controls Implementation Register

**Status:** Active implementation register; evidence-based, not a certification.
**Updated:** 2026-11-03
**Rule:** Documentation is not implementation. A control is only complete when its acceptance evidence is linked and independently checked.

| Control family | Current evidence | Status | Required closure evidence |
|---|---|---|---|
| Human approval gate | `src/sovereign/approval_gate.py`; unit tests added in `tests/unit/test_approval_gate.py` | Code added; CI not yet run | CI pass, integration into every consequential action path, authenticated approver adapter, durable audit sink, operational alerting and named human coverage |
| Existing HITL module | `src/sovereign/hitl.py` contains legacy implementation and a TODO notification mechanism | Open | Replace or safely adapt legacy callers to the new gate; compatibility tests; notification/response integration |
| Audit ledger | `src/services/ledger/ledger.py` provides an in-memory hash chain and process-local trusted head | Partial | Durable append-only storage, independent external head anchoring, concurrency and crash recovery tests, access controls, retention and restore drill |
| Role-based access | `src/services/access/rbac.py` contains in-memory roles and assignments | Partial | Persistent identity integration, least-privilege policy, deny-by-default checks on every route/action, revocation and tenant-isolation tests, admin separation |
| Consent tokens | `src/sovereign/consent_tokens.py` provides HMAC token operations and in-memory state | Partial | Secret manager integration, durable atomic single-use/revocation state, audience/issuer binding, key rotation, replay/concurrency tests |
| Ethics and transparency | `src/sovereign/ethics_engine.py` includes heuristic text matching and placeholder transparency/autonomy checks | Open | Replace keyword heuristics with typed policy rules and threat model; avoid false positives; enforce at execution boundaries; independent tests |
| Data privacy and retention | Existing deletion/receipt test plan documents intended tests | Open | Data inventory, lawful purpose, field minimization, retention/deletion enforcement, backup expiry, access logging, restore/deletion verification |
| Incident response | Policy documentation exists | Documentation only | Named primary and backup responders, staffed channel, severity matrix, alert delivery test, escalation exercise, incident records and postmortems |
| Customer continuity and remedies | Policy documentation exists | Documentation only | Approved customer terms, export/offboarding workflow, notice templates, appeal route, tested data preservation and deletion |
| Vendor governance | Policy documentation exists | Documentation only | Vendor inventory, due diligence, signed agreements, access review, incident notice and exit evidence |
| Workforce and speak-up | Company policy states principles; no evidence of staffed HR/reporting infrastructure | Not operationally verified | Lawful employment processes, accessible reporting route, non-retaliation process, named impartial reviewer and backup |
| Finance and incentives | Policy documentation exists | Not operationally verified | Budget/runway controls, approval thresholds, accounting reconciliation, funded compensation plans and anti-gaming review |
| Environmental responsibility | Policy documentation exists | Not measured | Defined material impacts, baseline, boundary, measurement method and review evidence |
| Release/change safety | Existing repository CI and deployment records | Partial | Required branch protections, CI gates, signed release evidence, staging and production verification, rollback exercise |
| Public claims | Documentation standard exists | Open | Claim inventory with evidence links, product limitation disclosures, review owner and correction log |

## Mandatory stop conditions

Do not enable production mutation, live payments, outbound mail, customer-data processing, or consequential automated decisions until the relevant controls above have passed their acceptance criteria. Existing production safety settings must remain unchanged absent explicit founder authorization and a reviewed change plan.

## Immediate engineering sequence

1. Run the new approval-gate tests and resolve import/test-discovery issues.
2. Integrate the gate into each consequential execution path; tests must prove no path can bypass it.
3. Add authenticated identity and durable audit adapters; fail closed if either is unavailable.
4. Replace placeholder ethics checks with structured, testable policies.
5. Add persistent storage, tenant isolation, deletion/retention, incident, and recovery tests.
6. Complete operational human coverage, legal review, customer terms, vendor and workforce processes.
7. Verify deployment in staging and production only under separately approved change controls.

## Evidence rule

A source file, passing unit test, draft policy, or GitHub issue is not proof of hosted operation, staffed coverage, legal compliance, or customer readiness. Keep each status separate.
