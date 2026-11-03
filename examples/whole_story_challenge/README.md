# Whole Story Challenge — Synthetic Warehouse Demonstration

**Status:** Illustrative synthetic demonstration; not a customer case, production capability claim, or competitor benchmark.

This exercise connects four ordinary operational record sets: warehouse management events, carrier scans, customer support records, and finance credits/refunds.

The case contains five synthetic orders on 2026-10-15. The WMS-only view is limited to what the WMS records. The cross-system demonstrator joins records by order ID, identifies discrepancies, and reports supporting source IDs.

## Explore the customer-facing demonstration

Open [customer_demo.html](./customer_demo.html) in a browser. The standalone page lets a prospective customer:

- switch between a warehouse-only view and the combined Whole Story view;
- filter orders by whether the cross-system rules flag them for review;
- expand each order to inspect source records and the reason for review;
- see the evidence sources, rule thresholds, and financial limitations.

The page uses embedded fictional records and runs locally in the browser. It does not connect to customer systems, send data, or invoke Maya Node. It is a concept prototype, not a hosted customer service.

## Competitive comparison discipline

See the [competitive benchmark protocol](../../docs/WHOLE_STORY_CHALLENGE_COMPETITIVE_BENCHMARK_PROTOCOL_2026-11-03.md) for the documented alternative landscape, public vendor capability claims, blind-test design, scorecard, and rules for what Civic Continuum may claim. The protocol explicitly distinguishes public vendor descriptions from tested performance.

## Run the reproducible reconciliation

Requires Python 3.10+ and only the Python standard library.

```bash
python examples/whole_story_challenge/run_challenge.py
```

Save the report with:

```bash
python examples/whole_story_challenge/run_challenge.py > whole_story_report.md
```

## What this proves — and does not prove

It proves that the included deterministic rules can reproduce the explicitly defined synthetic findings from the included records. It does **not** prove that Maya Node's deployed product performs this analysis, that an incumbent vendor would miss these findings, that the records establish legal fault, or that any credit was caused by a specific operational event.

The comparison is between a WMS-only record view and a transparent cross-source reconciliation demonstrator. It is not a test against Amazon, Celonis, SAP, or another commercial platform.

## Evidence discipline

- All records are fictional and use synthetic IDs.
- All timestamps are local operational timestamps on the same date; no timezone conversion is required in this small example.
- A carrier scan absence means **no matching scan in this dataset**, not proof that no physical event occurred.
- A refund or credit is a documented transaction associated with an order, not a proven consequence of a particular delay.
- Financial amounts are observed transactions, not recovered savings or causal loss.
- The independent ground-truth reference is in `ground_truth.md`.

## Files

- `customer_demo.html` — standalone interactive customer exploration page
- `data/wms_events.csv`
- `data/carrier_events.csv`
- `data/customer_support.csv`
- `data/finance_transactions.csv`
- `ground_truth.md`
- `run_challenge.py`
- `sample_output.md`
