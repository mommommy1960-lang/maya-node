## Purpose
Describe the change and why it is necessary.

## Verification
- [ ] Tests/checks relevant to this change pass.
- [ ] No credentials, tokens, private keys, PII, confidential partner data, or patent/trade-secret material were added.
- [ ] New/changed dependencies were reviewed for security and license implications.
- [ ] Workflow/action permissions remain least-privilege.
- [ ] Legal/license/IP changes preserve historical grants and do not silently broaden rights.
- [ ] Public disclosure was reviewed for patent/trade-secret consequences where applicable.
- [ ] Security/governance controls were not weakened to make a test pass.

## Sensitive-path review
If this changes `.github/`, `LICENSE*`, `LEGAL_AND_IP_NOTICE.md`, `SECURITY.md`, governance, release, deployment, or authority code, explain the threat model and rollback plan.

## Adversarial question
What is the strongest plausible way this change could be abused, bypassed, misunderstood, or used to weaken Commons/Maya Node protections, and what control prevents it?
