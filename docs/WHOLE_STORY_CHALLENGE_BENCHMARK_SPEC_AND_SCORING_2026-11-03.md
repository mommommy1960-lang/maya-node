# Whole Story Challenge — Benchmark Specification & Scoring Framework

**Date:** 2026-11-03  
**Status:** Proposed preregistration specification; not an executed benchmark  
**Owner:** Civic Continuum  
**Related protocol:** [WHOLE_STORY_CHALLENGE_COMPETITIVE_BENCHMARK_PROTOCOL_2026-11-03.md](WHOLE_STORY_CHALLENGE_COMPETITIVE_BENCHMARK_PROTOCOL_2026-11-03.md)  
**Scope:** Warehouse, fulfillment, and logistics operational-evidence reconciliation

## 1. Purpose and decision question

This specification defines how Civic Continuum will test whether Maya Node adds measurable value when reconciling evidence across warehouse management (WMS), transportation/carrier, customer-support, and finance systems.

The test question is:

> Given the same frozen operational evidence, business question, time allowance, and access conditions, does Maya Node produce more accurate, better-supported, more reproducible, or more economically useful findings than the customer's existing workflow and selected commercial alternatives?

This is a proposed protocol, not a report of completed testing. No competitor has been tested under this specification, no customer data has been obtained, and no performance advantage is established.

## 2. Benchmark principles

1. **Same evidence, same question.** All participants receive the same authorized source package and data dictionary.
2. **Blind ground truth.** Participants do not see the answer key before submitting locked results.
3. **No hindsight edits.** Freeze and hash inputs, rules, software versions, configurations, and submitted outputs.
4. **Count uncertainty honestly.** "Insufficient evidence" is a valid result when the record does not support a conclusion.
5. **Separate association from causation.** A refund or credit linked to an order is not automatically caused by the identified exception, avoidable, recoverable, or a saving.
6. **Measure the whole operating cost.** Include setup, mapping, engineering, analyst review, licensing, integrations, compute, and maintenance within the tested scope.
7. **Publish losses as well as wins.** Report raw results and limitations for every participant.
8. **Do not infer private capabilities.** A vendor's public documentation, a customer's configuration, and an observed test result are different evidence classes.

## 3. Benchmark population and dataset design

### 3.1 Target size

For the first expanded synthetic benchmark, target **500–1,000 unique orders**. This is a practical engineering target, not a guarantee of statistical power or representativeness. A statistician or independent evaluation lead should review sample size and uncertainty before inferential claims are made.

After synthetic validation, seek a separate, permissioned, de-identified operational dataset from a willing operator. Synthetic results and customer-operational results must be reported separately.

### 3.2 Required case mix

The dataset should contain ordinary controls as well as exceptions. Freeze the target proportions before generating or labeling data; do not tune the mix after observing system outputs.

Include, at minimum:

- clean, complete order journeys;
- missing carrier scans and genuine carrier exceptions;
- delayed or out-of-order EDI events;
- warehouse status / carrier status contradictions;
- inventory shortages, substitutions, and adjustment records;
- duplicate, replayed, corrected, and reversed events;
- timestamp timezone errors and bounded clock skew;
- partial shipments, split orders, returns, and cancellations;
- support complaints with and without corroborating operational evidence;
- finance credits, refunds, chargebacks, and adjustments;
- ambiguous cases where the evidence cannot establish what happened or why.

Include both material and immaterial discrepancies. A system must not be rewarded for flagging every anomaly as a material incident.

### 3.3 Data partitions

Partition by **order or other leakage-safe entity**, never by individual event row:

- **Development set:** available for building mappings, rules, and test harnesses.
- **Validation set:** available for declared configuration and threshold selection.
- **Sealed holdout set:** hidden ground truth; used once for primary comparative scoring.

No order, linked shipment, customer, or duplicated event family may leak across partitions. Keep a documented lineage manifest and cryptographic hashes for each frozen package.

### 3.4 Data dictionary and time semantics

For every field, document source system, meaning, type, null semantics, identifier scope, units, timezone, and known limitations. Normalize timestamps to a declared reference timezone while retaining original values and offsets. Define event-time versus ingestion-time explicitly. Never silently replace missing values or infer a scan that is absent.

## 4. Unit of analysis and independent ground truth

The primary unit is a **material finding**, defined before the test as a specific, actionable discrepancy or evidence gap concerning an order or shipment, with a documented expected evidence pattern and materiality rule.

