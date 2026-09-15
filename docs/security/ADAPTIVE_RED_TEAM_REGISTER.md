# Adaptive Red-Team Register

Status: ACTIVE. This is not a claim of impenetrability.

Method: every round must introduce a materially different attack or mutation. A round counts only when it records (1) threat, (2) observed weakness/evidence, (3) root cause, (4) remediation, (5) verification/retest, and (6) regression control. Repeating an attack without new information does not count.

## Verified findings

### RT-001 — Direct modification of authoritative branch
Attack: rely on documentation while `main` has no ruleset. Weakness: rulesets endpoint returned empty. Root cause: prose was not technically enforced. Remediation: CODEOWNERS + PR gate artifacts; repository ruleset remains OWNER ACTION REQUIRED. Retest: require PR/status checks and block destructive bypass. Regression: periodic ruleset verification.

### RT-002 — Diagnostic security checks can fail open
Attack: make Bandit/Safety/tests reject a change. Weakness: legacy `security-ethics-checks.yml` contains `continue-on-error` / `|| true`. Root cause: diagnostic workflow reports rather than gates. Remediation: a separate fail-closed gate was required. Regression: a deliberately failing safe fixture must make the gate red.

### RT-003 — Dependency becomes vulnerable after review
Weakness: no Dependabot configuration existed. Remediation: weekly pip and GitHub Actions Dependabot coverage added. Regression: dependency update monitoring remains part of PR review.

### RT-004 — Sensitive-path change receives ordinary review
Weakness: no CODEOWNERS existed. Remediation: CODEOWNERS added for repository and sensitive paths. Enforcement remains OWNER ACTION REQUIRED until code-owner review is required by ruleset.

### RT-005 — Benign-looking PR omits security/IP consequences
Weakness: no PR template. Remediation: adversarial PR checklist added. Regression: every PR must answer the strongest plausible bypass question.

### RT-006 — Vulnerability report leaks exploit details
Weakness: no root SECURITY.md. Remediation: SECURITY.md added with private-reporting/evidence-minimization rules. Stronger private reporting mechanism remains OPEN.

### RT-007 — Workflow privilege escalation
Weakness: Pages workflow held `contents: write`. Root cause: deployment pushed directly to `gh-pages`. Initial remediation target recorded; completed and retested in RT-012.

### RT-008 — Unsigned provenance ambiguity
Weakness: inspected main commit was unsigned/unverified. Remediation remains OWNER/TOOLING ACTION REQUIRED: adopt a compatible signed-commit policy and enforce where feasible.

### RT-009 — Secret committed despite .gitignore
Weakness: ignore rules cannot stop force-added/embedded credentials. Remediation: secret-scanning/push-protection verification remains OWNER ACTION REQUIRED; fail-closed gate now rejects obvious tracked private-key material. Never use live credentials as test fixtures.

### RT-010 — Dependency license/IP contamination
Weakness: functional CI does not establish license compatibility. Remediation: PR checklist requires license review; automated policy remains OPEN.

### RT-011 — A new security gate silently behaves like the old diagnostic workflow
**Attack:** create a separate security workflow, then inspect whether failures are allowed to continue.
**Observed weakness:** the repository previously had no independent fail-closed security gate.
**Root cause:** security and diagnostic concerns were coupled.
**Remediation:** added `.github/workflows/security-gate.yml` with read-only repository permission and no `continue-on-error` / `|| true` escape paths. It runs compilation, pytest, Bandit, pip-audit, and a tracked-private-key pattern check.
**Retest:** workflow definition is fail-closed by construction; branch-level mandatory enforcement remains OWNER ACTION REQUIRED through a required status check.
**Regression:** changes to this workflow are CODEOWNERS-sensitive and the workflow itself is part of adversarial review.

### RT-012 — Documentation deployment token can rewrite repository contents
**Attack:** assume the Pages deployment action or its dependency is compromised and ask what its token can modify.
**Observed weakness:** `deploy-docs.yml` granted `contents: write` and pushed a `gh-pages` branch.
**Root cause:** legacy branch-push deployment architecture required broad repository-content write authority.
**Remediation:** migrated the workflow to GitHub Pages artifact deployment with `contents: read`, `pages: write`, and `id-token: write`; it no longer receives repository-content write permission.
**Retest:** static site is staged and uploaded as a Pages artifact; deployment consumes that artifact rather than pushing repository contents.
**Regression:** workflow-permission inventory on every workflow change; CODEOWNERS review for `.github`.

## Newly discovered attacks not yet credited as completed rounds

These are real findings, but they do not increase the completed counter until repaired and retested:

- API construction explicitly sets `require_human_approval=False` despite the safer runtime default.
- Flask CORS is currently unrestricted for the API dashboard.
- Bridge attestation defaults to disabled when TPM/attestation is unavailable.
- API startup defaults `FLASK_ENV` to development, which can enable debug mode unless production is explicitly configured.
- Python dependencies use compatible version ranges rather than a reproducible lock/hash strategy.
- GitHub Actions dependencies are referenced by mutable major-version tags rather than immutable commit SHAs.
- A separate Node backend uses unrestricted `cors()`.

## Counter

**12 / 1,000 adaptive rounds completed and evidenced.**

The remaining findings are not counted merely because they were discovered. They become completed rounds only after remediation, retest, and regression protection satisfy this register's method.
