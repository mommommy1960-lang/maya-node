# Maya Node Early-Access Pilot Data and Incident Protocol — Draft

**Status: draft requiring founder completion and approval. Do not treat this document as a complete privacy policy or permission to accept live customer data.**

## 1. Scope and data minimization

The first pilot is limited to one low-risk administrative workflow. Collect only the information necessary to test that workflow. Prefer synthetic data; if a business example is needed, redact names, addresses, account identifiers, message contents, and other customer details. Do not submit credentials, payment-card details, government identifiers, health information, children's information, or sensitive case files.

No external AI/tool integration or customer messaging is in scope unless separately implemented, tested, documented, and explicitly authorized.

## 2. Access and authority

- Each pilot request must be associated with the authenticated user/business identity supported by the implementation.
- Only named, authorized pilot participants may access the pilot.
- Permission must be specific to the requested action and content, time-bounded where supported, and revocable.
- The service operator may have database access; this must be disclosed to the pilot participant.
- Never share credentials, tokens, or private customer data in public repositories, issues, logs, or demo recordings.

## 3. Receipts and records

Record only fields required to explain and review the attempt: request identifier, timestamp, requester/actor identifier appropriate to the system, action requested, authorization decision, execution result, error/escalation state, and relevant integrity metadata. Avoid storing full customer payloads in receipts unless necessary and explicitly agreed.

Receipts are service records, not independent proof of legal compliance or externally anchored signatures.

## 4. Retention and deletion

Current public engineering notes state that records persist until the owner deletes them, with deletion intended to remove the request, output, and receipt history. No automatic retention/SLA guarantee is currently established.

Before a live pilot, the founder must specify and communicate:
- exact retention period and what data it covers;
- how the participant reviews and deletes a record;
- how deletion of request, output, and associated receipts is verified;
- any backups/logs that are not immediately deleted and their expiry;
- who can perform administrative recovery and under what conditions.

Do not promise complete deletion until the implementation and its backups/logs have been verified.

## 5. Incident and escalation

**Primary pilot owner:** [Founder to enter name and monitored contact]
**Backup human owner:** [Founder to name a backup and monitored contact]
**Incident reporting channel:** [Founder to enter monitored email or other channel]
**Expected acknowledgement time:** [Agree with pilot participant before start]
**Out-of-hours coverage:** [State whether available; do not imply 24/7 support]

When an authorization, privacy, integrity, or availability concern is reported:
1. Pause the affected workflow and prevent further actions where possible.
2. Preserve minimal relevant evidence without copying unnecessary customer content.
3. Notify the named primary owner and backup.
4. Notify the pilot participant through the agreed channel and timeframe.
5. Record the issue, scope, containment, corrective action, and whether any data may have been exposed or changed.
6. Resume only after the owner has reviewed the fix and the participant has been informed as agreed.

This is an operational draft, not a legal determination of notification obligations.

## 6. Required pre-live acceptance

- [ ] Founder fills every bracketed contact/retention field and approves the protocol.
- [ ] Pilot participant receives and agrees to the data handling and incident terms.
- [ ] Hosted review/deletion behavior is tested end-to-end.
- [ ] Access isolation and authorization/revocation tests pass on the current build.
- [ ] Receipt completeness and failure behavior are verified.
- [ ] A human owner and backup are reachable.
- [ ] Synthetic/redacted-data trial passes before any live customer data is considered.

## 7. Current decision

Until these items are complete, the pilot is limited to synthetic or redacted test data. Do not advertise this draft as a privacy policy, security certification, compliance guarantee, or service-level agreement.
