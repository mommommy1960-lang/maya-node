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
    storage_pool: str | None = None
    transport_pool: str | None = None

    def __post_init__(self):
        values = (self.storage_capacity, self.transport_capacity,
                  self.arrival_minute, self.deadline_minute)
        if any(type(value) is not int or value < 0 for value in values):
            raise ValueError("Handoff capacity and times must be nonnegative integers")
        for pool in (self.storage_pool, self.transport_pool):
            if pool is not None and (not isinstance(pool, str) or not pool.startswith("demo-")):
                raise ValueError("Capacity pools must use fictional identifiers")


@dataclass(frozen=True)
class SaleTerms:
    """Fictional evidence supplied by an authorized operator."""

    seller_authorized: bool
    resale_eligible: bool
    donation_options_exhausted: bool
    unit_price_cents: int

    def __post_init__(self):
        if type(self.unit_price_cents) is not int or self.unit_price_cents <= 0:
            raise ValueError("A sale requires a positive unit price in USD cents")

    @property
    def permits_proposal(self) -> bool:
        return (self.seller_authorized is True and self.resale_eligible is True
                and self.donation_options_exhausted is True)


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
    sale_terms: SaleTerms | None = None
    buyer_max_unit_price_cents: int | None = None

    def __post_init__(self):
        if not self.synthetic or not self.partner_id.startswith("demo-") or not self.site_id.startswith("demo-"):
            raise ValueError("Operation Operator fixture accepts fictional records only")
        if not self.source_record_id.startswith("demo-") or self.kind not in ("surplus", "need", "storage", "buyer"):
            raise ValueError("Invalid fictional record")
        if not isinstance(self.quantity, int) or isinstance(self.quantity, bool) or self.quantity <= 0:
            raise ValueError("Quantity must be positive integer")
        if not self.category or self.unit not in ("boxes", "kg", "lb", "gallons"):
            raise ValueError("Invalid food category or unit")
        if type(self.priority) is not int or self.priority < 0:
            raise ValueError("Priority must be a nonnegative integer")
        if self.handoff is not None and (
            self.kind not in ("need", "storage", "buyer") or not isinstance(self.handoff, HandoffWindow)
        ):
            raise ValueError("Handoff capacity must belong to a fictional receiving record")
        if self.sale_terms is not None and (
            self.kind != "surplus" or not isinstance(self.sale_terms, SaleTerms)
        ):
            raise ValueError("Sale terms must belong to a fictional surplus record")
        limit = self.buyer_max_unit_price_cents
        if limit is not None and (self.kind != "buyer" or type(limit) is not int or limit <= 0):
            raise ValueError("An opted-in fictional buyer must specify a positive price limit")

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
    return plan_redistribution(adapter)["recipient_proposals"]


def plan_redistribution(
    adapter: ReadOnlyAdapter, storage_options: tuple[FoodSignal, ...] = (),
    *, buyer_options: tuple[FoodSignal, ...] = (),
) -> dict[str, list[dict]]:
    """Draft transfers for known fictional recipients, storage sites, and buyers."""
    caps = adapter.describe_capabilities()
    if caps.get("mode") != "synthetic_only" or not caps.get("read_only") or caps.get("outbound_actions"):
        raise PermissionError("Only read-only synthetic adapters are authorized")
    def record_key(signal: FoodSignal) -> tuple[str, str, str]:
        return signal.source_record_id, signal.partner_id, signal.site_id

    if not all(isinstance(option, FoodSignal) and option.kind == "storage"
               for option in storage_options):
        raise ValueError("Storage options must be fictional storage records")
    if not all(isinstance(option, FoodSignal) and option.kind == "buyer"
               for option in buyer_options):
        raise ValueError("Buyer options must be fictional buyer records")
    supplies = sorted(adapter.fetch_surplus(), key=record_key)
    needs = sorted(adapter.fetch_needs(), key=lambda need: (-need.priority, record_key(need)))
    storage = sorted(storage_options, key=record_key)
    buyers = sorted(buyer_options, key=record_key)
    for records in (supplies, needs, storage, buyers):
        if len({record_key(record) for record in records}) != len(records):
            raise ValueError("Duplicate fictional records")
    remaining = {record_key(supply): supply.quantity for supply in supplies}
    receivers = (*needs, *storage, *buyers)
    pool_limits = {}
    receiver_pools = {}
    for receiver in receivers:
        window = receiver.handoff
        if window is None:
            continue
        pools = []
        for kind, name, capacity in (
            ("storage", window.storage_pool, window.storage_capacity),
            ("transport", window.transport_pool, window.transport_capacity),
        ):
            if name is None:
                continue
            pool = (kind, name)
            limit = (receiver.unit, capacity)
            if pool_limits.setdefault(pool, limit) != limit:
                raise ValueError("Conflicting capacity or unit for a shared fictional pool")
            pools.append(pool)
        receiver_pools[receiver] = pools
    pool_remaining = {pool: capacity for pool, (_, capacity) in pool_limits.items()}
    proposals_by_kind = {"need": [], "storage": [], "buyer": []}
    rules = {"need": "higher priority first, then stable source record order",
             "storage": "temporary storage after recipient matches",
             "buyer": "eligible resale after donation and storage"}
    for need in receivers:
        needed = need.quantity
        handoff = need.handoff
        is_buyer = need.kind == "buyer"
        requires_handoff = need.kind != "need" or need.unit == "gallons" or need.category.casefold() == "milk"
        if handoff is None and requires_handoff:
            continue
        if is_buyer and need.buyer_max_unit_price_cents is None:
            continue
        if handoff is not None:
            if handoff.arrival_minute > handoff.deadline_minute:
                continue
            needed = min(needed, handoff.storage_capacity, handoff.transport_capacity)
        pools = receiver_pools.get(need, ())
        for pool in pools:
            needed = min(needed, pool_remaining[pool])
        for surplus in supplies:
            if needed == 0:
                break
            if surplus.category != need.category or surplus.unit != need.unit or surplus.site_id == need.site_id:
                continue
            terms = surplus.sale_terms
            if is_buyer and (terms is None or not terms.permits_proposal
                             or terms.unit_price_cents > need.buyer_max_unit_price_cents):
                continue
            supply_key = record_key(surplus)
            qty = min(needed, remaining[supply_key])
            if qty <= 0:
                continue
            proposal = {"from": surplus.site_id, "to": need.site_id,
                              "category": need.category, "quantity": qty, "unit": need.unit,
                              "source_refs": [surplus.source_record_id, need.source_record_id],
                              "request_priority": need.priority,
                              "allocation_rule": rules[need.kind],
                              "human_approval_required": True, "dispatched": False, "synthetic": True}
            if is_buyer:
                proposal.update(unit_price_cents=terms.unit_price_cents,
                                total_price_cents=qty * terms.unit_price_cents,
                                currency="USD")
            proposals_by_kind[need.kind].append(proposal)
            needed -= qty
            remaining[supply_key] -= qty
            for pool in pools:
                pool_remaining[pool] -= qty
    unplaced = [
        {"from": supply.site_id, "source_ref": supply.source_record_id, "category": supply.category,
         "quantity": remaining[record_key(supply)], "unit": supply.unit, "needs_human_review": True}
        for supply in supplies if remaining[record_key(supply)]
    ]
    return {"recipient_proposals": proposals_by_kind["need"],
            "storage_proposals": proposals_by_kind["storage"],
            "commercial_proposals": proposals_by_kind["buyer"], "unplaced": unplaced}
