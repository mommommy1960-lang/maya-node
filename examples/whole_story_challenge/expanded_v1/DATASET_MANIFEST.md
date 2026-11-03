# Dataset Manifest — Expanded Synthetic v1

- Dataset ID: `whole-story-synthetic-v1`
- Generated: 2026-11-03
- Generator: `generate_dataset.py`
- Seed: deterministic arithmetic sequence; no external randomness
- Orders: 500 unique order IDs (`ORD-0001`–`ORD-0500`)
- Source rows: 500 WMS, 500 carrier, 500 support, 500 finance
- Ground-truth rows: 500
- Scenario categories: 10, exactly 50 orders each
- Timezone: UTC; timestamps use ISO 8601 `Z`
- Currency: USD
- Data classification: entirely fictional synthetic test data
- Reference labels: generator expected labels; not independently adjudicated
- Holdout status: public/development only; not a sealed holdout
- Financial causation: no v1 transaction is independently established as causally attributable, avoidable, or recovered
- Benchmark status: not a completed competitive benchmark

## Category and label counts

| Category | Count | Label |
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

## Schema notes

Each CSV has one row per order, per source. Empty timestamps mean no corresponding carrier event is supplied. Explicit `NONE` values mean no support case or finance transaction in that source row; they are not missing data. The carrier duplicate marker and known clock offset are explicit synthetic test metadata. All timestamps and values are generated fixtures.

## Integrity note

Cryptographic hashes must be computed on the committed file bytes at the time a benchmark package is frozen. This manifest intentionally does not claim hashes before the final Git commit is established.
