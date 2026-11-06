# MAYA NODE | Operational Competence Academy
## Staff onboarding v0.1 — synthetic training only
**Audience:** pantry coordinators, dispatchers, receiving staff, supervisors, and organization administrators.
**Release boundary:** This is training material for a synthetic demonstration, not evidence that Maya Node is approved for customer data, live inventory integrations, calls, texts, or billing. Adapt with each partner's written permission and approved policies before real use.

### Learning outcomes
After training, staff can identify an authorized case, propose a food transfer, distinguish suggestions from approved actions, recognize escalation triggers, record delivery evidence, and report a privacy or safety incident. Supervisors can review audit events and reject unverified approvals.

### 60-minute guided session
- **0–10 minutes: Orientation.** What Maya does: detect, connect, request human approval, verify, document. What Maya does not do: override consent, assume inventory ownership, independently authorize transfers, or contact people without approved configuration.
- **10–20 minutes: Roles and permissions.** Operator versus named approver; never share credentials. Require organization-specific account setup and role mapping before launch.
- **20–35 minutes: Simulated transfer.** Create a fictional case for 50 boxes of tomatoes at Demo Pantry A; propose Demo Pantry B; review transport and cold-chain constraints; require an authenticated approver; dispatch only after approval.
- **35–45 minutes: Exceptions.** Simulate overdue pickup, unavailable driver, rejected proposal, missing delivery confirmation, and privacy complaint. Escalate to a named human; never mark a case delivered without evidence.
- **45–55 minutes: Audit and receipts.** Read event history; verify who approved and when; distinguish self-attestation from independently verified evidence; identify suspicious changes.
- **55–60 minutes: Knowledge check and support.** Practice emergency stop and reporting; gather feedback.

### Role-specific quick guides
**Pantry staff:** enter only permitted inventory details; check quantity, condition, expiry, temperature needs, pickup window; do not enter personal information in free text; flag discrepancies.
**Coordinator:** review recipient suitability and logistics; make a proposal; obtain authorized approval; monitor deadlines; escalate failures.
**Approver:** independently confirm recipient, quantity, transport, safety, and authorization; approve or reject using own credentials; never approve blindly.
**Receiving staff:** verify actual quantity and condition; record delivery receipt and exceptions; do not confirm delivery on a promise alone.
**Administrator:** assign/revoke access; maintain escalation contacts and backup owner; inspect audit and retention settings; arrange training and periodic drills.

### Guided practice: synthetic case
1. Sign into a *training-only* environment with individually assigned training credentials.
2. Open a fictional case; confirm it contains no real customer or beneficiary information.
3. Propose transfer and inspect missing logistics details.
4. Have a different authorized training approver approve; demonstrate that an operator-only request fails.
5. Supply fictional recipient and transport details; dispatch with required approval.
6. Confirm fictional delivery using an explicit simulated evidence record. Note: current prototype only stores an attestation; real receipt persistence and proof remain a release blocker.
7. Review audit events and name the approver.
8. Simulate a late pickup; inspect escalation queue and assign a human owner.

### Knowledge check (pass: 5/5 plus supervised practical demonstration)
1. May Maya send a transfer automatically because a case is urgent? **No; authorized human approval is required.**
2. Can staff share approver credentials? **No.**
3. What happens when a delivery is late? **Escalate to named human; preserve event history.**
4. Does a delivery status alone prove food arrived? **No; verify independent receipt/evidence.**
5. May real pantry data be used in the current demonstration? **No; synthetic-only until explicit gates pass.**

### Training completion record (do not store personal data in public repositories)
Organization: ____ | Role: ____ | Training date: ____ | Trainer: ____ | Quiz score: ____ | Practical demonstration: pass/fail | Access approved by: ____ | Refresher due: ____
Store completed records only in the organization's authorized system.

### Launch requirements before selling or deploying
- Written partner permission, data-use agreement, privacy/retention/deletion controls, incident response and named backup owner.
- Individual authentication and least-privilege access; no shared operator or approver tokens.
- Verified inventory connector scope, calls/SMS opt-in and rate limits, and human escalation coverage.
- Staging end-to-end test: survey consent, secure submission, approvals, persistent audit and receipts, delivery proof, overdue monitoring, and QR redirect.
- Accessibility review, translated materials reviewed by fluent speakers, hands-on training, support contact, and refresher cadence.
- Real customer data and live billing remain **NO-GO** until all gates have evidence and founder approval.

### Research attribution
Civic Continuum's food-rescue operations research is informed by the Washington State Department of Ecology's *The Last Mile* study. This does not imply agency endorsement or partnership.

### Training product packaging
Offer an onboarding workshop, role-based micro-lessons, printable one-page guides, a supervised sandbox exercise, knowledge check, and 30-day refresher. Pricing and service commitments are TBD, not advertised.
