# Accountability evaluation - October 13, 2026
## Observed local result
```json
{
  "seed": 20261013,
  "scope": "synthetic model decision correctness only",
  "exhaustive_combinations_per_sector": 128,
  "randomized_trials_per_sector": 1000,
  "sectors": {
    "school": {
      "trials": 1128,
      "correct": 1128
    },
    "billing": {
      "trials": 1128,
      "correct": 1128
    }
  },
  "total": 2256,
  "correct": 2256,
  "failures": [],
  "metrics": {
    "allowed": 68,
    "blocked": 2188,
    "unauthorized_allowed": 0,
    "unassigned_cases": 0,
    "missing_decision_evidence": 0
  },
  "field_reliability_estimate": null,
  "field_trials_for_zero_failures_99pct_at_one_sided_95pct": 299,
  "statistical_note": "299 independent representative zero-failure field trials would give a one-sided exact binomial lower bound above 99%, under fixed-process IID assumptions. These synthetic runs do not qualify."
}
```
Reproduce: `python -m demos.evaluate_accountability` from repository root.

Each sector includes all 128 combinations of seven binary flags: wrong person, wrong resource, wrong action, expired permission, revoked permission, primary absent, backup accepted. Another 1,000 seeded synthetic cases per sector vary those flags and simulated time. Expected decisions are computed from injected labels, separately from the authorization method. This examines the defined model boundary; randomness is not proof of representative customer use.

No unauthorized approval, missing decision event or empty incident-owner assignment occurred in this run. A assigned actor label is not evidence that a real person is reachable. No human acknowledgment speed, notification transport, child safety, payment behavior or complete root-cause trace was measured. These are not 2,256 independent field trials and no field reliability estimate is calculated.

The earlier 24-test suite covers separate local credential, restart, rollback, queue and model behaviors; its checks are not added to this trial denominator.

## Define a 99% claim before testing
Specify one metric, a version-frozen system, operating environment, population and failure definition. Example: at least 99% of eligible test incidents have complete evidence and acknowledgment by the designated human within the agreed window. Measure those actual outcomes. Keep safety boundaries separate: an unauthorized child release or charge is a stop condition, not an acceptable 1% failure allowance.

For zero failures in n independent representative Bernoulli trials, the exact one-sided 95% lower success bound is 0.05^(1/n). At n=299, it exceeds 0.99. This conditional statistical result does not cover rare hazards, clustered events, shifting deployments or unrepresented failure modes. Failures require a recalculated interval; do not delete failures or combine changed versions without a prespecified analysis.

Reference: NIST exact binomial confidence limits, https://itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbino.htm . The zero-failure closed form and sample count above are our mathematical derivation.

## Partner pilot prerequisites and acceptance record
1. Identify the workflow owner and buyer's assigned incident owner, accepted backup and escalation recipients.
2. Define workload mix using real operational requirements: normal requests, scope errors, revocation races, absent staff, conflicting/stale rosters, network outages, delayed/duplicate messages and recovery.
3. Freeze policy/version, preregister eligible cases and stop conditions, and keep protected synthetic/pilot records.
4. Measure gate outcome, event completeness, delivery, actual human acknowledgment and verified correction separately. An HTTP response is not human acknowledgment.
5. Set a strict safety-stop rule for unauthorized actions, evidence loss or a critical coverage failure.
6. Record every failure with remediation and revalidation. Use qualified independent review before a production claim.

No organization is connected; field trials cannot be generated from internet information alone. The current buyer-response policy explicitly excludes Mya as the default operational incident responder.
