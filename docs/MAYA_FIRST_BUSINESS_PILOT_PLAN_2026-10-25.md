# Maya Node First Business Pilot — 2026-10-25

## Decision

**Pilot offer:** Maya Node Permission & Action Receipt for one small service business.

**One-line promise:** Before a defined administrative action is taken, check that the action is explicitly authorized; afterward, produce a readable receipt showing the request, permission result, action outcome, and any failure or human handoff.

This is a proposed pilot scope, not a claim that all of these steps are currently integrated in the hosted site.

## Why this first

Generic chatbots are easy to compare on price. A narrow permission-and-evidence workflow is more aligned with Maya Node's existing demonstrated work: permission checks, create-only file actions, revocation blocking, and saved receipts. Recent industry reporting also highlights agent-caused workflow errors and incomplete audit trails, supporting the problem hypothesis; this is not proof of demand from our own customers.

## Initial customer profile

Recruit **one small service business** that handles repetitive customer/admin requests and currently relies on email, forms, spreadsheets, or manual follow-up. Prefer a low-risk internal or administrative workflow. Do not start with banking, health, housing eligibility, school discipline, payment movement, refunds, or other consequential automated decisions.

No business has agreed to participate yet. A pilot customer must opt in explicitly.

## Pilot workflow

1. The business selects one narrow workflow and writes down the current steps.
2. The business defines the exact actions Maya may prepare or perform, and actions that always require a human.
3. Use synthetic or redacted test data until privacy, retention, access, and deletion controls are verified.
4. Require an explicit, scoped authorization before each supported action.
5. Produce a receipt recording request ID, timestamp, actor/request source, requested action, authorization result, execution result, errors, and human review/escalation.
6. Test revocation, denied authorization, duplicate requests, partial failures, and record review/deletion before any live customer data is used.
7. Compare baseline measurements with pilot measurements and review all failures with the business.

## What the pilot does NOT promise

- It is not a general-purpose AI agent or a legal/compliance certification.
- It does not promise regulatory compliance, zero errors, guaranteed savings, or fully autonomous customer service.
- It does not connect to external business systems or send customer messages unless that integration is separately implemented, reviewed, and explicitly authorized.
- Existing file-action tests and receipts do not prove that the entire hosted customer workflow is production-ready.

## Success measures

Record a baseline first, then compare using the same definitions:

- **Authorization coverage:** supported actions with a recorded authorization decision / all supported action attempts. Target: 100%.
- **Receipt completeness:** completed attempts with all required receipt fields / completed attempts. Target: at least 95% in the pilot, with every missing receipt investigated.
- **Revocation test:** all test attempts after revocation are blocked. Target: 100% of test cases.
- **Unauthorized action test:** all deliberately unauthorized test attempts are blocked. Target: 100% of test cases.
- **Human review:** every out-of-scope, ambiguous, or failed case is held for a human rather than silently treated as complete.
- **Time saved:** compare median handling time against baseline; report the measured result, including no improvement or a negative result.
- **Customer outcome:** business owner rates usefulness and identifies whether they would continue using it. No fabricated testimonial.

A pilot is not considered successful if time improves but permission controls or evidence fail.

## Minimum readiness gates before live use

- [ ] Verify hosted deployment and the exact end-to-end path.
- [ ] Complete customer-controlled record review and deletion verification (previously identified as Check 5).
- [ ] Document data minimization, access, retention, deletion, and incident contact.
- [ ] Run authorization, revocation, duplicate, failure, and receipt-completeness tests.
- [ ] Confirm a named human owner and escalation route.
- [ ] Get written pilot scope and explicit permission from the participating business.
- [ ] Start with synthetic/redacted data; use live data only after the gates are passed.
- [ ] Record baseline and results, including failures and limitations.

## Outreach message (draft; do not send without approval)

> Hi, I'm building Maya Node through Civic Continuum. It is a permission-and-action-record prototype designed to make a narrow administrative workflow easier to review: what was requested, what was authorized, what happened, and where a person needs to step in.
>
> I'm looking for one small business to help evaluate a low-risk workflow using synthetic or redacted data first. This is a limited pilot, not a claim of certified compliance or error-free automation. We'd agree on the workflow, safeguards, and success measures before testing. Would you be open to a short discovery conversation?

## Evidence and positioning

Current repository documentation reports local tests and a working permission-gated file-action demonstration, including revocation blocking and saved receipts. The README also states these are limited prototypes and not yet a live hosted customer service or general-purpose AI integration. Keep public claims within that evidence.

Useful background reading:
- Nylas, *The State of Agentic AI: H2 2026* (published recently; survey reports agent-caused incidents and gaps in full audit logs): https://www.nylas.com/agentic-ai-report-h2-2026/
- Virtualspirit, *How to Audit a Customer-Service Workflow Before AI Automation* (2026): https://virtualspirit.me/insights/369/audit-customer-service-workflow-before-ai-automation

## Status as of 2026-10-25

**Stage:** service definition and pilot protocol drafted.
**Not yet achieved:** recruited pilot business, verified end-to-end hosted production path, passed Check 5, or collected business outcome data.
**Next action:** review this plan against the repository implementation, then approach one prospective design partner only after the founder approves the outreach.
