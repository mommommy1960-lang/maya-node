# School pickup accountability: development record and test script

Date: 2026-10-13 (Pacific). Founder-defined requirements for Civic Continuum / Maya Node.

## Purpose and evidence boundary

Make authority, actions, and response ownership visible when an AI-assisted workflow affects a child. Technical capability does not confer authority. An ID scan alone does not authorize pickup.

This is a written test plan, not an operational child-release system. No school integration, live alerts, authenticated parent dashboard, or response-time guarantee has been demonstrated here. Use only fictional people and records. Existing consent-token tests are component evidence, not evidence of school readiness.

## Current progress

| Item | Status | Evidence / next step |
| --- | --- | --- |
| Authority, consent, revocation, audit and human review foundation | Documented | README.md and tests/integration/test_consent_token_demonstrator.py |
| School pickup and backup requirements | Specified | This plan, based on founder discussion October 13 |
| Independent pickup authorization gate | Proposed | Implement separately from AI approval; test T02–T05 |
| Accepted backup handoff and escalation | Proposed | Implement roster, acknowledgment and timers; test T06–T09 |
| Role-limited accountability display | Proposed | Implement authorized access; test T10 |
| Durable evidence and recovery | Awaiting validation | Test T11–T12 with independent evidence preservation |
| Under-120-second human acknowledgment | Founder target; unvalidated | Measure real acknowledgment in a controlled pilot, not just timer simulation |

A passing component test does not advance a school feature to implemented or validated.

## Required behavior

Before release, independently check verified identity against a current authoritative pickup authorization for the specific child, scope, validity and revocation state. Missing, stale, conflicting or unavailable authorization pauses release for designated staff verification under the school's supervised fallback procedure. AI approval cannot bypass this gate.

The accountability view distinguishes authorization owner, actual approver, actual releasing staff member and current incident lead. Show available backup, escalation route, timestamps and evidence references. Unknown actors must remain explicitly unknown; do not infer identity from an assignment. An assignment identifies a duty, not proof of fault.

Coverage requires an accepted, time-bounded handoff. An unavailable primary cannot remain the only response contact. Record acknowledgment, escalation and coverage failures. A suspected missing child initiates the school's emergency procedure immediately; the response target is not a waiting period.

Expose only necessary information to verified, authorized viewers. Do not publish staff private contacts or child records. Evidence supports review; the system does not determine criminal guilt, arrest, or employment consequences.

## Test setup and procedure

Use child DEMO-CHILD-01; authorized collector DEMO-A; unauthorized collector DEMO-B; primary STAFF-1; backup STAFF-2; incident lead STAFF-3. Use synthetic authorizations and test-only contacts. Record exact revision, configuration, authoritative roster version and time source. In simulation use an injected monotonic clock. Live response testing requires actual delivery and human acknowledgment measurement.

For each case: reset fixture; record expected result; apply stimulus; capture actual gate decision, coverage/display state, alerts, acknowledgment, escalation and audit evidence; mark PASS, FAIL or BLOCKED with reason. Preserve failures and corrections. Do not fill results from expected behavior.

| ID | Stimulus | Required result |
| --- | --- | --- |
| T01 | DEMO-A, current child-specific grant, available staff | Staff verifies pickup; record actual authorization and releasing actor |
| T02 | DEMO-B scans valid ID; AI returns APPROVE | Independent gate blocks release; responsible staff alerted; mismatch recorded |
| T03 | Grant expired, revoked, or for another child (separate runs) | Each run blocks; correct reason recorded |
| T04 | Authorization source stale or unavailable | Pause; staff fallback; no cached AI approval bypass |
| T05 | Revoke grant after initial check but before release | Recheck at release boundary; block revoked grant |
| T06 | STAFF-1 away; STAFF-2 accepted current handoff | Display STAFF-2 as current coverage; preserve historical assignments |
| T07 | Handoff missing, rejected or expired (separate runs) | Flag coverage failure; escalate; do not fabricate acceptance |
| T08 | Primary does not acknowledge | Escalate per configured policy to available backup and lead; record elapsed time and acknowledgments |
| T09 | All contacts unavailable | Expose coverage failure and emergency fallback; do not claim reachable ownership |
| T10 | Authorized parent vs unrelated viewer | Parent sees permitted accountability detail; unrelated viewer denied |
| T11 | Restart, network loss or interrupted audit write | Recover state without silent release or fabricated evidence; mark missing evidence |
| T12 | Attempt audit alteration or forged acknowledgment | Detect/reject according to implemented integrity/authentication design; preserve independent evidence |
| T13 | Suspected missing child | Start emergency workflow immediately; show incident lead and pickup history; no timer delay |

For T08, test acknowledgment at 119 seconds, exactly 120 seconds, and no acknowledgment. The founder's under-two-minute target requires elapsed time <120 seconds. Configure escalation early enough to allow backup response; do not treat sending an alert as human acknowledgment. Deterministic timer tests cannot prove real-world response speed.

## Result template

- Test ID and timestamp:
- Commit / configuration / roster version:
- Operator and environment (simulation or controlled pilot):
- Input and injected fault:
- Expected outcome:
- Actual outcome:
- Evidence references and measured elapsed time:
- PASS / FAIL / BLOCKED:
- Gap, named remediation owner and next verification:
- Reviewer and review date:

School cases T01–T13: NOT RUN. No integrated school implementation is claimed.

## Changelog

### 2026-10-13
- Inspected main-branch docs and tests for pickup, vacation, school and handoff coverage. No school pickup script located.
- Located existing consent demonstrator tests for replay, revocation, restoration and ledger tamper detection.
- Added this written school accountability test plan, result template and status register.
- Next implementation milestone: independent authorization gate, accepted coverage roster, incident escalation, restricted display and durable audit integration.
- Before any live child-related deployment: school policy approval, security/privacy and safety review, controlled acceptance evidence and supervised operational fallback.
