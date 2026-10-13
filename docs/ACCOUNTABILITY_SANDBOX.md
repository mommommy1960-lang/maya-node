# Local accountability sandbox — stage 2
October 13, 2026 Pacific. Current result: 24 selected local tests passed, 0 failed. Earlier 15/17-test reports remain historical.

## Implemented locally
- Operator-provisioned random bearer credentials; stored token digests; expiry and revocation; caller identity derived from credential lookup.
- SQLite state snapshots and delivery queue committed together; cases and credentials survive reopening.
- HMAC verification of saved model state on reopening, using an externally supplied key.
- Pending, failed, delivered, acknowledged and canceled queue states; failed test delivery retries with a stable delivery ID.
- Advocate grant expiry/revocation rechecked before view/export and queued test delivery.
- Transaction failure restores the in-memory model and rolls back database changes.
- Case-scoped evidence export from the authenticated local request wrapper.

## Verification
From the repository root:
```sh
python -m unittest tests.integration.test_accountability_sandbox tests.integration.test_accountability_demo tests.integration.test_consent_token_demonstrator -v
```
Observed 24 passes: seven sandbox tests, 13 simulation tests, four existing consent tests.
Tested restart persistence; invalid/expired/revoked credentials; caller identity spoof rejection; unrelated case access denial; revoked advocate queue cancellation; state alteration detected at reopen; injected storage failure rollback; failed delivery retry and separate acknowledgment.

## Operational boundary
This is a local Python library with synthetic records, not a deployed network application or verified identity-provider integration. Operator provisioning and fixture configuration are trusted local methods; do not expose them as public endpoints. Tokens and actor labels do not verify real-world identity. The demo provides no live email, SMS, payment provider, school system or legal-aid connection.

The test adapter is intentionally not an external transport. Successful delivery is not human acknowledgment, case acceptance, representation, refund or emergency response. A crash after adapter acceptance may cause duplicate delivery; actual transports require durable idempotency by delivery ID. No exactly-once guarantee.

SQLite synchronous FULL and the restart tests establish only tested local persistence behavior, not full power-loss durability, backup restoration or fleet operation. Single-instance/single-worker use only: parallel instances can overwrite stale snapshots. Outbox/session tables lack HMAC protection; same-owner database access can alter authorization or delivery state. State HMAC cannot detect rollback to an older valid snapshot, and an attacker controlling both key and data can rewrite records. It is not immutable or legally certified evidence.

No real-time scheduler or external escalation worker is installed. The earlier model's escalation remains manually driven simulation. Full workflow correction/reviewer operations are not yet exposed through this authenticated wrapper. Secure transport, managed identity, key lifecycle, database permissions, independently anchored evidence, concurrency controls, retention, independent assessment and school-specific emergency integration remain open.

## Next external gates
Choose a participating pilot organization and its designated workflow owner. Agree scope, lawful sharing authority, roles and fallback procedures. Integrate an established identity service and protected transport; implement actual test-mode notification/payment adapters with idempotency and verified origins. Rehearse accepted handoffs, outages, missed acknowledgment, backup restoration and data deletion with synthetic records before operational claims.

This stage closes part of the partner-independent sandbox work. It does not represent a complete live integration.
