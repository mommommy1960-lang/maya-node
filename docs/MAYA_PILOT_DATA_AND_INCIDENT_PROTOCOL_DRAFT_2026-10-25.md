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

The original hosted Site is active at v17. New records have 30-day retention deadlines; legacy records with NULL deadlines are preserved. Owner deletion removes the request, associated output and service receipt history in the tested paths. Operator cleanup uses fixed server time, preserves unexpired records, and returns aggregate evidence. The first live cleanup completed with zero removals and its run reference matched persisted maintenance status. The daily cleanup/incident task is enabled at 8 AM Pacific; future scheduled execution has not yet been demonstrated. This application-level evidence does not establish hosting backup or log expiry.

Before a live pilot, the founder must specify and communicate:
- exact retention period and what data it covers;
- how the participant reviews and deletes a record;
- how deletion of request, output, and associated receipts is verified;
- any backups/logs that are not immediately deleted and their expiry;
- who can perform administrative recovery and under what conditions.

Do not promise complete deletion until the implementation and its backups/logs have been verified.

## 5. Incident and escalation

**Primary pilot owner:** Founder explicitly accepted the human incident-responder role for now on October 27, 2026. Coverage hours and acknowledgement targets remain unspecified; no 24/7 promise.
**Backup human owner:** Unfilled. Founder reports no backup person currently available; do not assign or contact anyone implicitly.
**Incident reporting channel:** contact@civiccontinuum.org. Incoming forwarding to the founder's connected inbox has been verified. Daily automated checks are enabled; this does not establish continuous human monitoring.
**Expected acknowledgement time:** [Agree with pilot participant before start]
**Out-of-hours coverage:** [State whether available; do not imply 24/7 support]

When an authorization, privacy, integrity, or availability concern is reported:
1. Pause the affected workflow and prevent further actions where possible.
2. Preserve minimal relevant evidence without copying unnecessary customer content.
3. Privately alert the founder with a concise summary and message link. Escalate to an explicitly consenting backup only after one exists; until then record the coverage gap. Outbound messages require explicit authorization.
4. Notify the pilot participant through the agreed channel and timeframe.
5. Record the issue, scope, containment, corrective action, and whether any data may have been exposed or changed.
6. Resume only after the owner has reviewed the fix and the participant has been informed as agreed.

This is an operational draft, not a legal determination of notification obligations.

### Current triage procedure (draft; no staffing or response-time commitment)

- Permission/revocation bypass or suspected cross-account disclosure: seek prompt human review; recommend pausing the affected workflow. Preserve minimal timestamps, sanitized error codes and private evidence links. Do not automatically revoke access or change production.
- Missing receipts, integrity concerns or failed cleanup: capture the actual outcome and persisted run reference, alert the founder, and keep uncertain outcomes unresolved. Do not retry an uncertain mutating action blindly.
- Availability failure: distinguish a single visitor/account failure from a wider outage using bounded read-only checks; report observed evidence and uncertainty.
- Track privately: received time, category, affected workflow, observed facts, containment decision, human owner, next action and resolution evidence. Keep customer payloads and identifying receipts out of public GitHub.
- Acknowledge or notify participants only after a human approves exact recipients and content. No acknowledgement deadline or out-of-hours promise exists yet.
- Recovery, configuration changes, live deletion and publication require their own applicable authorization; incident triage is not permission to perform them.
- Close only after the responsible human reviews remediation and verifies the affected path; document unresolved backup or staffing gaps.

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

## 8. Hosting verification gate — October 27, 2026

Official Sites administration guidance directs retention/deletion questions to OpenAI Support: https://learn.chatgpt.com/docs/enterprise/sites (retrieved October 27, 2026). It does not establish this Site's backup expiry or recovery configuration.

The existing unsent Support draft asks for actual D1 backup/PITR availability and retention; infrastructure-log/derived-copy expiry; prevention of deleted-data resurrection; a synthetic restore into a separate isolated hosted database; and evidence, cost and approval requirements. The draft has no recipient because Gmail did not honor the requested business sender. Do not send from the personal address or claim a Support request was submitted.

Acceptance requires provider-specific written answers and an approved isolated drill showing checkpoint recovery, owner isolation, consistent requests/outputs/receipts, and exclusion of deleted/expired data before any restored service is exposed. Keep the live Site unchanged during the drill. Record actual elapsed recovery time and restored checkpoint; do not invent recovery objectives or claim local tests prove hosted recovery.
