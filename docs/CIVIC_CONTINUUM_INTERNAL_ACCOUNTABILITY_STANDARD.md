# Civic Continuum Internal Accountability and Responsible Operations Standard

**Status:** Founder-directed operating standard, effective upon publication  
**Scope:** Civic Continuum and its products and services, including Maya Node and SAGE  
**Version:** 1.0  
**Purpose:** Ensure that the company practices the accountability it offers to customers.

> We will not demand accountability from others while exempting ourselves.

This standard is an internal operating commitment. It is not a claim of legal certification, regulatory compliance, independent audit, or completed implementation. Controls must be implemented and evidenced before the company represents them as operational.

## 1. Truthful claims and evidence

- Never describe a prototype as production-ready, a planned feature as available, or an unverified test as passed.
- Label statements as verified fact, customer-reported information, assumption, proposal, or unresolved question.
- Preserve evidence for material product, security, reliability, customer, and business claims.
- Publish limitations alongside demonstrations and customer-facing claims.

## 2. Authority and human responsibility

- Material actions must have an identifiable authorized human or documented system authority.
- AI assistants and agents may recommend or execute only within explicitly granted scope.
- An AI system may not grant itself authority, expand its own permissions, or silently change its operating boundaries.
- Require human approval for high-impact actions involving money, customer access, privacy, security, legal commitments, or production systems unless a separately approved and tested policy explicitly permits a narrower automated action.

## 3. Decision and action records

For material actions, retain a proportionate record of:
- What happened and when.
- The human, role, service, or agent that initiated the action.
- The authority, permission, or policy relied upon.
- The evidence available at decision time.
- Required and completed human reviews.
- The resulting outcome.
- Any exception, incident, correction, owner, and verification.

Records must distinguish original evidence from summaries or AI-generated explanations. Preserve provenance and timestamps where practical. Do not collect or retain unnecessary personal data.

## 4. Human oversight and safe operation

- Define escalation and stop conditions before high-impact workflows go live.
- Provide a practical way for an authorized human to pause, override, or roll back supported operations.
- Do not allow a system to approve its own high-impact action or certify its own correction without independent checks appropriate to the risk.
- Test failure modes, permission boundaries, revocation, replay, and recovery before production use.

## 5. Customer dignity, continuity, and fair dealing

- Explain service scope, limitations, pricing, renewal, suspension, termination, data handling, and support channels in understandable terms.
- Give reasonable notice and a workable export or offboarding path where feasible and lawful.
- Do not abruptly disable access without following disclosed terms and an appropriate safety, security, or legal exception process.
- Treat customer concerns respectfully, document them, and provide a clear route for review and correction.

## 6. Privacy and security

- Use data minimization, least privilege, secure credential handling, and purpose limitation.
- Prefer synthetic or de-identified data for demos, development, and testing.
- Do not request passwords, one-time codes, recovery codes, or private keys in ordinary support conversations.
- Do not expose customer information in public repositories, logs, screenshots, or demonstrations.
- Document retention, deletion, backup, incident response, and access review practices before making commitments about them.

## 7. Verification and release discipline

- A task is complete only when its acceptance criteria and evidence are recorded.
- Separate local test results, CI results, staging results, and production verification.
- Record failed, skipped, blocked, and inconclusive tests accurately.
- Do not make production, DNS, payment, credential, or customer-data changes without the required explicit authorization and change plan.
- Use staged rollout, rollback planning, and post-change verification for material releases.

## 8. Incident response and correction

When an error, security concern, harmful outcome, or material misrepresentation is identified:
1. Protect people and contain ongoing harm.
2. Preserve relevant evidence.
3. Notify the appropriate responsible human.
4. Describe known facts and uncertainties honestly.
5. Assign an owner and due date for corrective action.
6. Verify the correction and document residual risk.
7. Review whether the process or control must change to prevent recurrence.

People raising good-faith concerns must be treated respectfully and must not be punished for reporting them.

## 9. Responsible product design

- Do not build a replacement for an existing system unless discovery demonstrates a real need.
- Prefer interoperability and controlled integration over unnecessary rip-and-replace deployments.
- Validate customer pain, existing alternatives, buyer authority, measurable impact, and willingness to pay before claiming product-market fit.
- Keep human judgment in consequential decisions and avoid presenting automated outputs as certainty.
- Do not claim competitive superiority until independently testable comparisons support the claim.

## 10. Public accountability

- Do not fabricate customers, partnerships, endorsements, testimonials, certifications, compliance status, performance statistics, or deployment results.
- Public documentation must match actual product behavior and current operational readiness.
- Correct material errors promptly and preserve a dated record of significant corrections.

## 11. The Civic Continuum accountability test

Before a material action, ask:

1. Who authorized it?
2. What evidence supports it?
3. What policy or commitment applies?
4. What human review is required?
5. What could go wrong, and how can it be stopped?
6. Who owns the outcome?
7. How will a failure be corrected and independently verified?

## 12. Implementation and review

Publication of this standard does not itself prove that every control is implemented. The company must maintain an implementation register identifying each control, its owner, evidence, status, gaps, and next review date.

At minimum, review this standard quarterly and after a material incident, product change, or change in applicable obligations. Record revisions with dates and reasons.

**Operating promise:** Civic Continuum will build responsibly, communicate honestly, protect the people who trust us, and accept responsibility for the consequences of its decisions.
