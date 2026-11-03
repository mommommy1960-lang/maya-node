# Whole Story Challenge — Synthetic Warehouse Demonstration

**Status:** Illustrative synthetic demonstration; not a customer case, production capability claim, or competitor benchmark.

This exercise connects four ordinary operational record sets: warehouse management events, carrier scans, customer support records, and finance credits/refunds.

The case contains five synthetic orders on 2026-10-15. The WMS-only view is limited to what the WMS records. The cross-system demonstrator joins records by order ID, identifies discrepancies, and reports supporting source IDs.

## Run

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

- `data/wms_events.csv`
- `data/carrier_events.csv`
- `data/customer_support.csv`
- `data/finance_transactions.csv`
- `ground_truth.md`
- `run_challenge.py`
