# MAYA Node — Live Security Hardening Update

**Status:** ACTIVE / NOT A CLAIM OF IMPENETRABILITY  
**Method:** adaptive red-team: distinct attack → evidence → root cause → repair → retest → regression control. A finding is not counted closed merely because a fix was proposed.

## Latest verified work

- Established fail-closed CI/security-gate direction and repository governance hardening work.
- Removed a hard-coded Aurora simulation consent-token pattern and preserved explicit authorization semantics.
- Repaired Aurora integration behavior and obtained a successful integration baseline before the latest API hardening mutation.
- Reduced GitHub Pages deployment authority from repository-write behavior to a narrower deployment model.
- Added/identified governance controls including CODEOWNERS, PR review gates, dependency monitoring, security reporting, and repository-admin controls that still require platform enforcement.

## Current adaptive attack wave

1. **Human-approval bypass** — FOUND/PATCHED. API explicitly instantiated runtime with `require_human_approval=False`; API now requires human approval. **RETEST REQUIRED.**
2. **Attestation bypass** — FOUND/PATCHED. API allowed `require_attestation=False`; API now requires attestation. **RETEST REQUIRED.**
3. **Cross-origin browser abuse** — FOUND/PATCHED. Unrestricted `CORS(app)` replaced with explicit `MAYA_ALLOWED_ORIGINS` allowlist. **RETEST REQUIRED.**
4. **Debug-mode exposure** — FOUND/PATCHED. Debug is now off by default and requires explicit `MAYA_ALLOW_DEBUG`. **RETEST REQUIRED.**
5. **Consent-scope downgrade** — FOUND/PATCHED. Unknown scope no longer silently falls back to `SINGLE_OPERATION`; invalid scope is rejected. **RETEST REQUIRED.**
6. **Confused-deputy / cross-user consent substitution** — FOUND/PATCHED. Bridge verified signature and operation but did not bind the presented token's `user_id` to the executing `user_id`. Added explicit subject binding. **RETEST REQUIRED.**
7. **Attestation indeterminate-state acceptance** — FOUND/PATCHED. Prior bridge rejected only `FAILED`, allowing any other non-verified state. Attestation now fails closed unless status is exactly `VERIFIED`, and absence of the verifier while required is an error. **RETEST REQUIRED.**
8. **Single-use token consumption failure ignored** — FOUND/PATCHED. Operation path invoked token consumption without checking its result. It now treats inability to consume a required token as an execution failure. **RETEST REQUIRED.**

Relevant hardening commits: `17dc4c66d5ae7c3d75c08671c418812a3e397b21`, `ccaad9aa6b048d1cb1866d80bc9836dbeb0ac8b0`.

## Next attack families queued

- consent-token replay/race, substitution, expiry, mutation and scope escalation;
- attestation spoofing/downgrade/failure behavior;
- audit-ledger tamper, truncation, reorder and rollback attacks;
- malformed/oversized JSON and resource-exhaustion boundaries;
- error/log leakage and injection;
- CORS/preflight/header-policy regressions;
- dependency and GitHub Actions supply-chain mutation;
- workflow-token privilege escalation and untrusted PR execution;
- artifact/release provenance substitution;
- branch/ruleset/force-push/deletion bypass;
- secret/history exposure and credential rotation failure;
- package/license/IP contamination and provenance drift;
- cross-repository policy drift;
- recovery/rollback and backup-integrity failures.

## Non-negotiable accounting rule

Do not convert OPEN, FOUND, PATCHED, or RETEST REQUIRED into VERIFIED/CLOSED until evidence demonstrates the repaired control survives the relevant regression attack. Repetition does not count as a distinct adaptive round.

## Platform/admin blockers

Repository-file controls are not substitutes for GitHub platform enforcement. Main-branch rulesets/branch protection, required checks, force-push/deletion blocking, signed-commit policy where compatible, and available secret/code/dependency scanning must be independently verified at the repository settings/API layer. Keep those items open until verified.
