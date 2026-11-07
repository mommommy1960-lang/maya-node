"""Operation Operator: synthetic-only read-only adapter contract.
No network, credentials, customer data or dispatch capability.
"""
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class HandoffWindow:
    """Confirmed fictional capacity reserved for this request, in its unit."""

    storage_capacity: int
    transport_capacity: int
    arrival_minute: int
    deadline_minute: int

    def __post_init__(self):
        values = (self.storage_capacity, self.transport_capacity,
                  self.arrival_minute, self.deadline_minute)
        if any(type(value) is not int or value < 0 for value in values):
            raise ValueError("Handoff capacity and times must be nonnegative integers")


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
    priority: int = 0
    handoff: HandoffWindow | None = None

    def __post_init__(self):
        if not self.synthetic or not self.partner_id.startswith("demo-") or not self.site_id.startswith("demo-"):
            raise ValueError("Operation Operator fixture accepts fictional records only")
        if not self.source_record_id.startswith("demo-") or self.kind not in ("surplus", "need"):
            raise ValueError("Invalid fictional record")
        if not isinstance(self.quantity, int) or isinstance(self.quantity, bool) or self.quantity <= 0:
            raise ValueError("Quantity must be positive integer")
        if not self.category or self.unit not in ("boxes", "kg", "lb", "gallons"):
            raise ValueError("Invalid food category or unit")
        if type(self.priority) is not int or self.priority < 0:
            raise ValueError("Priority must be a nonnegative integer")
        if self.handoff is not None and (
            self.kind != "need" or not isinstance(self.handoff, HandoffWindow)
        ):
            raise ValueError("Handoff capacity must belong to a fictional request")

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
    def record_key(signal: FoodSignal) -> tuple[str, str, str]:
        return signal.source_record_id, signal.partner_id, signal.site_id

    supplies = sorted(adapter.fetch_surplus(), key=record_key)
    needs = sorted(adapter.fetch_needs(), key=lambda need: (-need.priority, record_key(need)))
    remaining = {record_key(supply): supply.quantity for supply in supplies}
    proposals = []
    for need in needs:
        needed = need.quantity
        handoff = need.handoff
        if handoff is None and (need.unit == "gallons" or need.category.casefold() == "milk"):
            continue
        if handoff is not None:
            if handoff.arrival_minute > handoff.deadline_minute:
                continue
            needed = min(needed, handoff.storage_capacity, handoff.transport_capacity)
        for surplus in supplies:
            if needed == 0:
                break
            if surplus.category != need.category or surplus.unit != need.unit or surplus.site_id == need.site_id:
                continue
            supply_key = record_key(surplus)
            qty = min(needed, remaining[supply_key])
            if qty <= 0:
                continue
            proposals.append({"from": surplus.site_id, "to": need.site_id,
                              "category": need.category, "quantity": qty, "unit": need.unit,
                              "source_refs": [surplus.source_record_id, need.source_record_id],
                              "request_priority": need.priority,
                              "allocation_rule": "higher priority first, then stable source record order",
                              "human_approval_required": True, "dispatched": False, "synthetic": True})
            needed -= qty
            remaining[supply_key] -= qty
    return proposals