Each ground-truth item must include:

- stable finding ID and affected order/shipment IDs;
- category and severity/materiality tier;
- expected classification (confirmed exception, non-exception, or indeterminate);
- source records required to support the classification;
- acceptable evidence paths and calculations;
- known confounders and alternative explanations;
- whether a financial transaction is merely associated, plausibly related, or causally attributed;
- reviewer rationale and adjudication status.

At least two reviewers independently label the sealed set. Disagreements go to a third adjudicator. Preserve reviewer decisions and reasons. The test lead must publish the labeling manual before scoring.

### 4.1 Three-way outcome labels

- **Confirmed:** evidence satisfies the pre-registered rule.
- **Not confirmed / control:** evidence supports no material exception under the rule.
- **Indeterminate:** available evidence cannot resolve the question.

Participants may return these labels or an equivalent calibrated representation. Treating an indeterminate case as confirmed without adequate evidence is an unsupported claim.

## 5. Common execution conditions

For each participant, record and hold constant where feasible:

- exact dataset version and file hashes;
- written business question and requested output schema;
- time budget and start/stop rules;
- access to documentation and technical support;
- permitted connectors, modules, and license tier;
- configuration and mapping hours;
- custom code, scripts, and manual intervention;
- analyst and engineer seniority/experience;
- product version, release date, and enabled features;
- hardware, hosting, and compute assumptions;
- training or vendor-assisted setup.

Use two baselines:

1. **Current-state human baseline:** the operator's ordinary WMS/carrier/support/finance workflow, performed by a trained analyst using normal procedures.
2. **Commercial alternatives:** select at least one process-mining platform and one logistics visibility or WMS platform relevant to the participating operator's actual stack. Record when a product cannot ingest the common package or when a fair trial is unavailable; do not score unavailable functionality as a product failure.

Maya Node receives the same source evidence and equivalent declared configuration allowance. Any special engineering or human review must be counted.

## 6. Primary metrics and exact definitions

Score at the finding level. Deduplicate multiple alerts that describe the same ground-truth finding. Publish the confusion matrix and denominators for every participant.

Let TP = correctly identified material findings; FP = reported material findings that are not supported by ground truth; FN = ground-truth material findings not identified; TN = correctly left unflagged eligible control cases. Report indeterminate cases separately.

| Metric | Definition | Reporting rule |
|---|---|---|
| Precision | TP / (TP + FP) | Report numerator and denominator; if no findings, report N/A, not 100%. |
| Recall (sensitivity) | TP / (TP + FN) | Report by category and severity as well as overall. |
| F1 | 2 × precision × recall / (precision + recall) | Secondary summary only; never replace precision and recall. |
| False-positive rate | FP / (FP + TN) | Define the eligible negative/control population in advance; report N/A if denominator is zero. |
| Unsupported-claim rate | Unsupported material assertions / all adjudicated material assertions | Audit conclusions, causal claims, certainty, and financial claims separately. |
| Evidence traceability | Correct findings with reproducible source IDs and supporting calculation / all findings scored | A citation to a source system without record-level identifiers is insufficient. |
| Reproducibility | Findings independently regenerated by a second reviewer / findings sampled for reproduction | Use a preselected sample and preserve reproduction logs. |
| Abstention quality | Correct indeterminate/insufficient-evidence decisions / all ground-truth indeterminate cases | Also report unjustified abstentions on confirmed cases. |
| Financial classification accuracy | Correctly classified finance records / finance records evaluated | Separate transaction matching from causal attribution. |
| Time to defensible result | Elapsed time from evidence handoff to a review-ready, locked output | Include pauses and disclose excluded time. |
| Human effort | Analyst + engineer hours, separated by role and task | Include setup, mapping, review, correction, and report preparation. |
| Total evaluated cost | License + implementation + integration + labor + compute + required services for the tested scope | State currency, period, assumptions, and excluded costs. |

A finding is not a true positive merely because a participant flagged the same order. It must identify the correct issue category and meet the pre-registered materiality/evidence criteria. Partial matches should be separately adjudicated and reported, not silently counted as full TP.

## 7. Proposed 100-point diagnostic score

The weighted score is a secondary summary to help compare trade-offs. The primary publication must always show the individual metrics, raw counts, denominators, and cost/time results. A high composite score cannot override a failed safety or evidence-integrity gate.

