# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
"""Hash-chained audit ledger with structural integrity verification."""
import copy
import hashlib
import json
import logging
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LedgerEntry:
    index: int
    timestamp: float
    operation: str
    data: Dict[str, Any]
    previous_hash: str
    entry_hash: str

class ImmutableLedger:
    def __init__(self):
        self.entries: List[LedgerEntry] = []
        # A separately maintained trusted head prevents an attacker who can
        # rewrite the final entry from simply recomputing its public hash and
        # presenting the forged tail as valid. In a persistent deployment this
        # anchor should itself live in protected/independent storage.
        self._trusted_head_hash: str = ""
        self._add_genesis_entry()

    def _add_genesis_entry(self) -> None:
        genesis = LedgerEntry(0, time.time(), "genesis", {"note": "Ledger initialized"}, "0" * 64, "")
        genesis.entry_hash = self._compute_hash(genesis)
        self.entries.append(genesis)
        self._trusted_head_hash = genesis.entry_hash

    def _compute_hash(self, entry: LedgerEntry) -> str:
        # Canonical JSON prevents representation-dependent dictionary hashing.
        data = json.dumps(entry.data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        content = f"{entry.index}:{entry.timestamp}:{entry.operation}:{data}:{entry.previous_hash}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def append(self, operation: str, data: Dict[str, Any]) -> LedgerEntry:
        previous = self.entries[-1]
        # Snapshot caller-owned data so later mutation of the input object does
        # not silently rewrite historical ledger state.
        entry = LedgerEntry(len(self.entries), time.time(), operation, copy.deepcopy(data),
                            previous.entry_hash, "")
        entry.entry_hash = self._compute_hash(entry)
        self.entries.append(entry)
        self._trusted_head_hash = entry.entry_hash
        return entry

    def verify_integrity(self) -> bool:
        # Structural anchor: deleting/replacing genesis must never turn the next
        # internally valid entry into a new trusted root.
        if not self.entries:
            return False
        genesis = self.entries[0]
        if (genesis.index != 0 or genesis.operation != "genesis" or
                genesis.previous_hash != "0" * 64 or
                genesis.data != {"note": "Ledger initialized"}):
            return False
        for i, entry in enumerate(self.entries):
            if entry.index != i:
                return False
            if entry.entry_hash != self._compute_hash(entry):
                return False
            if i > 0 and entry.previous_hash != self.entries[i - 1].entry_hash:
                return False
        # Hash chaining alone cannot detect a forged final entry if the attacker
        # can recompute that entry's hash. Compare the public chain tip against
        # the independently maintained trusted head as the final trust anchor.
        if self.entries[-1].entry_hash != self._trusted_head_hash:
            return False
        return True

    def get_entries(self, operation: Optional[str] = None) -> List[LedgerEntry]:
        if operation:
            return [e for e in self.entries if e.operation == operation]
        return self.entries.copy()
