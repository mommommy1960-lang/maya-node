# Maya Node Deletion Source Inventory — 2026-10-27

## Purpose
Locate the implementation that owns customer-request deletion before changing code. This is a source/documentation inventory, not a live hosted test.

## Findings

1. **Local Python file adapter is not the hosted deletion implementation.** `src/adapters/file_write_gate.py` implements authorization, revocation, file creation and receipt logging. The inspected adapter has no deletion method. Do not infer from this that the hosted web app lacks deletion; the hosted app is documented as a separate implementation.
2. **The checked-in Cloudflare worker is not the hosted customer workflow source.** `deploy/cloudflare/worker.mjs` is described in its code as an opt-in staging port for mail dispatch and health reporting. It does not provide an identifiable customer-request deletion route in the inspected source. This narrows the search but does not prove the separate hosted app has no deletion implementation.
3. **The repository contains a separate React/Vite marketing/consultation app, but it is not the identified hosted workflow.** `FULLSTACK_README.md`, `frontend/package.json`, `backend/server.js`, and `backend/routes/consultation.js` describe a site with Home/About/Services/Pricing/Contact/Consultation pages and a consultation API. The inspected consultation routes submit and retrieve intake records; no customer deletion endpoint is present in that route file. This is not proof about the separately hosted workflow.
4. **The offline workflow lab is a browser-only fictional demo.** `demos/offline_workflow_lab.html` and `tests/test_workflow_lab.mjs` exercise fictional browser fixtures, not the server-backed hosted customer workflow. Its tests must not be counted as hosted deletion tests.
5. **No hosted-workflow source location has yet been identified in the repository.** Repository searches for deletion routes, request/receipt deletion, and relevant API route patterns surfaced documentation and unrelated modules, but no confirmed source file for the hosted workflow. The hosted site may be maintained/deployed separately; that needs to be established before editing code.
6. **Historical hosted service evidence exists.** `docs/MAYA_HOSTED_ACTIONS_VERIFICATION_2026-10-16.md` reports 17 SQLite-backed service tests, including deletion and transaction rollback if receipt insertion fails. That is historical evidence, not a fresh run. It also describes the hosted workflow as a separate server-backed implementation using D1 and service-owned outputs.
7. **The current hosted deletion journey remains unverified.** `docs/MAYA_PILOT_GATE_EXECUTION_ATTEMPT_2026-10-25.md` says the authenticated hosted UI was not freshly exercised. The October 26 coverage map still marks key deletion cases as not established.
8. **The configured CI run passed, but does not test hosted deletion.** The recorded run is https://github.com/mommommy1960-lang/maya-node/actions/runs/40255591764. It passed its five configured jobs; this does not establish the current customer-facing deletion flow.
9. **Pilot readiness issue remains open.** https://github.com/mommommy1960-lang/maya-node/issues/76 tracks the hosted end-to-end check, deletion and receipt matrix, retention/incident policy, named escalation, and written business permission.

## Remaining evidence needed

- Identify the source repository or export/project for the server-backed hosted site at https://maya-working-workflow-lab.myqueen1960.chatgpt.site/, plus its build/deployment owner and deployment process. A repository link or source export is sufficient to continue; **do not share passwords, API keys, session cookies, or other secrets**.
- Map each case in `docs/MAYA_DELETION_AND_RECEIPT_COMPLETENESS_TEST_PLAN_2026-10-25.md` to an implementation function and an automated test.
- Run missing service tests using synthetic records: owner-only deletion, request/output/user-visible receipt history consistency, repeated deletion, rollback on failure, reload/re-query after deletion, and preservation of unrelated records.
- Separately run the customer-facing hosted UI journey with a disposable test account and verify server-side state. Do not use real customer data.
- Decide and document how backups and security/audit logs are retained or purged; do not promise immediate erasure of copies that are not actually removed.

## Safety boundary

No deletion code has been changed or deployed. No live records were deleted. No hosted UI test was completed in this review. The source inventory narrows the next step but does not prove that hosted deletion is broken or working today.

## Source links

- Hosted early-access workflow: https://maya-working-workflow-lab.myqueen1960.chatgpt.site/
- Coverage map: https://github.com/mommommy1960-lang/maya-node/blob/main/docs/MAYA_DELETION_RECEIPT_COVERAGE_MAP_2026-10-26.md
- Test plan: https://github.com/mommommy1960-lang/maya-node/blob/main/docs/MAYA_DELETION_AND_RECEIPT_COMPLETENESS_TEST_PLAN_2026-10-25.md
- Historical hosted verification: https://github.com/mommommy1960-lang/maya-node/blob/main/docs/MAYA_HOSTED_ACTIONS_VERIFICATION_2026-10-16.md
- Pilot gate execution attempt: https://github.com/mommommy1960-lang/maya-node/blob/main/docs/MAYA_PILOT_GATE_EXECUTION_ATTEMPT_2026-10-25.md
- Open readiness issue: https://github.com/mommommy1960-lang/maya-node/issues/76
