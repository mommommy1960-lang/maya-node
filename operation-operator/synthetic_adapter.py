"""Operation Operator: synthetic-only read-only adapter contract.
No network, credentials, customer data or dispatch capability.
"""
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class FoodSignal:
    partner_id: str
    site_id: str
    source_record_id: str
    kind: str
    category: str
    quantity: int
    unit: str
    synthetic: bool = True

    def __post_init__(self):
        if not self.synthetic or not self.partner_id.startswith("demo-") or not self.site_id.startswith("demo-"):
            raise ValueError("Operation Operator fixture accepts fictional records only")
        if not self.source_record_id.startswith("demo-") or self.kind not in ("surplus", "need"):
            raise ValueError("Invalid fictional record")
        if not isinstance(self.quantity, int) or isinstance(self.quantity, bool) or self.quantity <= 0:
            raise ValueError("Quantity must be positive integer")
        if not self.category or self.unit not in ("boxes", "kg", "lb"):
            raise ValueError("Invalid food category or unit")

class ReadOnlyAdapter(Protocol):
    def describe_capabilities(self) -> dict: ...
    def fetch_surplus(self) -> tuple[FoodSignal, ...]: ...
    def fetch_needs(self) -> tuple[FoodSignal, ...]: ...

class SyntheticAdapter:
    def __init__(self, records: tuple[FoodSignal, ...]):
        if not all(isinstance(x, FoodSignal) and x.synthetic for x in records):
            raise ValueError("Only fictional records accepted")
        self._records = records

    def describe_capabilities(self) -> dict:
        return {"mode": "synthetic_only", "read_only": True, "outbound_actions": False, "customer_ready": False}

    def fetch_surplus(self) -> tuple[FoodSignal, ...]:
        return tuple(x for x in self._records if x.kind == "surplus")

    def fetch_needs(self) -> tuple[FoodSignal, ...]:
        return tuple(x for x in self._records if x.kind == "need")

def propose_matches(adapter: ReadOnlyAdapter) -> list[dict]:
    caps = adapter.describe_capabilities()
    if caps.get("mode") != "synthetic_only" or not caps.get("read_only") or caps.get("outbound_actions"):
        raise PermissionError("Only read-only synthetic adapters are authorized")
    proposals = []
    remaining = {s.source_record_id: s.quantity for s in adapter.fetch_surplus()}
    for need in adapter.fetch_needs():
        needed = need.quantity
        for surplus in adapter.fetch_surplus():
            if needed == 0:
                break
            if surplus.category != need.category or surplus.unit != need.unit or surplus.site_id == need.site_id:
                continue
            qty = min(needed, remaining[surplus.source_record_id])
            if qty <= 0:
                continue
            proposals.append({"from": surplus.site_id, "to": need.site_id,
                              "category": need.category, "quantity": qty, "unit": need.unit,
                              "source_refs": [surplus.source_record_id, need.source_record_id],
                              "human_approval_required": True, "dispatched": False, "synthetic": True})
            needed -= qty
            remaining[surplus.source_record_id] -= qty
    return proposals
