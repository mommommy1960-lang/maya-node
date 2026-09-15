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

### API boundary attacks

1. **Human-approval bypass** — FOUND. API explicitly instantiated the runtime with `require_human_approval=False`. **Repair applied:** API now requires human approval by default. **State:** RETEST REQUIRED.
2. **Attestation bypass** — FOUND. API bridge allowed `require_attestation=False`. **Repair applied:** attestation is now required at this boundary. **State:** RETEST REQUIRED.
3. **Cross-origin browser abuse** — FOUND. API used unrestricted `CORS(app)`. **Repair applied:** cross-origin access is disabled unless `MAYA_ALLOWED_ORIGINS` explicitly supplies an allowlist. **State:** RETEST REQUIRED.
4. **Debug-mode exposure** — FOUND. development was effectively the default debug posture. **Repair applied:** debug is off by default and requires explicit `MAYA_ALLOW_DEBUG` opt-in. **State:** RETEST REQUIRED.
5. **Consent-scope downgrade** — FOUND. unknown scope could fall back to `SINGLE_OPERATION`. **Repair applied:** invalid scope is rejected. **State:** RETEST REQUIRED.

Latest API hardening commit: `17dc4c66d5ae7c3d75c08671c418812a3e397b21`.

## Next attack families queued

- authorization/identity binding and confused-deputy attacks;
- consent-token replay, substitution, expiry and scope escalation;
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
