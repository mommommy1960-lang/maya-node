# Adaptive Red-Team Register

Status: ACTIVE. This is not a claim of impenetrability.

Method: every round must introduce a materially different attack or mutation. A round counts only when it records (1) threat, (2) observed weakness/evidence, (3) root cause, (4) remediation, (5) verification/retest, and (6) regression control. Repeating an attack without new information does not count.

## Wave 1 verified findings

### RT-001 — Direct modification of authoritative branch
**Attack:** attempt to rely on repository documentation while `main` has no ruleset.
**Observed weakness:** repository rulesets endpoint returned an empty set on 2026-09-14.
**Root cause:** policy existed in prose but was not technically enforced at the repository rule layer.
**Remediation:** CODEOWNERS + PR gate artifacts added in this branch. Required repository ruleset remains OPEN because current connector cannot administer rulesets.
**Retest:** FAIL-CLOSED only after an active ruleset requires PR review/status checks and blocks force-push/deletion as appropriate.
**Regression:** verify ruleset after configuration and periodically thereafter.

### RT-002 — Security checks report failure but merge remains possible
**Attack:** introduce code that Bandit/Safety/tests reject.
**Observed weakness:** `security-ethics-checks.yml` uses `continue-on-error: true` and `|| true` across multiple security/test steps.
**Root cause:** diagnostic workflow was designed to report rather than gate.
**Remediation:** create a separate mandatory fail-closed gate rather than silently changing historical diagnostic behavior. OPEN until workflow is added/tested and required by ruleset.
**Regression:** intentionally failing fixture must make the gate red.

### RT-003 — Dependency substitution / stale vulnerable dependency
**Attack:** dependency becomes vulnerable after initial review.
**Observed weakness:** no `.github/dependabot.yml` existed.
**Remediation:** weekly pip and GitHub Actions Dependabot coverage added.
**Retest:** verify Dependabot configuration is recognized after merge.

### RT-004 — Unreviewed sensitive-path change
**Attack:** PR changes workflow/license/security file while ordinary reviewer focuses on application code.
**Observed weakness:** no CODEOWNERS file existed.
**Remediation:** CODEOWNERS added for repository and sensitive paths.
**Retest:** requires branch/ruleset setting that requires code-owner review. OPEN until technical enforcement exists.

### RT-005 — PR social-engineering / review omission
**Attack:** benign-looking PR omits security/IP implications.
**Observed weakness:** no PR template existed.
**Remediation:** adversarial PR checklist added.
**Retest:** confirm template appears on new PR; enforcement of truthful completion still depends on review/ruleset.

### RT-006 — Vulnerability disclosure leaks the vulnerability
**Attack:** reporter opens public issue containing exploit details/credentials.
**Observed weakness:** no root `SECURITY.md` guidance existed.
**Remediation:** SECURITY.md added with private-reporting and evidence-minimization rules.
**Retest:** documentation control only; stronger private reporting mechanism remains future work.

### RT-007 — Workflow privilege escalation
**Attack:** compromise a workflow and use its token to write repository contents.
**Observed evidence:** most inspected workflows explicitly use `contents: read`; `deploy-docs.yml` uses `contents: write` because it pushes `gh-pages`.
**Root cause/risk:** deployment requires write authority, increasing blast radius relative to read-only jobs.
**Remediation:** OPEN: migrate Pages deployment to the least privilege supported by the chosen deployment method and protect workflow changes via CODEOWNERS/ruleset.
**Regression:** workflow-permission inventory on every workflow change.

### RT-008 — Unsigned provenance ambiguity
**Attack:** dispute whether an important commit was cryptographically verified.
**Observed weakness:** inspected latest `main` commit reported `verified:false`, reason `unsigned`.
**Remediation:** OPEN: decide and implement signed-commit policy compatible with actual contributor/tooling workflow; then require it through ruleset if feasible.
**Regression:** verify important release/provenance commits report verified signatures.

### RT-009 — Secret committed despite `.gitignore`
**Attack:** explicitly add a credential or secret file despite ignore rules, or leak it in a non-ignored file/history.
**Observed weakness:** `.gitignore` blocks common secret filenames but cannot prevent forced adds or secrets embedded elsewhere.
**Remediation:** rely on GitHub secret scanning for public repositories; OPEN: verify push protection/security settings and require resolution gates where account/plan supports them.
**Regression:** safe synthetic-secret test only in an isolated authorized test context; never commit a live credential.

### RT-010 — Dependency license/IP contamination
**Attack:** add a dependency whose license conflicts with intended distribution/commercial model.
**Observed weakness:** ordinary functional CI does not establish license compatibility.
**Remediation:** PR checklist now requires license review; OPEN: add automated dependency review/license policy where supported.
**Regression:** every manifest/lockfile change gets dependency/security/license review.

## Non-negotiable count rule
The target is 1,000 adaptive rounds, not 1,000 executions. Only materially distinct, evidenced rounds count. Unverified or merely hypothetical mitigations remain OPEN.
