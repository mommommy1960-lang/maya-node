#!/usr/bin/env python3
"""Generate Whole Story Challenge synthetic v1. Standard library only."""
import argparse
import csv
from pathlib import Path

CATEGORIES = [
    "clean_control", "missing_carrier_scan", "late_edi_delivery",
    "status_contradiction", "inventory_shortage", "duplicate_carrier_event",
    "known_clock_skew", "split_shipment", "associated_goodwill_credit",
    "indeterminate_delivery",
]
FIELDS = {
    "wms_events.csv": ["order_id","wms_record_id","event_type","status","event_time_utc","ingested_at_utc","quantity_ordered","quantity_fulfilled","notes"],
    "carrier_events.csv": ["order_id","carrier_record_id","shipment_id","event_type","status","event_time_utc","ingested_at_utc","duplicate_count","known_clock_offset_minutes","notes"],
    "customer_support.csv": ["order_id","support_record_id","case_status","issue_type","created_at_utc","notes"],
    "finance_transactions.csv": ["order_id","finance_record_id","transaction_type","amount_usd","posted_at_utc","reason","causation_evidence"],
    "ground_truth.csv": ["order_id","case_category","expected_label","expected_finding","severity","financial_causation","adjudication_note"],
}

def timestamp(day, hour, minute=0):
    return f"2026-10-{day:02d}T{hour:02d}:{minute:02d}:00Z"

def build(i):
    category = CATEGORIES[(i - 1) // 50]
    order = f"ORD-{i:04d}"
    day = 1 + ((i - 1) % 28)
    w = [order, f"WMS-{i}", "FULFILLMENT_STATUS", "DELIVERED", timestamp(day,10), timestamp(day,10,2), 1, 1, "Synthetic record; fictional data"]
    c = [order, f"CAR-{i}", f"SHP-{i}", "SHIPMENT_STATUS", "DELIVERED", timestamp(day,14), timestamp(day,14,3), 1, 0, "Synthetic carrier record"]
    s = [order, f"SUP-{i}", "NONE", "NONE", timestamp(day,16), "No support exception recorded"]
    f = [order, f"FIN-{i}", "NONE", "0.00", timestamp(day,17), "NONE", "No financial transaction"]
    label, finding, severity, financial = "control", "No material exception under the benchmark rules", "none", "none"
    note = "Control case; no material exception is expected."
    if category == "missing_carrier_scan":
        c[4], c[5], c[6], c[9] = "IN_TRANSIT", timestamp(day,11), timestamp(day,11,2), "No delivery scan in supplied carrier record"
        s[2:4] = ["OPEN","MISSING_PACKAGE"]; s[5] = "Customer reports missing package"
        f[2:6] = ["REFUND","80.00",timestamp(day,17),"Missing package complaint"]
        label, finding, severity, financial = "confirmed_exception", "WMS reports delivered but carrier delivery scan is absent and support reports missing package", "high", "associated_only"
        note = "Conflicting evidence supports investigation, not a conclusion that delivery did not occur. Refund is associated, not proven caused."
    elif category == "late_edi_delivery":
        c[5], c[6], c[9] = timestamp(day,13), timestamp(day,19), "Delivery event ingested six hours after event time; delayed EDI"
        label, finding, severity = "confirmed_exception", "Carrier delivery event arrived six hours after its event timestamp", "low"
        note = "Delivery itself is recorded; the material finding is event-data latency, not failed delivery."
    elif category == "status_contradiction":
        c[4], c[9] = "DELIVERY_EXCEPTION", "Carrier exception conflicts with WMS delivered status"
        s[2:4] = ["OPEN","NOT_RECEIVED"]; s[5] = "Customer reports non-receipt"
        f[2:6] = ["CREDIT","25.00",timestamp(day,17),"Service credit"]
        label, finding, severity, financial = "confirmed_exception", "WMS delivered status conflicts with carrier delivery exception and customer non-receipt report", "high", "associated_only"
        note = "Evidence establishes a status contradiction; it does not independently establish final physical disposition or credit causation."
    elif category == "inventory_shortage":
        w[3], w[7], w[8] = "SHORT_PICK", 0, "Order allocated but no units fulfilled; synthetic shortage marker"
        c[4:7] = ["NOT_TENDERED","",""]
        s[2:4] = ["OPEN","ORDER_DELAY"]; s[5] = "Customer reports order delay"
        f[2:6] = ["CREDIT","20.00",timestamp(day,17),"Delay courtesy credit"]
        label, finding, severity, financial = "confirmed_exception", "WMS records zero fulfilled quantity and carrier has no tender event", "medium", "associated_only"
        note = "Records support an unfulfilled order exception; credit causation is not established."
    elif category == "duplicate_carrier_event":
        c[7], c[9] = 2, "Same carrier business event appears twice under distinct source record IDs"
        label, finding, severity = "confirmed_exception", "Duplicate carrier event replay detected", "low"
        note = "Duplicate count is a synthetic ground-truth marker; count one underlying business event, not two deliveries."
    elif category == "known_clock_skew":
        c[5], c[6], c[8], c[9] = timestamp(day,10,10), timestamp(day,10,12), 10, "Carrier source clock is known to be ten minutes fast; normalize before comparison"
        note = "Naive timestamp comparison would create a false alert; known offset resolves the discrepancy."
    elif category == "split_shipment":
        w[3], w[6], w[7] = "PARTIALLY_FULFILLED", 2, 1
        c[4], c[9] = "PARTIAL_DELIVERY", "Carrier reports partial delivery"
        s[2:4] = ["OPEN","MISSING_ITEM"]; s[5] = "Customer reports missing item"
        f[2:6] = ["CREDIT","15.00",timestamp(day,17),"Partial shipment credit"]
        label, finding, severity, financial = "confirmed_exception", "Two-unit order has only one fulfilled unit and carrier reports partial delivery", "medium", "associated_only"
        note = "Partial fulfillment is supported; credit is associated but not proven avoidable or caused by a specific failure."
    elif category == "associated_goodwill_credit":
        f[2:6] = ["REFUND","12.00",timestamp(day,17),"Goodwill courtesy adjustment"]
        f[6] = "Explicit goodwill reason; no operational exception evidence"
        financial = "associated_not_causal"
        note = "Do not classify a finance transaction as an operational failure solely because it references the order."
    elif category == "indeterminate_delivery":
        c[4:7] = ["","",""]; c[9] = "No carrier event supplied in this case"
        s[2:4] = ["OPEN","MISSING_PACKAGE"]; s[5] = "Customer reports missing package; delivery outcome unresolved"
        f[2:6] = ["REFUND","40.00",timestamp(day,17),"Customer complaint adjustment"]
        label, finding, severity, financial = "indeterminate", "Insufficient evidence to determine delivery outcome or cause", "unknown", "indeterminate"
        note = "WMS delivered status, absent carrier record, complaint, and refund do not establish what physically happened or why."
    truth = [order, category, label, finding, severity, financial, note]
    return {"wms_events.csv":w, "carrier_events.csv":c, "customer_support.csv":s, "finance_transactions.csv":f, "ground_truth.csv":truth}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows = {name: [] for name in FIELDS}
    for i in range(1, 501):
        item = build(i)
        for name, row in item.items():
            rows[name].append(row)
    for name, header in FIELDS.items():
        with (out / name).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(header)
            writer.writerows(rows[name])
        print(f"{name}: {len(rows[name])} rows")

if __name__ == "__main__":
    main()
