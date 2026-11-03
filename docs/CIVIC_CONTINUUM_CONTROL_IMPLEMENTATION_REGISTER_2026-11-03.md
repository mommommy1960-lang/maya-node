# Civic Continuum Control Implementation Register

**Updated:** 2026-11-03  
**Applies to:** Civic Continuum, Maya Node, SAGE, and company operations  
**Authority:** Founder-adopted Company-Wide Human-First Operating Standards (2026-11-01) and Internal Accountability and Responsible Operations Standard (2026-11-03)

## How to read this register

This is the source of truth for implementation status. Policy adoption is not technical deployment. Source code is not proof of hosted operation. A test plan is not a test result. A control is **VERIFIED** only when current evidence demonstrates the control in the relevant environment.

Statuses:
- **VERIFIED** — current evidence demonstrates the control for the stated scope.
- **PARTIAL** — some implementation exists, but important enforcement, coverage, or environment verification is missing.
- **DOCUMENTED** — written policy or procedure exists; operational effectiveness has not been demonstrated.
- **BLOCKED** — requires access, a human owner, a decision, budget, or external-system verification not presently available.
- **NOT IMPLEMENTED** — no adequate implementation evidence identified.
- **NOT APPLICABLE** — supported by a documented scope decision.

No entry below certifies legal compliance, independent audit, or enterprise readiness.

## Initial status snapshot

| Control domain | Current status | Existing evidence | Remaining gap / acceptance evidence |
|---|---|---|---|
| Truthful claims and evidence | DOCUMENTED | Company-wide operating standards; product readiness and demo documentation | Maintain claim-to-evidence review for each public claim and release; record review date and reviewer |
| Decision authority and least privilege | PARTIAL | RBAC module, consent-token module, permission tests | Verify identity binding, purpose-specific permissions, revocation, expiry, separation of duties, and enforcement in deployed paths |
| Audit trail and provenance | PARTIAL | Hash-chained in-memory ledger and accountability demo | Durable storage, protected independent chain anchor, actor/authority/evidence fields, access controls, retention and tamper tests in target environment |
| Human approval and override | PARTIAL / BLOCKED | HITL request/approve/reject methods and test scaffolding | Actual notification/response mechanism is a TODO; enforce fail-closed behavior for high-impact actions; test timeout, escalation, override, and independent approver |
| Human review / no self-approval | PARTIAL | Accountability demo tests independent correction verification | Map all production workflows; enforce separation of proposer, approver, executor, and verifier where risk requires |
| Customer dignity and continuity | DOCUMENTED | Company-wide policy and consumer-trust documentation | Publish and validate actual terms, notices, export/offboarding path, appeal route, and support coverage; do not claim staffing not present |
| Privacy and data minimization | PARTIAL | Synthetic demo rules, pilot data/incident draft, deletion test plan | Complete data inventory, purpose/legal basis review, access matrix, retention schedule, backup/log expiry, deletion verification |
| Security and secret handling | PARTIAL | SECURITY.md; CI security workflows; RBAC and consent-token code | Current threat model, secret scan evidence, dependency review, access review, incident drill, hosted configuration review |
| Release/change control | PARTIAL | CI workflows and prior CI records | Require approval/change record for production, payment, DNS, credential, database, and customer-data changes; record rollback and post-deploy verification |
| Incident response | DOCUMENTED / PARTIAL | Pilot incident protocol draft and founder alert policy | Backup human owner unfilled; no 24/7 coverage; complete incident workflow and tabletop exercise; agree participant response expectations before pilot |
| Corrective action | PARTIAL | Accountability demo includes correction and separate verification tests | Production issue/case register, named owner, due date, evidence, independent verification, overdue escalation |
| Public claims and customer demos | PARTIAL | Offline workflow lab and demo scope docs | Dated claim review; ensure all interfaces label simulations; no unsupported performance, certification, customer, or readiness claims |
| Vendor/partner controls | DOCUMENTED | Company-wide operating standards | Complete vendor inventory and signed agreements covering access, data, incident notice, subcontracting, exit, deletion, and IP before access |
| Workforce / compensation / anti-retaliation | DOCUMENTED | Company-wide human-first policy | No formal HR, payroll, staffed reporting hotline, or independent investigator evidenced; establish before hiring or making such claims |
| Financial stewardship / continuity | DOCUMENTED | Business viability checkpoint and consumer trust policy | Current cash/runway and obligations register; funded support and continuity plan; no unapproved financial promises |
| Environmental responsibility | DOCUMENTED | Company-wide operating standards | Define material footprint and evidence method before making environmental-benefit claims |
| Independent governance | BLOCKED | Policy requires independent review when leadership is implicated | No independent board, ombudsperson, or investigator evidenced; pause conflicted decisions or obtain independent reviewer |
| SAGE review capability | PARTIAL | Project concept and existing review artifacts | Define production scope, evidence inputs, false-positive handling, human review, audit of SAGE outputs, and test suite |

