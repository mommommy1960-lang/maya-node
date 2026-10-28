# Maya readiness execution — October 28, 2026 (Pacific)

**Current result: routine hardening v18 deployed successfully. Demonstration/synthetic testing only; hosting recovery, human backup and physical alert-delivery gates remain open.**

## Identity and preservation
Existing project `appgprj_6ad2958158e88191a37abacacbfe1f45`; native Sites owner access confirmed, public v17 preserved. Saved v17 source is `89b4adb67544d41938217e4fb12873d1169a6093`, deployment `appgdep_6ae16eb5b1e08191a48951d870745f90`. The original editing conversation was opened in Work and its existing Site controls found. Source was opened through the supported managed-Git helper, not reconstructed from the public bootstrap repository.

Backend: Cloudflare Worker/Vinext, D1 binding `DB`; no R2 binding. Live overview confirms request, output, action-event, service-notice and maintenance-run tables. Runtime environment revision 1 has the secret operator identity configured; its value was not printed. Sites dispatch supplies per-Site identity. Website writes check Origin; MCP uses a fixed operation map and cannot grant permission. Exact text-file creation and receipts are real stored server actions. The authority tour and `/lab` are illustrations. No inference, external execution, checkout or subscription is implemented here.

No production source deployment, access/configuration change, customer data read for testing, live deletion, permission grant or fault injection occurred in this continuation. The request-throttle candidate includes an additive counter table, service protection and privacy wording; it was validated and deployed as a routine hardening update to the existing demonstration; publication does not open the customer pilot. No consequential customer launch is authorized by this report.

## Fresh execution
- 82 baseline automated tests passed before the throttle change. The candidate adds four throttle tests plus one stale-counter maintenance test; final validation is recorded below.
- Existing isolated local workerd/D1 integration passed, including migration, export, foreign-access denial, transaction rollback and retention cleanup.
- The new isolated acceptance suite initially passed six child scenarios; the throttle candidate adds a seventh (eight Node test records including the parent): exact-byte baseline/grant reference; queued approval revoked before both execution routes; object substitution; website/MCP concurrency and replay; alternate routes/cross-account denial; exact permission expiry/deletion re-query.
- TypeScript no-emit check passed.
- All integration storage was local and ephemeral, with `remoteBindings:false` and `persist:false`. Named identities A/B are isolated synthetic principals, not newly created real ChatGPT accounts.
- The original six acceptance cases required no repair. The additional abuse-control review identified an absent frequency limit; the candidate adds a transactional counter table and throttle. No production rollout occurred during these checks.

## Authoritative 18-case matrix disposition
Definitions come from the GitHub `MAYA_DELETION_AND_RECEIPT_COMPLETENESS_TEST_PLAN_2026-10-25.md`. PASS below means the stated isolated implementation evidence, not a claim that every case was repeated on hosted disposable accounts today.