| Dimension | Weight | Component scoring |
|---|---:|---|
| Detection quality | 25 | Recall 15 points; precision 10 points |
| Evidence quality | 25 | Traceability 15 points; reproducibility 10 points |
| Epistemic integrity | 15 | Unsupported-claim control 10 points; abstention quality 5 points |
| Financial correctness | 10 | Correct transaction classification and appropriately bounded causal attribution |
| Operational efficiency | 15 | Time to defensible result 8 points; total human effort 7 points |
| Evaluated cost | 10 | Total evaluated cost against the pre-declared scope and cost model |

### 7.1 Normalization

Before opening the holdout set, publish the exact transformation from each raw metric to points, including caps, floors, missing-data treatment, and tie rules. For rate metrics, use the observed rate on the sealed holdout set; do not normalize against the best-performing participant after seeing results. For time, effort, and cost, use pre-registered thresholds or a transparent reference target. Do not award points merely because a competitor could not be tested.

If a metric is not applicable or cannot be fairly measured, mark it **N/A**, explain why, and do not silently redistribute its weight. Publish both the weighted score over applicable dimensions and the coverage percentage of the possible 100 points. A score with materially incomplete coverage must not be used for ranking.

### 7.2 Suggested rate-to-points rule

For precision, recall, traceability, reproducibility, and abstention quality, use a linear 0–100 transformation of the observed proportion, multiplied by the component weight. For unsupported-claim rate, invert the proportion: component points = component weight × (1 − unsupported-claim rate). Clamp only for numerical validity; do not remove legitimate difficult cases.

For financial correctness, award full credit only for correct transaction classification **and** disciplined separation of association from causation. Publish the two submetrics separately. No participant may receive causal-attribution credit without evidence meeting the adjudication rule.

For time, effort, and cost, pre-register a target and a floor/ceiling based on the pilot scope. A suggested transparent rule is: 100 points at or below target; 0 at or above the declared unacceptable ceiling; linear interpolation between. Set those thresholds before the test and show raw values. Do not choose thresholds after seeing participant results.

## 8. Non-negotiable integrity gates

A participant, including Maya Node, cannot be described as having passed the benchmark if any of these conditions occur:

1. **Evidence integrity failure:** input hashes or lineage cannot be verified, or source records are silently altered.
2. **Material unsupported assertion:** the output presents a material allegation, delivery conclusion, fraud claim, or causal financial conclusion as fact without sufficient evidence.
3. **Consent/authorization failure:** data was accessed or used without documented authorization and scope.
4. **Reproducibility failure:** submitted results cannot be reconstructed from the frozen evidence, declared rules, and recorded version.
5. **Ground-truth contamination:** the participant or operator accessed sealed labels before output lock.
6. **Safety-boundary failure:** a consequential action (email, payment, account change, customer contact, or production write) occurs without the required human authorization.

Report each gate as Pass, Fail, or Not Evaluated with supporting evidence. A failed gate must be prominently disclosed regardless of numeric score.

## 9. Financial-value protocol

Use separate labels for:

- **Observed transaction:** a refund, credit, charge, fee, or adjustment present in the source data.
- **Associated transaction:** linked to an order or incident, without proven causation.
- **Causally attributed amount:** independently supported by evidence that the defined event caused the transaction under the pre-registered rule.
- **Avoidable amount:** a causally attributed amount shown to have been preventable under a feasible intervention.
- **Recovered value:** cash or credit actually realized and verified after an authorized intervention.
- **Net customer value:** verified benefit minus implementation, operating, labor, and intervention costs over a declared period.

Do not call associated credits "losses," "savings," or "recoveries." Do not add the same transaction to multiple categories. Use a unique transaction ID and reconcile totals. Report gross and net values, timing, confidence, and counterfactual assumptions. A synthetic dataset can validate arithmetic and classification logic; it cannot establish real customer ROI.

## 10. Statistical analysis and uncertainty

- Pre-register primary outcomes, subgroup analyses, exclusion rules, and stopping rules before unsealing labels.
- Report counts, rates, denominators, and 95% confidence intervals for primary proportions. Use an interval method appropriate to the sample size and clustering.
- Because findings may be clustered within orders, use order-level clustered bootstrap or another justified cluster-aware method for uncertainty estimates.
- Compare paired outcomes on the same cases; do not compare unrelated samples as if independent.
- Report performance by exception category and severity, not only an overall average.
- Disclose small subgroup sizes and suppress claims where uncertainty is too wide.
- Treat exploratory analyses as exploratory; validate them on a new holdout set.
- Do not claim statistical significance, generalization, or superiority solely from a point estimate.

