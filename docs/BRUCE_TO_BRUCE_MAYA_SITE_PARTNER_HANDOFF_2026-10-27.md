# BRUCE-TO-BRUCE: Maya Node website editor access and partner handoff
Date: 2026-10-27
Status: HANDOFF IN PROGRESS. NOT DEPLOYED OR FINISHED.

## User instruction
The user is transferring the next Maya Node website task to a partner and plans to open a new ChatGPT conversation/canvas. The next assistant should read this file and the referenced GitHub docs before proceeding. Explain everything in very simple, one-step-at-a-time tablet instructions; proactively provide exact URLs before asking the user to open anything. The user may say "connect to GitHub Bruce-to-Bruce" (speech recognition may sound like "garden").

## Actual hosted test website
https://maya-working-workflow-lab.myqueen1960.chatgpt.site/
This is the working ChatGPT Sites-hosted test app, NOT proof of access to its editor/source. Do not change civiccontinuum.org or activate payments without explicit approval.
GitHub repository: https://github.com/mommommy1960-lang/maya-node
ChatGPT home: https://chatgpt.com/

## Immediate goal
Locate the ACTUAL ChatGPT Sites project/editor for "Maya Working Workflow Lab" and obtain supported editing/deployment access. Inspect actual deployed authentication/session architecture. Implement a visible, real sign-out/switch-account control that truly terminates or switches the app's session; never merely hide records. Do not copy the GitHub bootstrap UI's fake auth/logout stub into the live site. Test account A/B isolation and safe switching using two consenting accounts and synthetic data. Verify save/deploy, then report exact changed files, test results, deployed URL, and remaining blockers.

## Partner's simple steps
1. Open hosted test site above and identify current behavior; do not delete existing records.
2. Open https://chatgpt.com/ using the account that owns the project; locate the Maya Working Workflow Lab project in Sites/projects, if present.
3. Look for Edit, Open in Work, Share, Settings, or three-dot menu. UI may vary. Open the editor (not the public viewer).
4. If no editor, capture a screenshot, share with next assistant; do not share passwords, codes, tokens, API keys.
5. With real editor access, implement real sign-out/account switching, test using two separate accounts, and do not assert completion before deployed verification.
6. Continue remaining pilot security gates: cross-user read/download/delete and receipts; fault injection only in isolated staging; backups/retention; incident process. No real customer data until proven.
7. Return a clear checklist of passed, failed, blocked, and untested work.

## What is verified
Two owner-scoped hosted deletion tests on 2026-10-27 passed. Latest connected Maya list showed signedIn=true, 10 requests, 28 events, five completed requests, both disposable deleted IDs absent, zero orphan events. No second-account isolation was performed. GitHub narrative reports 17 historical SQLite service tests including owner isolation and rollback, but these are not fresh hosted multi-user evidence.
Evidence:
- docs/MAYA_COMPLETED_FILE_DELETION_VERIFICATION_2026-10-27.md
- docs/MAYA_DRAFT_DELETION_VERIFICATION_2026-10-27.md
- docs/MAYA_CROSS_ACCOUNT_ISOLATION_EXECUTION_GATE_2026-10-27.md
- docs/MAYA_DELETION_AND_RECEIPT_COMPLETENESS_TEST_PLAN_2026-10-25.md
- Issue #76 https://github.com/mommommy1960-lang/maya-node/issues/76

## Critical distinction
The repository file ui/web-dashboard/src/auth.ts is a bootstrap stub that accepts any nonempty username/password and has a nonfunctional logout; ui/web-dashboard/src/App.tsx renders a Logout button for that demo. DO NOT treat this as current hosted site's source or security. The current assistant has GitHub write access for documentation, but NO verified editor/deployment access to the hosted ChatGPT Sites project, so no live logout change has been made. The user expects the partner to help establish that access.

## User experience
User uses Samsung Android tablet, wants second-grade-level steps, one at a time, with links immediately. They have several ChatGPT accounts. Incognito Chrome was opened to test a separate account, but they noticed no visible sign-out on the site and prioritized fixing it. Avoid unnecessary repeated deletion tests and do not promise all security gates can be completed without backend/staging access.
