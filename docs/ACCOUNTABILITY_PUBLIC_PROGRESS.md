# Civic Continuum / Maya Node: public development record
Date: October 13, 2026 (America/Los_Angeles). Update recorded around 16:11 Pacific.
Owner: Mya P. Brown. Draft work: https://github.com/mommommy1960-lang/maya-node/pull/61

## Why
Make authority, responsibility and correction visible in AI-assisted workflows. Initial discovery audiences: school operations and subscription-billing teams using AI. An affected person should have a named response owner without needing to settle fault before assistance begins.

## What we built and how
| Stage | Method / artifact | Observed evidence | Limit |
| --- | --- | --- | --- |
| Requirements | School pickup plan and founder-defined backup/response targets | Written cases and result template | No verified pickup deployment |
| Model | Independent scope/expiry/revocation predicate, accepted backup, case ownership, advocate access, correction review | First 11 checks; four existing consent checks | Synthetic in-memory actors and events |
| Access extension | Expiring/revocable advocate grant and case-isolated export | 13 model + four consent checks = 17 | No real identity or secure delivery |
| Local sandbox | SQLite snapshots, operator-provisioned credentials, HMAC state check, case/outbox transaction, retry states | Seven sandbox + prior 17 = 24 | Single worker; session/outbox tamper protections incomplete |
| Boundary sweep | All 128 seven-flag combinations plus 1,000 seeded random cases per sector | 1,128 school + 1,128 billing decisions matched expected labels | Model correctness, not field reliability |
| Public-record fixtures | FTC ABCmouse and Edmodo records; CFPB revocation rules; synthetic abstractions | Four new scenario checks; 28 selected tests passed | No historical-system replay, AI-use finding or compliance certification |

The counts are chronological scoped results, not numbers of real customers or independent field trials. Do not combine unit checks with scenario sweeps into one reliability denominator.

## Sources and reproduction
- [School test plan](SCHOOL_PICKUP_ACCOUNTABILITY_TEST_PLAN.md)
- [Customer roles and pitches](INITIAL_CUSTOMER_FOCUS.md)
- [Demo results](ACCOUNTABILITY_DEMO_RESULTS.md)
- [Sandbox scope and limitations](ACCOUNTABILITY_SANDBOX.md)
- [Boundary evaluation](ACCOUNTABILITY_EVALUATION_2026-10-13.md)
- [Public-record scenarios and official links](PUBLIC_RECORD_SCENARIO_REGISTER.md)

From repository root:
```sh
python -m demos.accountability_demo
python -m demos.evaluate_accountability
python -m unittest tests.integration.test_public_record_scenarios tests.integration.test_accountability_sandbox tests.integration.test_accountability_demo tests.integration.test_consent_token_demonstrator -v
```
Boundary seed: 20261013. Expected labels derive from injected fault flags separately from the permission function. Tests use fictional data and injected clocks; alert delivery uses a test adapter. No external organization was contacted through the sandbox.

## Corrections preserved
- Earlier wording about founder contact could be confused with operational response. Revised requirement: the purchasing organization assigns its incident owner, accepted backup and escalation recipients. Founder contact on discovery material is for research replies only. The earlier packet and its explicit correction were retained in adviser correspondence.
- Buyer-assigned operational response does not eliminate provider duties for its software, defects or applicable obligations. Responsibilities need a role map, not a blanket disclaimer.
- A short pilot or synthetic pass rate does not establish 99% field reliability. The published evaluation protocol defines conditional sampling assumptions and separate safety stop conditions.
- An interrupted tool response created uncertainty about saving public-record work. Follow-up reads confirmed both the test module and scenario register exist on this draft branch. No duplicate was created.

## What the research revealed
- Base/add-on cancellation authority must be modeled separately.
- Educational use does not grant advertising authority.
- Revoked charge authority must stay blocked on resubmission.
- Repeated attempts currently create separate cases; stable incident grouping remains open.
- Cancellation-login traps need an alternate protected dispute route; the grant predicate alone is insufficient.
- No primary public pickup incident was located. Do not represent the founder-defined school pickup scenario as a documented incident.

## Remaining gates
No managed identity provider, live school/payment/legal-aid integration, actual human-response measurement, immutable evidence, independent assessment or verified hosted CI result. State HMAC does not prevent rollback/key compromise; outbox/session tables can be altered by a database-controlling actor; concurrent snapshot writers are unsupported.

Next: incident grouping, verified external source adapters, protected alternate intake, multi-user transaction controls, externally anchored evidence and measured notification/human acknowledgment. Representative partner trials require an agreed workflow and actual operating conditions; internet sources cannot replace them.

Transparency covers methods, evidence, corrections and limitations. Private customer records, credentials, private correspondence and protected invention material are not public progress artifacts.
