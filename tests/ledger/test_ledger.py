# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Tests for Ledger Integrity

Test coverage:
- Ledger initialization
- Entry appending
- Hash chain integrity
- Chain validation
- Tamper detection
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import unittest
from services.ledger.ledger import ImmutableLedger, LedgerEntry


class TestImmutableLedger(unittest.TestCase):
    """Test cases for ImmutableLedger."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ledger = ImmutableLedger()
    
    def test_initialization(self):
        """Test ledger initialization with genesis block."""
        self.assertEqual(len(self.ledger.entries), 1)
        
        genesis = self.ledger.entries[0]
        self.assertEqual(genesis.index, 0)
        self.assertEqual(genesis.operation, "genesis")
    
    def test_append_entry(self):
        """Test appending entries to ledger."""
        initial_count = len(self.ledger.entries)
        
        entry = self.ledger.append(
            "test_operation",
            {"key": "value"}
        )
        
        self.assertEqual(len(self.ledger.entries), initial_count + 1)
        self.assertEqual(entry.operation, "test_operation")
        self.assertEqual(entry.index, initial_count)
    
    def test_hash_chain_linkage(self):
        """Test that entries are properly linked."""
        self.ledger.append("op1", {"data": 1})
        self.ledger.append("op2", {"data": 2})
        
        # Check linkage
        for i in range(1, len(self.ledger.entries)):
            current = self.ledger.entries[i]
            previous = self.ledger.entries[i - 1]
            
            self.assertEqual(
                current.previous_hash,
                previous.entry_hash,
                f"Chain broken at index {i}"
            )
    
    def test_integrity_verification_success(self):
        """Test integrity verification on valid ledger."""
        self.ledger.append("op1", {"data": 1})
        self.ledger.append("op2", {"data": 2})
        
        self.assertTrue(self.ledger.verify_integrity())
    
    def test_integrity_verification_detects_tampering(self):
        """Test that tampering is detected."""
        self.ledger.append("op1", {"data": 1})
        self.ledger.append("op2", {"data": 2})
        
        # Verify integrity is good before tampering
        self.assertTrue(self.ledger.verify_integrity())
        
        # Tamper with an entry's data
        self.ledger.entries[1].data["tampered"] = True
        
        # Now integrity check should fail because the hash won't match
        # the tampered data
        self.assertFalse(self.ledger.verify_integrity())
    
    def test_get_entries_all(self):
        """Test retrieving all entries."""
        self.ledger.append("op1", {"data": 1})
        self.ledger.append("op2", {"data": 2})
        
        entries = self.ledger.get_entries()
        self.assertEqual(len(entries), 3)  # Including genesis
    
    def test_get_entries_filtered(self):
        """Test retrieving filtered entries."""
        self.ledger.append("op1", {"data": 1})
        self.ledger.append("op2", {"data": 2})
        self.ledger.append("op1", {"data": 3})
        
        op1_entries = self.ledger.get_entries(operation="op1")
        self.assertEqual(len(op1_entries), 2)
        
        for entry in op1_entries:
            self.assertEqual(entry.operation, "op1")
    
    def test_sequential_indices(self):
        """Test that indices are sequential."""
        for i in range(5):
            self.ledger.append(f"op{i}", {"index": i})
        
        for i, entry in enumerate(self.ledger.entries):
            self.assertEqual(entry.index, i)
    
    def test_hash_uniqueness(self):
        """Test that each entry has unique hash."""
        self.ledger.append("op1", {"data": 1})
        self.ledger.append("op2", {"data": 2})
        
        hashes = [entry.entry_hash for entry in self.ledger.entries]
        unique_hashes = set(hashes)
        
        self.assertEqual(len(hashes), len(unique_hashes))


class TestLedgerEntry(unittest.TestCase):
    """Test cases for LedgerEntry dataclass."""
    
    def test_entry_creation(self):
        """Test creating a ledger entry."""
        entry = LedgerEntry(
            index=1,
            timestamp=1234567890.0,
            operation="test",
            data={"key": "value"},
            previous_hash="abc123",
            entry_hash="def456"
        )
        
        self.assertEqual(entry.index, 1)
        self.assertEqual(entry.operation, "test")
        self.assertIn("key", entry.data)


if __name__ == "__main__":
    unittest.main()
