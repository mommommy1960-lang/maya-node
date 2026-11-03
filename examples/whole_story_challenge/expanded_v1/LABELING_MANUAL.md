# Whole Story Challenge — Independent Labeling Manual

**Version:** 1.0  
**Date:** 2026-11-03  
**Dataset:** Expanded synthetic v1, 500 fictional orders  
**Status:** Initial reference labels are synthetic-generation labels; independent adjudication is still required before a blind comparative benchmark.

## 1. Purpose and boundary

This manual defines how independent reviewers classify order-level evidence. It is designed to prevent a missing record, status mismatch, customer complaint, or finance transaction from being overstated as proof of physical delivery, misconduct, causation, loss, or recoverable value.

All records in this dataset are fictional. The dataset is suitable for engineering and scoring dry runs, not for claims about real-world prevalence, customer savings, or product superiority.

## 2. Review unit and required output

Review one order at a time. Record:

- order ID and all source record IDs examined;
- primary category and severity;
- outcome: `confirmed_exception`, `control`, or `indeterminate`;
- finding statement limited to what the evidence establishes;
- supporting calculation or rule;
- alternative explanations and missing evidence;
- finance status: `none`, `associated_only`, `associated_not_causal`, `causally_attributed`, or `indeterminate`;
- reviewer ID, timestamp, rationale, and adjudication status.

Do not treat a matching order ID alone as sufficient evidence. Check record identity, event time, ingestion time, shipment/transaction linkage, and relevant quantity/status fields.

## 3. General classification rules

### Confirmed exception

Use only when the supplied evidence meets the specific rule below. State the narrow discrepancy. Do not infer intent, fraud, final physical disposition, or causation unless separately established.

### Control

Use when the records meet the control rule and no material exception is supported. A recorded refund or credit does not, by itself, turn a control into an operational exception.

### Indeterminate

Use when the evidence is insufficient or materially conflicting and the benchmark rule does not resolve the outcome. Indeterminate is not a failure to analyze; it is the correct answer when certainty is unsupported.

## 4. Category-specific rules

| Category | Expected outcome | Required evidence / rule | Prohibited overstatement |
|---|---|---|---|
| clean_control | control | WMS delivered; carrier delivered; no support exception; no finance transaction | Do not invent a problem. |
| missing_carrier_scan | confirmed_exception | WMS delivered + carrier only in transit/no delivery event + missing-package support case | Do not state that delivery definitely failed; absence of scan is not proof of non-delivery. |
| late_edi_delivery | confirmed_exception | Carrier event time precedes ingestion time by more than the preregistered 2-hour latency threshold | Do not call this a failed delivery; delivery is recorded. |
| status_contradiction | confirmed_exception | WMS delivered conflicts with carrier delivery exception and support non-receipt report | Do not assert final physical disposition or blame without further evidence. |
| inventory_shortage | confirmed_exception | WMS fulfilled quantity is zero/short and carrier has no tender event | Do not call a courtesy credit a proven loss. |
| duplicate_carrier_event | confirmed_exception | Same underlying business event is represented more than once; deduplicate by event identity, not merely similar timestamps | Do not count duplicate rows as multiple deliveries. |
| known_clock_skew | control | Apply documented +10-minute carrier clock offset before comparing timestamps; adjusted events align within 5 minutes | Do not flag a discrepancy using uncorrected timestamps. |
| split_shipment | confirmed_exception | Ordered quantity exceeds fulfilled quantity and carrier reports partial delivery | Do not describe the entire order as undelivered. |
| associated_goodwill_credit | control | Delivery evidence is complete; finance record is explicitly a goodwill adjustment; no operational exception evidence | Do not infer the credit was caused by an operational failure. |
| indeterminate_delivery | indeterminate | WMS delivered, no carrier event, support missing-package case, finance adjustment; evidence does not resolve physical delivery or cause | Do not choose confirmed delivery failure or confirmed successful delivery. |

## 5. Financial classification

Apply these labels independently from the operational finding:

- **Observed transaction:** transaction exists in finance data.
- **Associated only:** transaction shares an order reference with an exception; causation is not established.
- **Associated, not causal:** transaction reason explicitly indicates goodwill/courtesy and there is no operational evidence tying it to an exception.
- **Causally attributed:** only when independent evidence and a pre-registered causal rule support attribution. No v1 synthetic row qualifies.
- **Indeterminate:** the transaction exists but its relationship to the event cannot be resolved.

The v1 data contains no verified avoidable amount, recovered value, or ROI. Never sum associated refunds and call the total losses or savings.

## 6. Severity guidance

- **High:** unresolved delivery/status contradiction with a customer impact signal.
- **Medium:** fulfillment or shipment completeness discrepancy.
- **Low:** data latency or duplicate event that affects record quality but does not alone establish customer harm.
- **None:** control case.
- **Unknown:** indeterminate case.

Severity is an evaluation aid, not a legal or financial conclusion.

## 7. Independent review and adjudication

1. Two reviewers independently label each order without seeing the generated reference label.
2. Each reviewer cites source record IDs and records a concise rationale.
3. Compare disagreements only after both label sets are locked.
4. A third reviewer adjudicates disagreements and records the reason.
5. Preserve original labels, adjudicated label, reviewer identities/roles, timestamps, and manual version.
6. Do not silently edit the reference labels to match a system's output.
7. Any change to rules requires a new manual version and, where appropriate, a new sealed holdout set.

The included `ground_truth.csv` is the generator's expected synthetic label set. It is not independent adjudication. Before a formal blind benchmark, reviewers must independently re-label the holdout set and adjudicate it under this manual.

## 8. Known v1 limitations

- One synthetic summary row per order per source, rather than full event histories.
- Fixed category blocks of 50 orders each; not representative of real operational prevalence.
- Deterministic scenario construction can be learned; this dataset must not be used as a sealed external holdout once the generator and labels are public.
- No real connector behavior, carrier integration, ERP semantics, privacy controls, or production-scale performance is tested.
- No v1 financial transaction supports causal attribution or recovered-value claims.

## 9. Acceptance before comparative use

Do not call this an independent benchmark until:
- independent reviewers have completed and adjudicated labels;
- the final test package is frozen and hashed;
- a leakage-safe, undisclosed holdout is created for comparative runs;
- participant access, configuration time, and support are documented;
- the scoring formulas and thresholds are preregistered;
- all integrity gates are evaluated.
