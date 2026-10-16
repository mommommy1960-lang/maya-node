# Maya Accountable Actions — hosted verification, October16,2026

[Open the early-access website](https://maya-working-workflow-lab.myqueen1960.chatgpt.site/)

Civic Continuum has moved one defined accountability workflow from a local adapter to a server-backed website. A signed-in visitor prepares a text-file payload, authorizes that exact content for five minutes, and either creates the file or withdraws permission. Records are scoped to that visitor's platform identity.

## Observed live results

- Authenticated workspace loaded successfully.
- A real request was prepared and explicitly authorized in the website.
- The server created one saved output and an action receipt.
- The downloaded text file matched all123 approved bytes; SHA256 `6a2f940b9ea98683f73aa522c0d4478507ec5583c99ac6a98ca7d5b7f4333814`.
- A separate request was authorized and then revoked before execution. The website displayed a blocked/permission-revoked receipt.
- A live read of hosted output storage confirmed the revoked request had no output.
- Page reload preserved both requests and their receipt history.
- Receipt JSON downloaded successfully.

These are real site interactions and saved outputs, not fictional client records or a local-only mock. The text used for verification was non-sensitive engineering test content, not a customer transaction.

## Checks and implementation boundary

17 service tests use actual local SQLite and transactions, including revocation, exact expiry, replay/concurrent requests, changed execution input, owner isolation, missing authentication/storage, CSRF, input bounds, deletion and transaction rollback when receipt insertion fails. TypeScript validation and production build passed.23 older lab tests passed separately; that fictional lab remains available at `/lab` and must not be confused with the real main workflow.

The website ports the [local file-action contract](MAYA_REAL_FILE_ACTION_2026-10-16.md) to atomic D1 state and service-owned outputs. It does not execute the Python/POSIX module inside the hosting runtime. Download creates the visitor's local copy; server output creation is a saved database-backed file payload.

## What is not established

This early-access release does not generate AI replies, send email, control other applications, accept payment, establish commercial readiness or certify compliance. The original separate Maya AI/payment project remains under access recovery. A second real-user isolation test, physical Galaxy tablet acceptance, independent security review, external AI/tool integration and paid delivery validation remain open. Local isolation tests are not a substitute for independent multi-user testing.

Receipts are service records, not independently signed or externally anchored. The operator has database access. Text is retained until the owner deletes its record; deletion also removes that request's output and receipt history. No automatic retention/SLA guarantee. Use non-sensitive text during early access. Platform sign-in may be required to open the site. No endorsement by advisers or named reviewers is claimed.

## Next gates toward a paid accountability product

1. Validate the same workflow with a second consenting user and the founder's tablet.
2. Connect one narrowly scoped external AI/tool action and test refusal, withdrawal, failure and replay at the real execution boundary.
3. Obtain a design partner's specific problem and acceptance criteria; complete business/payment/privacy/refund readiness before charging.

Advancing the Commons Initiative: human authority, understandable evidence and meaningful correction. Credentials, personal correspondence, taxpayer identifiers and customer records are excluded from this public record.
