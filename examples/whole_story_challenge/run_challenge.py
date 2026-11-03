#!/usr/bin/env python3
"""Deterministic cross-source reconciliation for the synthetic Whole Story Challenge.

This is a small, auditable demonstration—not the deployed Maya Node product.
It uses only the Python standard library and never connects to external systems.
"""
from __future__ import annotations

import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DELIVERY_TOLERANCE_MINUTES = 5


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def minutes_between(later: str, earlier: str) -> int:
    return int((parse_time(later) - parse_time(earlier)).total_seconds() // 60)


def money(value: Decimal) -> str:
    return f"${value:,.2f}"


def main() -> None:
    wms_rows = read_csv("wms_events.csv")
    carrier_rows = {row["order_id"]: row for row in read_csv("carrier_events.csv")}
    support_rows = {row["order_id"]: row for row in read_csv("customer_support.csv")}
    finance_rows = {row["order_id"]: row for row in read_csv("finance_transactions.csv")}

    findings: list[dict[str, object]] = []
    associated_credits = Decimal("0.00")

    for wms in wms_rows:
        order_id = wms["order_id"]
        carrier = carrier_rows.get(order_id)
        support = support_rows.get(order_id)
        finance = finance_rows.get(order_id)
        reasons: list[str] = []
        evidence = [wms["wms_record_id"]]

        if carrier is None:
            reasons.append("No matching carrier scan row exists in this dataset; physical delivery is not disproved.")
        else:
            evidence.append(carrier["carrier_record_id"])
            pickup_delay = minutes_between(
                carrier["carrier_pickup_at"], wms["promised_ship_by"]
            )
            if pickup_delay > 0:
                reasons.append(
                    f"Carrier pickup was {pickup_delay} minutes after the WMS promised-ship-by time."
                )

            dispatch_gap = minutes_between(
                carrier["carrier_pickup_at"], wms["marked_dispatched_at"]
            )
            if abs(dispatch_gap) > DELIVERY_TOLERANCE_MINUTES:
                reasons.append(
                    f"Carrier pickup and WMS dispatch timestamps differ by {abs(dispatch_gap)} minutes."
                )

            delivery_gap = minutes_between(
                carrier["carrier_delivered_at"], wms["marked_delivered_at"]
            )
            if abs(delivery_gap) > DELIVERY_TOLERANCE_MINUTES:
                reasons.append(
                    f"Carrier and WMS delivery timestamps differ by {abs(delivery_gap)} minutes."
                )

        if support:
            evidence.append(support["support_record_id"])
            reasons.append(f"Customer support recorded a {support['complaint_type']} complaint.")

        if finance:
            evidence.append(finance["finance_record_id"])
            amount = Decimal(finance["amount_usd"])
            associated_credits += amount
            reasons.append(
                f"Finance recorded a {finance['transaction_type']} of {money(amount)}; causation is not established."
            )

        if reasons:
            findings.append({
                "order_id": order_id,
                "reasons": reasons,
                "evidence": evidence,
            })

    print("# Whole Story Challenge — Cross-System Reconciliation Report")
    print()
    print("> Synthetic demonstration only. These are fictional records and deterministic rule outputs, not findings about a real operator or a deployed Maya Node production system.")
    print()
    print("## WMS-only view")
    print()
    print(f"- WMS orders represented: **{len(wms_rows)}**")
    print("- WMS status recorded as delivered: **"
          f"{sum(1 for row in wms_rows if row['wms_status'] == 'delivered')}**")
    print("- A WMS-only status view does not contain the carrier, support, or finance rows needed to reconcile the full sequence.")
    print()
    print("## Cross-system findings")
    print()
    print(f"- Orders with one or more rule-triggered findings: **{len(findings)}**")
    for finding in findings:
        print()
        print(f"### {finding['order_id']}")
        for reason in finding["reasons"]:
            print(f"- {reason}")
        print(f"- Evidence references: {', '.join(finding['evidence'])}")

    print()
    print("## Financial records associated with flagged orders")
    print()
    print(f"- Recorded refunds/credits: **{money(associated_credits)}**")
    print("- This is the sum of finance transactions linked by order ID. It is not proof that the identified discrepancies caused those transactions, and it is not a savings or recovery claim.")
    print()
    print("## Interpretation and limitations")
    print()
    print("- A missing carrier row means no matching scan was present in this supplied dataset; it does not prove that pickup or delivery never happened.")
    print("- Timestamp differences are record discrepancies. Clock synchronization, scan latency, time-zone handling, and source-system semantics would need validation in a real pilot.")
    print("- Findings are rule-based and human-reviewable. No blame, misconduct, legal conclusion, or automated operational action is inferred.")
    print("- The independent ground-truth reference is documented in ground_truth.md.")
    print()
    print("## Deterministic acceptance checks")
    print()
    expected_ids = {"ORD-100", "ORD-101", "ORD-102"}
    actual_ids = {str(item["order_id"]) for item in findings}
    checks = {
        "flagged order set matches ground truth": actual_ids == expected_ids,
        "associated finance total equals $137.00": associated_credits == Decimal("137.00"),
        "exactly five WMS orders loaded": len(wms_rows) == 5,
    }
    for label, passed in checks.items():
        print(f"- {'PASS' if passed else 'FAIL'} — {label}")
    if not all(checks.values()):
        raise SystemExit("One or more deterministic acceptance checks failed.")


if __name__ == "__main__":
    main()
