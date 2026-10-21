# Maya Node customer-action verification ledger — October 20, 2026

## Scope and provenance
This is a status record based on previously documented tests, **not** a claim that these tests were rerun on October 20. Hosted demonstration: https://maya-working-workflow-lab.myqueen1960.chatgpt.site/ . Existing evidence: [hosted verification](../docs/MAYA_HOSTED_ACTIONS_VERIFICATION_2026-10-16.md) and [real file action](../docs/MAYA_REAL_FILE_ACTION_2026-10-16.md). Do not infer production security certification or general AI-assistant capability.

| Check | Current evidence | Status |
|---|---|---|
| 1. Request an authorized file action | Hosted demonstration created a text file after authorization | Demonstrated within narrow scope |
| 2. Verify permission | Exact scoped permission checked before creation | Demonstrated within narrow scope |
| 3. Execute and produce receipt | Exact output bytes and saved allow/block receipts documented | Demonstrated within narrow scope |
| 4. Revoke and block | Revocation prevented subsequent action; receipts persisted across reload | Demonstrated within narrow scope |
| 5. Customer review and delete their records | Receipt visibility/persistence documented; authenticated customer-controlled deletion and isolation not verified | **Pending** |

## Check 5 acceptance criteria
- Authenticated customer can list only their own receipts and records.
- Deletion request requires explicit current authority, names the exact record(s), and returns a verifiable result.
- After deletion, customer-accessible records and underlying permitted stored copies are no longer retrievable, subject to clearly disclosed legal retention obligations and backup windows.
- Cross-customer reads/deletes, revoked grants, expired grants and replayed requests fail closed.
- Tests cover persistence, reload, authorization, concurrent requests, error paths, backup/retention policy and audit metadata that does not retain deleted sensitive content.
- Publish a reproducible test report and scope limitations before marking PASS.

## Public collaboration request
Seeking a technical peer review of scoped record deletion, identity isolation, authorization and auditable receipts. No private customer records, keys or unpublished design materials should be shared publicly. Any named collaborator's participation or endorsement requires independent confirmation.

## Release gate
Checks 1–4: documented earlier, not freshly rerun here. Check 5: NOT PASSED. No customer billing or general production readiness implied. Do not change production or enable payments until end-to-end testing and authorization are complete.
