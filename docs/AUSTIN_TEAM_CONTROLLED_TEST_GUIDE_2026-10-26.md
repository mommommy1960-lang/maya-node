# Maya Node — Austin & Team Controlled Test Guide
Date: 2026-10-26

## Purpose
Invite Austin and his team to review the current Maya Node prototype and help validate the permission-gated text-file workflow. This is a controlled evaluation, not a claim that Maya Node is production-ready.

## Public entry points
- Prototype: https://maya-working-workflow-lab.myqueen1960.chatgpt.site/
- Project and evidence: https://github.com/mommommy1960-lang/maya-node
- Current readiness tracker: https://github.com/mommommy1960-lang/maya-node/issues/76
- Deletion/receipt case map: https://github.com/mommommy1960-lang/maya-node/blob/main/docs/MAYA_DELETION_RECEIPT_COVERAGE_MAP_2026-10-26.md

## Scope and safety
- Use only synthetic text that contains no personal, confidential, regulated, customer, payment, or authentication data.
- Do not connect production accounts or upload business records.
- Do not treat the demo as a general-purpose AI assistant, a general OS sandbox, a certified security product, or a production customer service.
- Do not enter credentials into the demo unless a separately verified official sign-in flow explicitly requires them.
- Stop and report any unexpected action, cross-user visibility, unclear permission, or misleading receipt.

## Suggested test session
1. Record browser/device and time; use a unique synthetic phrase such as `AUSTIN-TEST-2026-10-26-ALPHA`.
2. Prepare a harmless text request and inspect the exact content before authorizing.
3. Authorize only the exact displayed action; confirm the output bytes match the approved text.
4. Inspect the receipt: requested action, authorization outcome, time, result, and any error should be understandable.
5. Revoke permission, retry the same action, and verify it is blocked.
6. If a dedicated disposable account and test-environment support are provided, test deletion there only. Verify the request, output and receipt behavior after deletion; do not perform destructive tests on other users' data.
7. Report each result as PASS, FAIL, or NOT TESTED, with a redacted screenshot or error text. Never include secrets or personal data.

## What is not yet cleared
Current repository records do not establish a fresh end-to-end hosted deletion test, complete receipt-case coverage, customer-controlled deletion across all stored copies/backups, or finalized retention/incident contacts. These remain release gates. CI passing is useful evidence for the jobs it ran, but is not proof of live hosted behavior.

## Feedback format
- Test ID:
- PASS / FAIL / NOT TESTED:
- Steps taken:
- Expected result:
- Observed result:
- Redacted evidence:
- Impact / reproduction notes:

## Access
The repository and prototype entry point are public, but this guide does not create accounts, grant private repository permissions, or confirm that the hosted service is accepting new testers. Founder must separately approve any access, scope, and handling of test findings before a real customer pilot.
