# Civic Continuum accountability demonstration
October 13, 2026 (Pacific). First-party local simulation evidence.

## Purpose
Meet human needs, make power traceable, preserve human control, expose failures and remain correctable. This principle is recorded in the founder's earlier Word planning record, "what needs doin.docx", pages 2–4. Transparency must preserve legitimate privacy.

## Run
From repository root:
```sh
python -m demos.accountability_demo
python -m unittest tests.integration.test_accountability_demo tests.integration.test_consent_token_demonstrator -v
```
Observed: 17 tests passed, 0 failed (13 new simulation checks and four existing consent demonstrator tests). These results are local; hosted CI has not been verified. The model is separate from production Maya Node controls.

## What the walkthrough shows
- School: a primary staff member is away; a backup accepts a time-windowed handoff; an unauthorized collector receives a fictional AI approval; the independent permission predicate blocks the proposed pickup and opens a case; backup acknowledgment is simulated at 20 seconds.
- Subscription billing: a revoked charge grant is rejected; the named owner acknowledges at 15 simulated seconds; the affected fictional customer grants a fictional advocate case access; correction remains pending until a separate designated reviewer verifies it.
- Unanswered alerts escalate in the model at 30 and 60 seconds. Under-120-second acknowledgment is a founder target; tests distinguish 119 from 120 seconds. No real human response speed is measured.
- Access is scoped to the particular case. Assignment, action evidence and review are separate.

## Ten-minute adviser walkthrough
1. State the two discovery audiences: school operations and subscription billing teams using AI.
2. Explain technical capability does not confer authority.
3. Run the school scenario and inspect the wrong approval, blocked action and accepted backup.
4. Run the billing scenario and inspect revoked authority, case ownership and correction verification.
5. Show advocate access and explain that actual external delivery needs approved integration.
6. Show test results and remaining gates.
7. Ask which workflow owner to interview first and whether the bounded review would support a buying decision.

## Remaining gaps
This model uses in-memory mutable events and string actor identifiers. It has no authenticated identity, durable/tamper-protected audit storage, live messages, external legal-aid dashboard, payment transport, child-release control or production clock. It cannot locate a person, order an arrest, guarantee a refund or determine liability. Delivery flags are explicitly simulated. Advocate expiry/revocation and case-scoped exports are now modeled and tested. Authentication, protected export delivery and record authenticity remain unimplemented. Evidence preservation, retries, concurrency, input hardening, emergency procedure integration and independent review remain open.

The larger school plan remains an acceptance specification: not every T01–T13 scenario has been implemented. In particular storage/recovery, real identity verification and emergency integration are untested.

Next build: durable authenticated sandbox with grant revocation, accepted roster handoffs, role-limited views, secure evidence export and acknowledgment/escalation delivery adapters. Before any live pilot, agree the workflow, authorization policy, participant access, emergency fallback, data handling and acceptance tests with the participating organization.

## Adviser package
See INITIAL_CUSTOMER_FOCUS.md for the two pitches and discovery questions, and SCHOOL_PICKUP_ACCOUNTABILITY_TEST_PLAN.md for the full written test script and status record.
The preliminary monthly planning target remains $2,500 ($500 operations plus $2,000 provisional owner pay); quotes, startup expenses and customer demand still need validation.

## October 13 follow-up: official-source integration requirements
- NIST AI RMF GOVERN 2 supports clear roles, responsibilities and communication lines: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf
- OWASP recommends denying access by default and checking authorization on every request: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- Stripe requires verified event origins and documents retries: https://docs.stripe.com/webhooks
- Stripe documents duplicate events and event-ID deduplication: https://docs.stripe.com/webhooks/event-notification-handlers
These are design references, not endorsements or certification.

Implementing advocate expiry and revocation is our application of authorization guidance. Two additional local tests verify expired/revoked access denial and exclusion of another case from an export. All 17 selected tests passed.

Next integration specification:
1. Authenticate actors using a maintained identity provider; derive identity from verified sessions rather than request-supplied actor names.
2. Persist cases, grants, handoffs, audit records and delivery outbox transactionally; test restart, write failure, concurrency and reconciliation.
3. Preserve externally protected evidence anchors and define retention/export rules. A local mutable log is insufficient.
4. Distinguish pending, delivered, acknowledged and accepted-for-service notifications. Retry idempotently; never treat delivery as legal representation.
5. Use payment-provider sandbox events with signature checks and duplicate handling. A generic webhook notification is not authority to block a charge; prevention requires enforcement at the actual execution boundary.
6. Connect only approved participating recipients with scoped sharing authority. No real customer data, payments, agency messages or external legal-aid connections were used.