## Implementation gates

### Gate A — Internal policy and ownership
- [x] Company-wide human-first operating policy exists.
- [x] Internal accountability standard published.
- [ ] Founder confirms named control owners and backup coverage.
- [ ] Create dated quarterly review record.
- [ ] Establish a conflict-of-interest and exception register.

### Gate B — Application-level controls
- [ ] Replace in-memory-only audit assumptions with a durable, access-controlled ledger and independent integrity anchor.
- [ ] Complete HITL approval delivery and response; no production auto-approval.
- [ ] Add explicit action-risk classification and purpose-bound authorization checks to each consequential execution path.
- [ ] Enforce separation of duties for approval and correction verification where required.
- [ ] Ensure every action receipt links actor, authority, evidence reference, policy/version, outcome, and correction case.
- [ ] Add tests for tampering, replay, expired/revoked permissions, unauthorized approver, timeout, missing approver, and partial failure.
- [ ] Add tenant isolation and privacy-safe logging checks to each data path.

### Gate C — Data, security, and customer protections
- [ ] Complete data-flow and data-classification inventory.
- [ ] Approve retention/deletion schedule including database, backups, logs, and derived data.
- [ ] Verify deletion on disposable hosted test data, not production customer data.
- [ ] Complete threat model, dependency review, access review, and incident-response drill.
- [ ] Publish accurate terms for data use, support, interruption, cancellation, export, deletion, and appeals.
- [ ] Confirm customer-facing incident contact and realistic human response window before pilot.

### Gate D — Operational governance
- [ ] Name and confirm a consenting backup human incident owner.
- [ ] Establish independent review route for matters involving the founder.
- [ ] Create incident and corrective-action registers with owners, due dates, and verification evidence.
- [ ] Establish vendor/partner due diligence and written access/data/IP terms.
- [ ] Establish financial obligations, runway, and continuity review.
- [ ] Conduct tabletop exercises for data incident, unauthorized action, service interruption, and customer complaint.

### Gate E — Release and public claims
- [ ] Maintain a release record separating local, CI, staging, and production evidence.
- [ ] Require explicit authorization for production, DNS, payments, secrets, database, and customer-data changes.
- [ ] Test rollback and post-deployment verification.
- [ ] Review public claims and demo labels against current evidence before publication.
- [ ] Keep all demonstrations synthetic unless a separate approved data-use agreement and controls exist.

## Required evidence format

For every control completion, record:
- Control ID and exact scope.
- Commit SHA or deployed version/environment.
- Test or review date.
- Test procedure and expected result.
- Actual result, including failures and skipped steps.
- Evidence URL or protected artifact reference.
- Reviewer and approver.
- Residual risk and next review date.

Never place credentials, tokens, personal data, or confidential customer records in this register or public issue comments.

## Non-negotiable safety boundary

This register authorizes documentation, analysis, tests in isolated synthetic environments, and non-production code changes. It does **not** authorize production deployment, DNS changes, live payment activation, secret rotation, database binding changes, customer-data processing, or contacting a proposed backup person. Those actions require separate explicit authorization and a safe change plan.

## Immediate next sequence

1. Build and test the application-level approval and audit controls in an isolated branch.
2. Map every consequential execution path and bind it to explicit authorization and evidence.
3. Complete the data/security/customer-control evidence before any live pilot.
4. Resolve human coverage and independent-review gaps before making service commitments.
5. Run hosted staging verification only after access and a safe test environment are confirmed.

**Current conclusion:** Civic Continuum has meaningful policy and prototype foundations. It does not yet have evidence that every company control is operational. This register intentionally keeps that distinction visible.
