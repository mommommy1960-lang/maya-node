"""Deterministic, synthetic-only pantry reconciliation. No network, payments, or dispatch."""
from decimal import Decimal, InvalidOperation
from collections import defaultdict

def analyze(records):
    """Compare demo purchase, delivery and inventory records; return review-only findings."""
    if not isinstance(records, list) or len(records)>500:
        raise ValueError("Expected at most 500 synthetic records")
    groups=defaultdict(lambda: {"ordered":0,"received":0,"stocked":0,"paid":Decimal("0"),"expected_cost":Decimal("0"),"references":[]})
    for row in records:
        if not isinstance(row,dict) or row.get("synthetic") is not True:
            raise ValueError("Every record must be explicitly synthetic")
        kind=row.get("kind")
        if kind not in ("order","delivery","inventory","payment"):
            raise ValueError("Invalid record kind")
        key=row.get("order_id")
        if not isinstance(key,str) or not key.startswith("demo-") or len(key)>64:
            raise ValueError("Synthetic order_id required")
        qty=row.get("quantity",0)
        if type(qty) is not int or qty<0 or qty>100000:
            raise ValueError("Invalid quantity")
        if kind=="payment" and qty!=0:
            raise ValueError("Payment quantity must be zero")
        try:
            amount=Decimal(str(row.get("amount","0")))
        except (InvalidOperation,ValueError):
            raise ValueError("Invalid amount") from None
        if not amount.is_finite() or amount<0 or amount>Decimal("10000000") or amount.as_tuple().exponent < -2:
            raise ValueError("Invalid amount")
        if kind not in ("order","payment") and amount!=0:
            raise ValueError("Unexpected amount")
        g=groups[key]
        g["references"].append(kind)
        if kind=="order":
            g["ordered"]+=qty
            g["expected_cost"]+=amount
        elif kind=="delivery":g["received"]+=qty
        elif kind=="inventory":g["stocked"]+=qty
        else:g["paid"]+=amount
    findings=[]
    for key,g in sorted(groups.items()):
        if g["ordered"]>g["received"]:
            findings.append({"order_id":key,"type":"missing_delivery","difference":g["ordered"]-g["received"],"severity":"review","evidence":sorted(g["references"])})
        if g["received"]>g["stocked"]:
            findings.append({"order_id":key,"type":"unaccounted_inventory","difference":g["received"]-g["stocked"],"severity":"review","evidence":sorted(g["references"])})
        if g["paid"]>g["expected_cost"]:
            findings.append({"order_id":key,"type":"payment_exceeds_order","difference":str(g["paid"]-g["expected_cost"]),"severity":"review","evidence":sorted(g["references"])})
        if g["received"]>g["ordered"]:
            findings.append({"order_id":key,"type":"unexpected_delivery","difference":g["received"]-g["ordered"],"severity":"review","evidence":sorted(g["references"])})
    return {"mode":"synthetic_only","human_approval_required":True,"automated_actions":False,"orders_reviewed":len(groups),"findings":findings,"disclaimer":"Discrepancies are not evidence of theft or misconduct. Review underlying records before conclusions."}