| Case | Fresh result and evidence | Hosted/operational limit |
| --- | --- | --- |
| DEL-01 | PASS: SQL and D1 owner deletion removes request/output/linked history | Prior hosted completed deletion evidence retained; no live deletion repeated |
| DEL-02 | PASS: SQL draft/revoked deletion removes linked history, no output | Dedicated new hosted session not repeated |
| DEL-03 | PASS: SQL and D1 foreign deletion denied, safe notices, target intact | Prior live cross-owner read denial; no destructive live cross-account probe |
| DEL-04 | PASS: repeat deletion safely returns 404 | Hosted repeat not repeated |
| DEL-05 | PASS: isolated SQL/D1 injected failure rolls back all in-scope data | Never inject storage faults in production |
| DEL-06 | PASS: SQL/D1 fresh requests and export cannot recover deleted record | New real identity-provider session expiration not exercised |
| DEL-07 | PARTIAL/BLOCKED: active retention/legacy preservation tested; live operator cleanup verified | Actual hosting backup/log expiry and hosted restore unverified |
| DEL-08 | PASS: unrelated requests/outputs/receipts preserved | Prior hosted preservation evidence retained |
| REC-01 | PASS: exact bytes/hash/count, correct grant/output linkage in SQL/D1 | Existing hosted output/export evidence retained |
| REC-02 | PASS: missing permission creates denial, no output | No new hosted attempt required to repeat earlier evidence |
| REC-03 | PASS: revoke-before-dispatch denies website and MCP, no output | No peer-system result inferred |
| REC-04 | PASS: exact five-minute expiry blocks output with correct reason | Physical waiting/UI test not repeated |
| REC-05 | PASS: concurrent website/MCP execution produces one output and one success; replays denied | No broad load test or platform abuse guarantee |
| REC-06 | PASS: output/storage failure rolls back and records handoff if storage permits | Complete outage truthfully cannot promise receipt persistence |
| REC-07 | PASS: receipt insertion failure rolls back output/transition | Local fault injection only |
| REC-08 | PASS: durable review reference without execution | Reference is not a sent message, staffed ticket or delivered notification |
| REC-09 | PASS: account-scoped SQL/D1 exports and foreign attempts reveal no target | Not every hosted endpoint was retested using two real sessions |
| REC-10 | PASS: stored/exported metadata consistency, repeat export, >200 events, explicit overflow | Service-controlled and unsigned; no independent tamper-proof guarantee |

## Customer experience
Isolated browser preview rendered the signed-out public page in 375- and 800-pixel iframe widths. Document client/scroll widths were 360/360 and 785/785 (scrollbars consume 15px); no horizontal document overflow in those views. Protections, scope, sign-in, tester instructions, retention limits and contact route were present. The revoked tour visibly reported blocked execution and clearly identified itself as illustrative. This is a responsive desktop-browser check, not a physical Android acceptance test or signed-in mobile download test. Earlier founder tablet download/open evidence remains valid within its scope.

## Privacy and operational findings
Application stores per-Site user ID, filename, exact user text, SHA-256, request state/timestamps/permission nonce, saved output, linked action receipts and minimal denial/review notices. Signed-in email is used from dispatch for access/UI, not persisted in the action tables. Operator maintenance audit records actor ID plus aggregate counts, not payloads. Service operator/hosting provider can access stored service data; account routes isolate ordinary users. New records expire after 30 days; NULL-deadline legacy data remains until owner deletion. Owner deletion removes active request/output/linked receipts; local downloads remain on devices. Hosting logs/backups are a separate unverified copy/retention boundary.

Current application limits: 4,096-byte text, 16,384-byte request body, 50 records per owner, 10,000 global records, bounded receipt export. The live v17 service has no application request-frequency throttle; repeated denied operations can grow receipts. The candidate now adds per-identity fixed-minute limits of 60 ordinary writes, 240 reads and a separate 120 revoke/delete control budget, shared by website and MCP. Rejected operations return 429/Retry-After without creating another receipt or performing an action. Counters hold only identity/scope/minute/count; stale windows are removed on subsequent traffic or operator maintenance. Concurrency, recovery, account separation, no-effect throttling and counter-failure handling are tested. This is not upstream DDoS protection or a rolling-window guarantee. Until publication and hosted verification are recorded, the live rate-limit gap remains open.

The scheduled cleanup completed with run `5c4451cc-e7c4-44ee-a9d5-3af85b03e6f8`, matching persisted status; removed counts 0/0/0/0; pending expiry 0; legacy/unexpired records preserved. Daily task remains enabled.

Support case 17489131 contains the sent request for actual D1 backup/PITR and log expiry, deleted-data resurrection prevention, isolated hosted restoration and evidence/cost/approval. No answer supplying those facts was found. The connected toolset offers no backup/restore control. A local D1 rollback/migration test is not hosting recovery evidence.

Primary human responder: founder, acceptance already recorded. No backup has consented. No duty hours or acknowledgement guarantee is established. Event-triggered incident check is enabled and has completed recorded runs; delivery status is unknown, so physical tablet receipt is unverified.

