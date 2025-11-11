# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Immutable Ledger

Implements an immutable audit ledger for tracking operations and decisions.
"""

import logging
import hashlib
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LedgerEntry:
    """Single ledger entry"""
    index: int
    timestamp: float
    operation: str
    data: Dict[str, Any]
    previous_hash: str
    entry_hash: str


class ImmutableLedger:
    """
    Immutable audit ledger.
    
    Provides tamper-proof record-keeping with:
    - Sequential entries
    - Hash chain linking
    - Integrity verification
    """
    
    def __init__(self):
        """Initialize ledger."""
        self.entries: List[LedgerEntry] = []
        self._add_genesis_entry()
        logger.info("Immutable Ledger initialized")
    
    def _add_genesis_entry(self) -> None:
        """Add genesis (first) entry."""
        genesis = LedgerEntry(
            index=0,
            timestamp=time.time(),
            operation="genesis",
            data={"note": "Ledger initialized"},
            previous_hash="0" * 64,
            entry_hash=""
        )
        genesis.entry_hash = self._compute_hash(genesis)
        self.entries.append(genesis)
    
    def _compute_hash(self, entry: LedgerEntry) -> str:
        """Compute hash for an entry."""
        content = (
            f"{entry.index}:{entry.timestamp}:"
            f"{entry.operation}:{entry.data}:"
            f"{entry.previous_hash}"
        )
        return hashlib.sha256(content.encode()).hexdigest()
    
    def append(self, operation: str, data: Dict[str, Any]) -> LedgerEntry:
        """
        Append entry to ledger.
        
        Args:
            operation: Operation type
            data: Operation data
            
        Returns:
            Created ledger entry
        """
        previous = self.entries[-1]
        
        entry = LedgerEntry(
            index=len(self.entries),
            timestamp=time.time(),
            operation=operation,
            data=data,
            previous_hash=previous.entry_hash,
            entry_hash=""
        )
        entry.entry_hash = self._compute_hash(entry)
        
        self.entries.append(entry)
        logger.info(f"Ledger entry added: {operation} (index {entry.index})")
        
        return entry
    
    def verify_integrity(self) -> bool:
        """
        Verify integrity of entire ledger.
        
        Returns:
            True if ledger is intact
        """
        for i, entry in enumerate(self.entries):
            # Verify hash
            expected_hash = self._compute_hash(entry)
            if entry.entry_hash != expected_hash:
                logger.error(f"Hash mismatch at index {i}")
                return False
            
            # Verify chain linkage
            if i > 0:
                previous = self.entries[i - 1]
                if entry.previous_hash != previous.entry_hash:
                    logger.error(f"Chain broken at index {i}")
                    return False
        
        logger.info("Ledger integrity verified")
        return True
    
    def get_entries(self, operation: Optional[str] = None) -> List[LedgerEntry]:
        """
        Get ledger entries, optionally filtered by operation.
        
        Args:
            operation: Filter by operation type
            
        Returns:
            List of matching entries
        """
        if operation:
            return [e for e in self.entries if e.operation == operation]
        return self.entries.copy()


if __name__ == "__main__":
    ledger = ImmutableLedger()
    
    # Add some entries
    ledger.append("test_operation", {"value": 42})
    ledger.append("another_operation", {"status": "ok"})
    
    # Verify integrity
    print(f"Integrity: {ledger.verify_integrity()}")
    print(f"Total entries: {len(ledger.entries)}")
