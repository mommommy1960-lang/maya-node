# MAYA Node — Live Security Hardening Update

**Status:** ACTIVE / NOT A CLAIM OF IMPENETRABILITY  
**Method:** distinct attack → evidence → root cause → repair → retest → regression control.

## 100-case adaptive wave — EXECUTED

A dedicated executable suite now contains 100 enumerated adversarial cases covering consent subject mutation, operation/scope mutation, expiry manipulation, signature substitution/corruption, metadata mutation, token identity/state/replay, and audit-ledger tamper/deletion/reorder/splice attacks.

### First execution

- 100 cases collected and executed.
- 99 attacks were blocked.
- Attack 086 **succeeded**: deleting the genesis ledger entry was not detected because integrity verification accepted the next internally valid entry as a new root.
- Root cause: the verifier checked entry hashes and downstream links but did not assert the structural identity of the genesis anchor.

### Repair

Commit `2015f06064490f4639f382275c20a8352cbef671` hardened ledger verification to require the genesis anchor, sequential indices, canonical JSON hashing, valid entry hashes, and valid previous-hash linkage.

### Retest

GitHub Actions run `34921683873`, job **Adaptive Red-Team 100**, completed successfully after the repair. All 100 enumerated adversarial cases passed. Bandit also passed on the repaired commit.

**Wave result: 100/100 attacks executed; one real breach found, repaired, and regression-tested.** This means these 100 specific attacks are currently blocked. It does not mean the repository is impenetrable.

## CI defense discovered during the wave

The pre-existing Security & Ethics workflow used multiple fail-open constructs (`continue-on-error` / shell fallbacks). Those were removed from the core security path and a dedicated fail-closed `Adaptive Red-Team 100` job was added with read-only `GITHUB_TOKEN` permissions.

Fail-closing the workflow then exposed missing CI dependencies rather than hiding them: runtime collection lacked Flask and ethics verification lacked pytest. Commit `d1f4066bd4c586079d4b027aac693d65ae660624` adds the required test dependencies while retaining fail-closed behavior. This change must itself survive CI before being credited as verified.

## Earlier hardening retained

- Human approval required at the API boundary.
- Attestation required at the API boundary and non-VERIFIED attestation fails closed.
- CORS disabled unless an explicit origin allowlist is supplied.
- Debug mode disabled by default and separately opt-in gated.
- Invalid consent scopes rejected rather than downgraded.
- Consent tokens bound to both user identity and operation.
- Single-use token consumption failure is treated as execution failure.
- Hard-coded Aurora simulation consent-token pattern removed.
- GitHub Pages deployment authority reduced.
- CODEOWNERS, PR review gates, dependency monitoring and security reporting added/identified.

## Next adaptive waves

The next attacks must move beyond the first 100 rather than merely mutate the same cases: concurrent token replay/races; restart and multi-worker authorization state; persistence/revocation recovery; attestation spoof/downgrade; ledger rollback/checkpoint attacks; malformed/oversized API input and resource exhaustion; log/error leakage; workflow-token privilege escalation; untrusted PR execution; action/dependency supply-chain substitution; artifact/release provenance; branch/ruleset bypass; secret/history exposure; package/license/IP contamination; cross-repository policy drift; backup/recovery integrity.

## Accounting rule

OPEN, FOUND, PATCHED and RETEST REQUIRED are not VERIFIED. Repetition is not a new round. A proposed control is not a deployed control.

## Platform/admin blockers

Repository-file controls do not replace GitHub platform enforcement. Main-branch rulesets/branch protection, required checks, force-push/deletion blocking, signed-commit policy where compatible, and available secret/code/dependency scanning remain subject to independent repository-settings/API verification.
