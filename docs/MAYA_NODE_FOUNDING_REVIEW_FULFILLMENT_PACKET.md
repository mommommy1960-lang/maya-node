# Maya Node Founding Review — Repeatable Fulfillment Packet

## Purpose

A bounded, human-delivered design review for AI systems that need clearer consent, permission boundaries, authority limits, auditability, and recovery paths.

## Customer deliverables

1. Intake confirmation and scope statement.
2. Written boundary-risk report.
3. One practical adversarial test against the customer's stated limits.
4. Findings summary with evidence requested, open questions, and recommended next controls.
5. Plain-language limitations notice.

## Intake checklist

- System name and version:
- Customer/team:
- Intended use:
- Actions the system may take:
- Actions it must never take:
- Human approval points:
- Revocation/stop mechanism:
- Audit and evidence available:
- External services or consequential actions:
- Confidentiality constraints:
- Preferred delivery date:

## Review sequence

### A. Boundary map

Record allowed actions, prohibited actions, approval requirements, authority source, expiry/freshness expectations, and recovery path.

### B. Adversarial test

Choose one test tied to the design's own stated risk. Examples:

- expired authorization;
- revoked authorization;
- attempted scope expansion;
- conflicting instruction;
- unavailable approver;
- replayed approval;
- audit-record tampering.

Record setup, expected fail-closed behavior, observed result, and unresolved limitations.

### C. Report

Use the following headings:

- Executive finding
- What the system appears authorized to do
- What it must not do
- Evidence reviewed
- Adversarial test
- Fail-closed behavior
- Human recovery path
- Material gaps
- Priority recommendations
- Limitations and non-certification statement

## Delivery and recordkeeping

- Store the intake and report in the agreed customer-controlled location.
- Do not include secrets, private keys, protected supplier drawings, or unnecessary personal data.
- Keep a dated evidence index and preserve failed tests.
- Obtain customer permission before publishing any case study or identifying details.

## Commercial boundary

The founding offer is a human-delivered design review, not certification, legal advice, penetration testing, safety approval, or a claim that the customer's system is production-ready. Price and availability must be confirmed before acceptance.

## Definition of repeatable

The packet is repeatable when a second reviewer can follow the same intake, test-selection, report, and delivery steps without relying on undocumented context.
