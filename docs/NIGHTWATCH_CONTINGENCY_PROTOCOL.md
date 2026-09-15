# Nightwatch Contingency Protocol

**Status:** defensive architecture / fail-closed contingency doctrine  
**Scope:** MAYA Node and connected Commons Initiative systems  
**Name:** intentionally original; no dependency on a third-party fictional mark.

## Purpose

Nightwatch is the last-resort defensive layer for the case everyone hopes never happens: a trusted dependency, vendor, collaborator, CI action, credential, release channel, repository setting, or operator becomes compromised, coerced, malicious, unavailable, or simply wrong.

Its governing assumption is: **trust can fail without warning, therefore authority must remain bounded and recoverable.**

## The last-stroke rule

No single company, account, dependency, token, maintainer, automation, model, CI runner, package registry, hosting provider, or repository setting may silently acquire irreversible authority over the system.

When evidence crosses a defined compromise threshold, Nightwatch moves the affected capability toward the safest reversible state rather than improvising destructive action.

## Contingency layers

1. **Least authority** — third parties receive only the minimum scope and duration required.
2. **Human authority boundary** — learned preferences, familiarity, vendor status, automation, or historical trust never expand permission scope.
3. **Two-boundary release** — sensitive releases require both technical verification and explicit authorized release state.
4. **Dependency quarantine** — unexpected provenance/version/signature changes block promotion pending review.
5. **Credential compartmentalization** — compromise of one credential must not imply authority over unrelated systems.
6. **Immutable evidence** — security events and release evidence are chained and externally checkpointable so rollback/truncation can be detected.
7. **Known-good recovery** — recovery uses a separately verified clean state, not whatever the compromised environment claims is clean.
8. **Revocation first** — suspected compromised authority is disabled before restoration; restoration does not silently resurrect revoked authority.
9. **Provider independence** — backups, recovery instructions, provenance records, and critical documentation must not depend exclusively on the provider being recovered from.
10. **Fail closed** — ambiguous authorization, attestation, provenance, integrity, or recovery state cannot promote privileged execution.

## Company / supply-chain threat model

Nightwatch explicitly tests and plans for malicious or compromised vendors; dependency takeover; poisoned updates; compromised GitHub Actions; package-name confusion; malicious maintainer changes; CI token escalation; artifact substitution; release-channel takeover; credential theft; collaborator privilege creep; telemetry/data exfiltration; lock-in that prevents recovery; terms/API changes that silently widen access; insider misuse; compromised OAuth/app installations; DNS/domain takeover; backup corruption; rollback attacks; provenance forgery; and cross-repository policy drift.

These are threat hypotheses, not accusations against any named company.

## Activation states

- **GREEN:** evidence and controls verified.
- **AMBER:** anomaly or provenance uncertainty; privileged promotion pauses while evidence is collected.
- **RED:** verified compromise or integrity failure; affected authority is revoked/quarantined and recovery proceeds from independently verified state.
- **BLACK:** trust root itself cannot be established; privileged operation remains frozen until a human-authorized clean-room recovery establishes a new trust root.

## Non-destructive contingency actions

Nightwatch may deny, freeze, quarantine, revoke, rotate, isolate, preserve evidence, restore from verified backup, or require human reauthorization. It must not retaliate, damage third-party systems, destroy evidence, or perform offensive counter-intrusion.

## Verification doctrine

A contingency is not considered real merely because documentation says it exists. Tests must exercise revocation, recovery, provenance validation, backup restoration, replay resistance, concurrency boundaries, and provider-loss scenarios. Results remain OPEN/PATCHED/RETEST REQUIRED until evidence supports VERIFIED.

## Thousand-case campaign accounting

The campaign consists of the established 100 enumerated adaptive attacks plus 900 additional deterministic adversarial mutations. Passing 1000 tests means those cases passed. It does **not** mean 1000 distinct vulnerability classes were tested and does not establish impenetrability.

Nightwatch evolves whenever a new failure class is discovered. The contingency plan itself is treated as attackable code and policy, because naturally humans eventually manage to break the emergency system too.
