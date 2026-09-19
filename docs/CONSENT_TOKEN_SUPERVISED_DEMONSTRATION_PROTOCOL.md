# Maya Node / Consent Token — Supervised Demonstration Protocol

## Status

Prepared for controlled software demonstration. Not a customer pilot and not independent certification.

## Objective

Demonstrate that a consent token can be granted, checked, consumed, revoked, frozen, restored only with fresh operation-specific authorization, and recorded in an append-only audit path.

## Preconditions

- Use a test environment only.
- Use synthetic identities and non-consequential operations.
- No production credentials or external side effects.
- Record commit SHA, test date, operator, and environment.

## Test matrix

| ID | Scenario | Expected result |
|---|---|---|
| D01 | Valid grant and verification | Allowed within scope |
| D02 | Wrong operation | Denied |
| D03 | Single-use replay | Denied |
| D04 | Expired token | Denied |
| D05 | Revoked token | Denied |
| D06 | Frozen token | Denied |
| D07 | Restore without fresh authorization | Denied |
| D08 | Restore with fresh operation-specific authorization | Allowed only after fresh authorization is consumed |
| D09 | Audit append and verification | Passes integrity check |
| D10 | Tampered audit entry | Integrity failure detected |

## Evidence record

For every run record:

- test ID;
- expected result;
- observed result;
- pass/fail;
- timestamp;
- software commit;
- operator;
- failure detail;
- corrective action or follow-up.

## Exit criteria

The demonstration is considered software-ready only when every applicable test has a recorded result, failures are preserved, and no test depends on a secret or consequential external action.

## Remaining gate

A supervised customer demonstration requires an actual participant, consent to testing, and a written boundary around the test environment. Until then, this document is a rehearsal protocol.
