# Whole Story Challenge — Sample Output

**Synthetic demonstration only.** These are fictional records and deterministic rule outputs, not findings about a real operator or a deployed Maya Node production system.

## WMS-only view

- WMS orders represented: **5**
- WMS status recorded as delivered: **5**
- A WMS-only status view does not contain the carrier, support, or finance rows needed to reconcile the full sequence.

## Cross-system findings

- Orders with one or more rule-triggered findings: **3**

### ORD-100

- Carrier pickup was 22 minutes after the WMS promised-ship-by time.
- Carrier pickup and WMS dispatch timestamps differ by 37 minutes.
- Carrier and WMS delivery timestamps differ by 30 minutes.
- Customer support recorded a late_delivery complaint.
- Finance recorded a customer_refund of $45.00; causation is not established.
- Evidence references: WMS-100, CAR-100, SUP-100, FIN-100

### ORD-101

- Carrier and WMS delivery timestamps differ by 40 minutes.
- Customer support recorded a delivery_delay complaint.
- Finance recorded a service_credit of $12.00; causation is not established.
- Evidence references: WMS-101, CAR-101, SUP-101, FIN-101

### ORD-102

- No matching carrier scan row exists in this dataset; physical delivery is not disproved.
- Customer support recorded a missing_package complaint.
- Finance recorded a customer_refund of $80.00; causation is not established.
- Evidence references: WMS-102, SUP-102, FIN-102

## Financial records associated with flagged orders

- Recorded refunds/credits: **$137.00**
- This is the sum of finance transactions linked by order ID. It is not proof that the identified discrepancies caused those transactions, and it is not a savings or recovery claim.

## Interpretation and limitations

- A missing carrier row means no matching scan was present in this supplied dataset; it does not prove that pickup or delivery never happened.
- Timestamp differences are record discrepancies. Clock synchronization, scan latency, time-zone handling, and source-system semantics would need validation in a real pilot.
- Findings are rule-based and human-reviewable. No blame, misconduct, legal conclusion, or automated operational action is inferred.

## Deterministic acceptance checks

- PASS — flagged order set matches ground truth
- PASS — associated finance total equals $137.00
- PASS — exactly five WMS orders loaded

The run used the included synthetic CSVs and Python standard library only. It did not access external systems.
