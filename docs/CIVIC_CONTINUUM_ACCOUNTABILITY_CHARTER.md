# Civic Continuum Accountability Charter
**Status:** Proposed company standard  
**Date:** November 3, 2026  
**Applies to:** Civic Continuum, Maya Node, SAGE, employees, contractors, agents, and customer-facing work

## Our commitment

Civic Continuum will practice the accountability it asks other organizations to adopt. We will make consequential decisions traceable, explain what we know and do not know, protect people and their information, assign human responsibility, correct mistakes, and verify that corrections are complete.

We will not describe aspirations as delivered capabilities, tests as production readiness, demonstrations as customer deployments, or assumptions as verified facts.

## The operating standard

For every consequential company or product action, preserve an understandable chain:

**ACTION → AUTHORITY → EVIDENCE → HUMAN OVERSIGHT → OUTCOME → CORRECTION**

1. **Action:** What happened, when, and in which system?
2. **Authority:** Who or what initiated it, under which role, permission, policy, and approved purpose?
3. **Evidence:** What source material supported it? Distinguish verified records, user statements, assumptions, and AI-generated content.
4. **Human oversight:** What review was required, who performed it, and what did they decide? Do not represent automated review as human approval.
5. **Outcome:** What actually happened? Record failures and uncertainty rather than filling gaps with guesses.
6. **Correction:** Who owns the remedy, what changed, and what evidence verifies completion?

## Company principles

### Truthful claims
- Label capabilities as proposed, in development, locally tested, independently tested, hosted-tested, or production-validated.
- Publish the scope, date, environment, and limitations of material test results.
- Never claim customer adoption, integrations, certifications, compliance, uptime, or security assurance without evidence.
- Correct public and customer-facing inaccuracies promptly and preserve a record of material corrections.

### Human responsibility
- Name a responsible human owner for consequential decisions and customer commitments.
- Keep human approval explicit where policy, law, safety, or customer agreement requires it.
- Provide a clear path to pause, challenge, escalate, and reverse actions where technically and operationally possible.
- Do not let an AI agent authorize its own expanded permissions or certify its own compliance.

### Privacy and security
- Collect only information needed for a defined purpose; minimize retention and restrict access.
- Use synthetic data for demonstrations and early tests unless a separately approved data-protection plan permits otherwise.
- Never request or store customer passwords, one-time codes, recovery codes, or secret keys in ordinary project records.
- Document access, retention, deletion, backup, incident response, and recovery procedures before handling sensitive customer data.
- Do not change production traffic, DNS, secrets, databases, payment activation, or customer data without explicit authorization and a reviewed change plan.

### Customer respect and continuity
- Do not replace existing customer systems merely to make our product central.
- Explain integrations, dependencies, limitations, costs, data handling, and exit options before commitment.
- Give clear notice of material service changes and provide a reasonable, documented path to retrieve customer data and transition where applicable.
- Do not abruptly withdraw paid access or strand customer work without a documented, fair process, subject to lawful security and safety exceptions.
- Do not imply that a discovery conversation is a pilot, partnership, endorsement, or purchase.

### Learning and correction
- Treat incidents, complaints, failed tests, and customer feedback as evidence to investigate, not reputational threats to hide.
- Record severity, impact, owner, containment, root-cause status, corrective action, and verification.
- Distinguish confirmed root cause from a working hypothesis.
- Close corrective actions only when completion evidence is recorded and reviewed.

## Product design requirements

### Maya Node — controlled workflow and evidence engine
Maya Node should help organizations define permitted workflows, enforce scoped permissions, record consequential actions, preserve supporting evidence, and make handoffs and exceptions traceable. It must fail safely when required authority or evidence is missing. It must not silently convert a missing approval into an approval.

### SAGE — review and verification engine
SAGE should examine records for missing authority, inconsistent evidence, policy conflicts, unresolved exceptions, overdue corrective actions, and gaps between claimed and observed outcomes. It should show its sources and uncertainty, route findings to accountable humans, and never present a flag as proof of misconduct.

### Civic Continuum — accountability framework
Civic Continuum should connect organizational purpose, policies, people, systems, evidence, oversight, outcomes, and remedies. It should complement existing systems through controlled integrations rather than claim to replace established operational, security, audit, or governance platforms.

## Evidence and assurance levels

Use these labels consistently:
- **Proposed:** design or intention only.
- **In development:** implementation is underway; not yet demonstrated end to end.
- **Locally tested:** passed a stated test in a local or isolated environment.
- **Hosted-tested:** passed a stated test in a hosted environment.
- **Production-validated:** verified in the actual production context against documented acceptance criteria.
- **Customer-accepted:** a named customer has reviewed and accepted a defined scope; this does not imply broader endorsement.

Every material claim should link to dated evidence, its environment, acceptance criteria, limitations, and an owner. A green CI result alone does not establish customer readiness, operational coverage, security assurance, or production acceptance.

## Required gates before a customer pilot

No pilot involving real organizational data or consequential workflows begins until the company has documented:
1. The customer's problem, desired outcome, system boundaries, and success measures.
2. A named customer sponsor, operational owner, technical owner, and escalation contact.
3. Written scope, permissions, human-approval points, prohibited actions, and rollback/stop conditions.
4. Data classification, minimum necessary access, retention, deletion, backup, and incident procedures.
5. Test evidence for authorization, denial, revocation, expiry, replay, isolation, failure handling, and recovery as relevant to the scope.
6. Monitoring, human support coverage, response expectations, and a customer communication plan.
7. Acceptance criteria and a written record of customer approval to proceed.

A synthetic demonstration is not a pilot. A pilot is not production readiness. Each transition requires its own evidence and approval.

## Company accountability record

For each material decision, maintain a record with:
- Decision or action ID and timestamp
- Decision owner and accountable reviewer
- Purpose, authority, and applicable policy
- Evidence links and source classifications
- AI or automation involvement and relevant model/system version
- Human review and approval status
- Outcome, uncertainty, and impact
- Exceptions, incident references, and corrective-action owner
- Verification evidence and closure date

Access to these records must be role-limited and retention must be defined. Do not put secrets or unnecessary personal data in the log.

## Measures we will review

At a regular operating review, examine:
- Percentage of consequential actions with complete authority and evidence records
- Missing or late human approvals
- Unresolved exceptions and age of corrective actions
- Time to detect, contain, communicate, and correct incidents
- Deletion and recovery test results
- Customer-reported workflow friction and verified customer outcomes
- Claims that lack current supporting evidence
- Access changes and production changes with documented authorization

Metrics must include definitions, denominators, time periods, and known gaps. We will not optimize a score at the expense of truthful reporting.

## Governance and change control

This charter is a proposed baseline until the founder formally adopts it. Changes must be versioned, dated, explained, and approved by the accountable company owner. Exceptions must identify the reason, scope, approver, duration, compensating controls, and review date. No exception may waive applicable law or a customer's explicit safety or data-protection requirements.

## Our public promise

**We will not ask customers to trust a claim that we cannot explain and support with evidence. We will not ask customers to be accountable while exempting ourselves. When we make a mistake, we will say what happened, take responsibility, correct it, and show how we verified the correction.**

---
*This charter is an internal operating standard proposal, not a legal opinion, certification, compliance attestation, or claim that the described product capabilities have already been implemented.*
