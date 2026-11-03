# Whole Story Challenge — Expanded Synthetic Dataset v1

**Created:** 2026-11-03  
**Status:** Synthetic engineering/dry-run dataset; not an independent benchmark result  
**Size:** 500 fictional orders; 10 scenario categories; 50 orders per category

## Files

- `wms_events.csv` — 500 synthetic WMS order-status/fulfillment records.
- `carrier_events.csv` — 500 synthetic carrier records, including explicit missing-event rows.
- `customer_support.csv` — 500 synthetic support status rows, including explicit no-case rows.
- `finance_transactions.csv` — 500 synthetic finance rows, including explicit no-transaction rows.
- `ground_truth.csv` — expected synthetic labels and narrow finding statements.
- `LABELING_MANUAL.md` — category rules, uncertainty boundaries, finance labels, and independent review procedure.
- `DATASET_MANIFEST.md` — schema, category counts, limitations, and integrity status.
- `generate_dataset.py` — deterministic standard-library generator.

## Scenario mix

| Category | Orders | Expected outcome |
|---|---:|---|
| clean_control | 50 | control |
| missing_carrier_scan | 50 | confirmed_exception |
| late_edi_delivery | 50 | confirmed_exception |
| status_contradiction | 50 | confirmed_exception |
| inventory_shortage | 50 | confirmed_exception |
| duplicate_carrier_event | 50 | confirmed_exception |
| known_clock_skew | 50 | control |
| split_shipment | 50 | confirmed_exception |
| associated_goodwill_credit | 50 | control |
| indeterminate_delivery | 50 | indeterminate |
| **Total** | **500** | |

## Important interpretation

This is a balanced, deterministic synthetic dataset. It is intentionally not a representative sample of warehouse operations. The 50/50 scenario blocks make it useful for exercising category logic, but prevalence, accuracy in the wild, scalability, financial recovery, and ROI cannot be inferred from it.

The reference labels are generated expected labels, not independently adjudicated truth. The dataset and labels are public in this repository; therefore this version is **not a blind holdout**. Use it for development, validation, parser/scoring tests, and reviewer training. Generate a new sealed holdout with an independent seed and restricted label access before a comparative benchmark.

All identifiers and transactions are fictional. Amounts are test fixtures only. No real person, company, customer, shipment, carrier, or financial account is represented.

## Reproduction

Run with Python 3.10+ and the standard library:

```bash
python generate_dataset.py --output-dir .
```

The script overwrites only the five generated CSV files in the specified output directory. Review the diff before committing regenerated outputs.

## Related documents

- [Benchmark specification and scoring framework](../../docs/WHOLE_STORY_CHALLENGE_BENCHMARK_SPEC_AND_SCORING_2026-11-03.md)
- [Competitive benchmark protocol](../../docs/WHOLE_STORY_CHALLENGE_COMPETITIVE_BENCHMARK_PROTOCOL_2026-11-03.md)
