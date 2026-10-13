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
Observed: 15 tests passed, 0 failed (11 new simulation checks and four existing consent demonstrator tests). These results are local; hosted CI has not been verified. The model is separate from production Maya Node controls.

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
This model uses in-memory mutable events and string actor identifiers. It has no authenticated identity, durable/tamper-protected audit storage, live messages, external legal-aid dashboard, payment transport, child-release control or production clock. It cannot locate a person, order an arrest, guarantee a refund or determine liability. Delivery flags are explicitly simulated. Advocate access expiry/revocation and secure exports remain unimplemented. Evidence preservation, retries, concurrency, input hardening, emergency procedure integration and independent review remain open.

The larger school plan remains an acceptance specification: not every T01–T13 scenario has been implemented. In particular storage/recovery, real identity verification and emergency integration are untested.

Next build: durable authenticated sandbox with grant revocation, accepted roster handoffs, role-limited views, secure evidence export and acknowledgment/escalation delivery adapters. Before any live pilot, agree the workflow, authorization policy, participant access, emergency fallback, data handling and acceptance tests with the participating organization.

## Adviser package
See INITIAL_CUSTOMER_FOCUS.md for the two pitches and discovery questions, and SCHOOL_PICKUP_ACCOUNTABILITY_TEST_PLAN.md for the full written test script and status record.
The preliminary monthly planning target remains $2,500 ($500 operations plus $2,000 provisional owner pay); quotes, startup expenses and customer demand still need validation.
