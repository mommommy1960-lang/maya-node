# CIVIC CONTINUUM — Maya Node as an AI accountability foundation

**Advancing the Commons Initiative · contact@civiccontinuum.org**

## The full concept
Maya is intended as a reusable governance layer between AI/tool requests and consequential execution. It connects identity and provenance, permission, execution-time checks, preserved evidence, accountable response, human challenge, safe stopping and controlled recovery. The sector demos illustrate parts of that chain; they are not the whole architecture.

| Layer | Intended function | Current evidence / next gate |
|---|---|---|
| Identity and provenance | Identify the actor, organization, model/tool version and source of an assertion | Keys/signatures and actor concepts exist; trusted issuer integration and deployed identity remain open |
| Licensing and conditions | Record the applicable use terms and check a specified issuer's credential when required | Legacy CERL/node-access concepts; no universal AI legal-legitimacy certification or deployed external credential registry |
| Consent and delegation | Bind permission to an operation, person, purpose, resource, duration and withdrawal path | Existing consent-token and scoped-grant implementations; unified contract and resource-bound integration remain incomplete |
| Enforcement before execution | Recheck authority when the action runs; reject revoked, expired or frozen grants | Local token/model tests; live adapters and bypass resistance remain open |
| Evidence and audit | Preserve what was requested, authorized, attempted, blocked and changed | Local hash-linked ledger and case evidence; protected durable operation and outside anchoring remain open |
| Responsibility and escalation | Name an empowered responder, accepted backup and escalation route | Fictional/local models; real delivery and human acknowledgement need a partner pilot |
| Challenge and remedy | Let affected people understand decisions, grant limited advocate access and obtain separately reviewed correction | Local case/advocate controls and fictional receipt; real remedy and usability not validated |
| Safe stop and recovery | Freeze, reduce privilege and restore only under fresh authority | Consent freeze/restore exists; hardening in PR70; cross-system recovery remains open |
| Interoperability and assurance | Let different vendors implement a common contract and pass published negative tests | CUP/SAGE concepts exist; inspected CUP phi-schema.json is blank, so it is not a finished interoperable specification |

## A global foundation is a direction to earn
The goal is an adoptable, testable accountability contract that different AI products can implement and people can independently inspect. Being universally mandatory, number one or larger than Amazon has not been established and cannot be promised. A sole compulsory private gate would concentrate power; Commons anti-capture principles call for transparent rules, independent review and meaningful exit. Commercial rights and compatibility terms also need explicit resolution before broad third-party adoption.

Trust must be evidence-backed and scoped: documented guarantees, adversarial tests, published failures/corrections, protected enforcement, operating reliability, independent reproduction and measured outcomes. A bounded passing test is not proof that every future input or deployment succeeds.

## Concrete foundation repair completed locally
Original consent code allowed session/batch tokens to restore a frozen token and accepted tokens at the exact expiry boundary. New tests reproduced those behaviors. The patch requires single-operation restoration permission, rejects expired restoration targets, closes expiry at the deadline, validates positive finite TTL and uses hmac.compare_digest with malformed-signature rejection. After repair,19 runtime checks and4 existing integration/ledger checks pass. These are separate from the earlier23 Node checks for the browser lab.

[Consent repair PR70](https://github.com/mommommy1960-lang/maya-node/pull/70) is proposed code, not deployed production. Process-local mutable state, durable atomic consumption, actual identity, adapter enforcement and independent security review remain open. [Portable lab PR69](https://github.com/mommommy1960-lang/maya-node/pull/69) remains separate.

## Next engineering milestone
Freeze one versioned action/decision/evidence contract against the existing token, ledger and case modules; implement one test-only adapter; run shared negative cases through two independent callers before expanding sectors. This is planned work, not completed interoperability. Business and technical advising will review this direction; no adviser approval or scheduled meeting is claimed.

## Source trail
- docs/HUMAN_AUTHORITY_AI_ALIGNMENT_BRIEF_2026-09-21.md
- docs/AI_GOVERNANCE_ACCOUNTABILITY_EVIDENCE_MAP_2026-09-21.md
- docs/CONSENT_TOKEN_SUPERVISED_DEMONSTRATION_PROTOCOL.md
- src/sovereign/consent_tokens.py ; src/services/ledger/ledger.py ; demos/accountability_demo.py
- Commons-Unified-Protocol/spec/cup-auth.md and spec/phi-schema.json (inspected main)

No endorsement, universal requirement, certification, competitor superiority or guaranteed financial outcome is implied.