## Reviewable next steps requiring external participation
1. Hosting provider supplies actual retention settings and a supported isolated synthetic restore path. Record restore checkpoint/time, pre-restore hash/count manifest, successful isolated restoration, account separation, expiry/deletion reconciliation and operator-visible recovery evidence. Obtain any required cost/risk approval before execution; never restore into the live database.
2. Founder nominates a willing backup. Obtain explicit acceptance, contact route, coverage windows, authority limits and a safe handoff drill. Proposed role receives sanitized incident summaries, contacts the founder and follows the agreed triage plan; no automatic admin, mailbox or financial access.
3. Conduct a clearly labelled alert-delivery test using a supported test path. Founder confirms notification permissions on the actual tablet and records send/arrival/open times and visible notification. A completed cloud task alone is not delivery evidence. No synthetic incident email was sent, alert prompt changed or production fault created here.
4. Keep the peer comparison conditional on accessible exact-source material, written scope and participant permission. Do not substitute another source revision or claim completed joint testing. Record expected/actual effects and feedback independently.
5. Verify the tested request-throttle release and its additive migration before expanding traffic. Keep real customer/sensitive data out of scope while readiness gaps remain.

## Decision
Demonstration and bounded synthetic testing only. Not production ready, and no independently completed external controlled pilot is claimed. Hosting recovery, real device delivery, human backup/coverage, verified abuse protection and participant authorization remain open. Do not repeat resolved source recovery or basic two-account work as a prerequisite.

## Final prepublication validation
87 automated tests passed, including five new frequency/cleanup cases. The existing local D1 integration passed. The new acceptance suite passed seven child scenarios (eight Node records including the harness). TypeScript passed. The additive migration creates only maya_rate_windows and its expiry index; existing action schema and retention deadlines are unchanged. Build and any deployment evidence are recorded separately. Rollback can redeploy v17 without dropping this additive table; that restores the old unthrottled behavior, so document the regression and arrange approved counter cleanup if necessary. Never roll back the database by overwriting customer data.

## Verified release evidence
- v18 source commit: `e6831dd5012fe6ce0e0ec8c81677631cc174e033`.
- Saved version: `appgprj_6ad2958158e88191a37abacacbfe1f45~appgver_a71bd9fb34f88191a512fb8ec55edba9`.
- Deployment: `appgdep_6ae25787a8f081919864b7eae59f3c15`, **succeeded**, environment revision 1; original public audience preserved.
- URL: https://maya-working-workflow-lab.myqueen1960.chatgpt.site
- Additive migration `0003_overconfident_ironclad.sql` creates only the counter table/index. Fresh live D1 overview confirms it exists alongside all original action/service/maintenance tables.
- Fresh live server receipt download parsed as v2: 10 original requests, 28 action events, one existing service notice, five completed-output references. No payload text/email fields appeared in action receipts. No existing action record was deleted or modified by this continuation.
- Connected maintenance status still returns the matching morning run and zero pending expiry. No extra cleanup was invoked.
- Recent error-only Worker-log query returned zero events; this is a bounded observation, not a future reliability guarantee.
- Public GitHub Security & Ethics run [40757849954](https://github.com/mommommy1960-lang/maya-node/actions/runs/40757849954) passed on documentation commit `69780e6c67984f404ed61d8567172df2901bd743`. It is separate from the actual Site's 87 tests, local D1 suites, TypeScript and production build; it does not certify the hosted service.
- Local source checkout is clean after supported helper push/package. UI responsive fixture was temporary and removed before build; no test page or alternate auth route was published.

This section supersedes prepublication/candidate wording above. The application's frequency-limit gap is fixed in v18; infrastructure-level DDoS defenses remain unverified. No customer-pilot launch, billing activation, real-customer-data migration, hosted backup restoration or appointment of a backup person occurred.
