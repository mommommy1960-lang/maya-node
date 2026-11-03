# Independent Ground-Truth Reference — Synthetic Case

**Dataset:** Whole Story Challenge synthetic warehouse case  
**Date represented:** 2026-10-15  
**Purpose:** Expected findings for validating the deterministic demonstration.  
**Not a real company, customer, worker, carrier, or transaction.**

| Order | Expected finding | Evidence | Classification |
|---|---|---|---|
| ORD-100 | Carrier pickup occurred 22 minutes after the WMS promised-ship-by time; carrier pickup was 37 minutes after the WMS marked-dispatched time. Delivery scans differ by 30 minutes (WMS 13:50 vs carrier 14:20). A late-delivery complaint and $45 refund are recorded. | WMS-100, CAR-100, SUP-100, FIN-100 | Confirmed record discrepancies and associated transactions; causation of refund not established |
| ORD-101 | Carrier delivery was 40 minutes after the WMS marked-delivered time. A delivery-delay complaint and $12 service credit are recorded. | WMS-101, CAR-101, SUP-101, FIN-101 | Confirmed timestamp discrepancy and associated transactions; causation not established |
| ORD-102 | WMS records delivered, but this dataset contains no carrier pickup or delivery scan. A missing-package complaint and $80 refund are recorded. | WMS-102, absence of matching carrier row, SUP-102, FIN-102 | Confirmed record-set gap and associated transactions; no proof that physical delivery did not occur |
| ORD-103 | WMS and carrier delivery times differ by 2 minutes; no support or finance exception row. | WMS-103, CAR-103 | No material discrepancy under the 5-minute comparison tolerance |
| ORD-104 | WMS and carrier delivery times differ by 2 minutes; no support or finance exception row. | WMS-104, CAR-104 | No material discrepancy under the 5-minute comparison tolerance |

## Expected aggregate facts

- Orders in WMS dataset: 5
- Orders with material cross-source findings: 3
- Orders with a support complaint: 3
- Orders with a finance credit/refund: 3
- Documented credits/refunds associated with the three flagged orders: **$137.00**
- Amount established as causally attributable to the identified operational discrepancies: **$0.00 proven by this dataset** (causation is not established)

The $137.00 is a sum of recorded financial transactions, not a claim of recoverable savings, proven operational loss, or causal damages.

## Scoring notes

The demonstrator should identify ORD-100, ORD-101, and ORD-102, cite the listed source records, preserve the uncertainty on ORD-102's absent scan, and avoid claiming causation for the financial transactions. ORD-103 and ORD-104 should not be raised as material delivery-time exceptions using a 5-minute tolerance.