## 11. Customer-value evaluation after the technical benchmark

A technical benchmark does not by itself prove business value. For an authorized pilot, define a baseline period, intervention, comparison period or matched control, outcome measure, and review owner in advance.

Possible outcomes include fewer unresolved material exceptions, reduced time to defensible resolution, fewer avoidable credits, improved audit completeness, or reduced analyst effort. Attribute improvement only when the design supports attribution. Record implementation and operating costs. Customer acceptance, willingness to pay, and repeat use are separate evidence and should be measured directly.

## 12. Dataset quality and acceptance checklist

Before any blind run, confirm:

- [ ] 500–1,000 unique orders targeted for the expanded synthetic set; final count and rationale documented.
- [ ] Ordinary controls and all required exception categories represented.
- [ ] Ground truth independently labeled and adjudicated.
- [ ] Indeterminate cases included.
- [ ] Leakage-safe development, validation, and sealed holdout partitions created.
- [ ] Data dictionary, timezone rules, event-time/ingestion-time semantics published.
- [ ] Source files frozen and cryptographic hashes recorded.
- [ ] Financial transaction IDs unique and no double counting.
- [ ] Labeling manual, materiality rules, metric formulas, weights, and thresholds preregistered.
- [ ] Execution conditions, time budgets, support rules, and cost model preregistered.
- [ ] Privacy, consent, security, retention, and publication approvals documented for any real data.
- [ ] Neutral reviewer and independent reproduction reviewer confirmed.

If any required item is incomplete, the run may proceed only as a clearly labeled pilot or engineering dry run—not as a completed comparative benchmark.

## 13. Reporting template

For every participant, publish:

1. Product/system name, version, license tier, enabled modules, and test date.
2. Dataset hashes, case counts, partition, and data limitations.
3. Configuration, connectors, custom code, vendor assistance, and setup effort.
4. Confusion matrix and all primary metric numerators/denominators.
5. Category/severity breakdowns and uncertainty intervals.
6. Unsupported assertions, abstentions, and integrity-gate results.
7. Financial transaction classifications, with association and causation separated.
8. Time, human effort, total evaluated cost, and excluded costs.
9. Reproduction result and reviewer notes.
10. Deviations from protocol, unavailable features, and reasons for missing scores.
11. Customer-value results, if and only if a separate authorized outcome evaluation was performed.

## 14. Decision rules and claims policy

A result supports only the narrow claim directly tested. For example, a single operator's dataset can support a statement about that operator, workflow, product versions, and test period—not the entire market.

Before using comparative language such as "more accurate," "faster," "lower cost," or "better," require:

- all integrity gates passed;
- fair, documented access and comparable execution conditions;
- pre-registered primary metric and analysis;
- independent review and reproducibility;
- uncertainty intervals that support the stated direction and practical significance;
- full disclosure of limitations and contrary results.

A broad superiority claim requires replication across multiple independent operators and materially different environments. No benchmark result establishes "world's first" or superiority over private systems that were not tested.

Approved pre-benchmark wording:

> Civic Continuum is developing an independent way to reconcile operational evidence across existing systems, identify material gaps and contradictions, and trace documented consequences. The Whole Story Challenge demonstrates the method on fictional data. We are testing whether this approach adds measurable value alongside the tools organizations already use.

## 15. Current status and next gates

At publication of this specification:

- the five-order Whole Story Challenge remains a synthetic teaching demonstration and smoke test;
- the expanded 500–1,000-order dataset has not been built or independently labeled;
- no competitor has been run under this protocol;
- no customer operational dataset or pilot outcome has been verified;
- no comparative performance, ROI, recovery, or superiority claim is established.

Next gates:

1. Approve this specification and select an independent evaluation lead.
2. Create the expanded synthetic dataset and labeling manual.
3. Validate data generation, joins, scoring implementation, and leakage controls on development/validation data.
4. Seal the holdout set and freeze the preregistration.
5. Select the operator-relevant alternatives and agree on fair execution conditions.
6. Run the blind benchmark and independent reproduction.
7. Publish results—including failures and limitations—before revising market claims.

**No deployment, production write, payment activation, outbound email, or customer-data access is authorized by this document.**
