# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Tests for Append-Only Audit Log

Test coverage:
- Audit log initialization
- Entry appending
- Hash chain integrity
- Consent token integration
- Tamper detection
- Entry retrieval
"""

import sys
import os
import unittest
import tempfile
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from sovereign.audit_log import AppendOnlyAuditLog, AuditLogEntry
from sovereign.consent_token import ConsentTokenManager


class TestAuditLogEntry(unittest.TestCase):
    """Test cases for AuditLogEntry."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_key = b"test_key_for_audit_log_tests_1234"
        self.manager = ConsentTokenManager(self.test_key)
        self.token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True,
            user_id="test_user"
        )
    
    def test_entry_creation(self):
        """Test creating an audit log entry."""
        entry = AuditLogEntry(
            entry_id=1,
            timestamp="2025-11-12T00:00:00+00:00",
            operation="test_op",
            data={"key": "value"},
            consent_token=self.token,
            previous_hash="0" * 64
        )
        
        self.assertEqual(entry.entry_id, 1)
        self.assertEqual(entry.operation, "test_op")
        self.assertIsNotNone(entry.entry_hash)
    
    def test_entry_hash_computation(self):
        """Test that entry hash is computed correctly."""
        entry = AuditLogEntry(
            entry_id=1,
            timestamp="2025-11-12T00:00:00+00:00",
            operation="test_op",
            data={"key": "value"},
            consent_token=self.token,
            previous_hash="0" * 64
        )
        
        # Hash should be 64 hex characters
        self.assertEqual(len(entry.entry_hash), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in entry.entry_hash))
    
    def test_entry_to_dict(self):
        """Test converting entry to dictionary."""
        entry = AuditLogEntry(
            entry_id=1,
            timestamp="2025-11-12T00:00:00+00:00",
            operation="test_op",
            data={"key": "value"},
            consent_token=self.token,
            previous_hash="0" * 64
        )
        
        entry_dict = entry.to_dict()
        
        self.assertIsInstance(entry_dict, dict)
        self.assertEqual(entry_dict["entry_id"], 1)
        self.assertIn("consent_token", entry_dict)
    
    def test_entry_to_json(self):
        """Test serializing entry to JSON."""
        entry = AuditLogEntry(
            entry_id=1,
            timestamp="2025-11-12T00:00:00+00:00",
            operation="test_op",
            data={"key": "value"},
            consent_token=self.token,
            previous_hash="0" * 64
        )
        
        json_str = entry.to_json()
        
        self.assertIsInstance(json_str, str)
        # Should be valid JSON
        parsed = json.loads(json_str)
        self.assertEqual(parsed["entry_id"], 1)
    
    def test_entry_from_dict(self):
        """Test creating entry from dictionary."""
        entry = AuditLogEntry(
            entry_id=1,
            timestamp="2025-11-12T00:00:00+00:00",
            operation="test_op",
            data={"key": "value"},
            consent_token=self.token,
            previous_hash="0" * 64
        )
        
        entry_dict = entry.to_dict()
        restored_entry = AuditLogEntry.from_dict(entry_dict)
        
        self.assertEqual(restored_entry.entry_id, entry.entry_id)
        self.assertEqual(restored_entry.entry_hash, entry.entry_hash)


class TestAppendOnlyAuditLog(unittest.TestCase):
    """Test cases for AppendOnlyAuditLog."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_key = b"test_key_for_audit_log_tests_1234"
        self.manager = ConsentTokenManager(self.test_key)
        
        # Create temporary log file
        self.temp_dir = tempfile.mkdtemp()
        self.log_path = os.path.join(self.temp_dir, "test_audit.jsonl")
        self.log = AppendOnlyAuditLog(self.log_path, self.manager)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_log_initialization(self):
        """Test audit log initialization."""
        self.assertTrue(os.path.exists(self.log_path))
        self.assertEqual(self.log.get_entry_count(), 1)  # Genesis entry
    
    def test_genesis_entry(self):
        """Test that genesis entry is created."""
        entries = self.log.read_all()
        
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].operation, "genesis")
        self.assertEqual(entries[0].entry_id, 0)
    
    def test_append_entry(self):
        """Test appending an entry."""
        token = self.manager.issue_token(
            operation="test_append",
            ethics_verified=True,
            human_approval=True
        )
        
        entry = self.log.append(
            operation="test_append",
            data={"test": "data"},
            consent_token=token
        )
        
        self.assertEqual(entry.operation, "test_append")
        self.assertEqual(entry.entry_id, 1)
    
    def test_multiple_appends(self):
        """Test appending multiple entries."""
        for i in range(5):
            token = self.manager.issue_token(
                operation=f"test_op_{i}",
                ethics_verified=True,
                human_approval=True
            )
            
            self.log.append(
                operation=f"test_op_{i}",
                data={"index": i},
                consent_token=token
            )
        
        self.assertEqual(self.log.get_entry_count(), 6)  # 1 genesis + 5 appends
    
    def test_read_all_entries(self):
        """Test reading all entries."""
        # Append some entries
        for i in range(3):
            token = self.manager.issue_token(
                operation=f"test_op_{i}",
                ethics_verified=True,
                human_approval=True
            )
            self.log.append(f"test_op_{i}", {"index": i}, token)
        
        entries = self.log.read_all()
        
        self.assertEqual(len(entries), 4)  # Genesis + 3
        self.assertEqual(entries[0].operation, "genesis")
        self.assertEqual(entries[3].operation, "test_op_2")
    
    def test_read_stream(self):
        """Test streaming entries."""
        # Append some entries
        for i in range(3):
            token = self.manager.issue_token(
                operation=f"test_op_{i}",
                ethics_verified=True,
                human_approval=True
            )
            self.log.append(f"test_op_{i}", {"index": i}, token)
        
        # Stream entries
        entries = list(self.log.read_stream())
        
        self.assertEqual(len(entries), 4)
        self.assertEqual(entries[1].operation, "test_op_0")
    
    def test_hash_chain_linkage(self):
        """Test that hash chain links entries correctly."""
        # Append entries
        for i in range(3):
            token = self.manager.issue_token(
                operation=f"test_op_{i}",
                ethics_verified=True,
                human_approval=True
            )
            self.log.append(f"test_op_{i}", {"index": i}, token)
        
        entries = self.log.read_all()
        
        # Check chain linkage
        for i in range(1, len(entries)):
            self.assertEqual(
                entries[i].previous_hash,
                entries[i-1].entry_hash,
                f"Chain broken between entry {i-1} and {i}"
            )
    
    def test_verify_integrity_valid(self):
        """Test integrity verification of valid log."""
        # Append entries
        for i in range(3):
            token = self.manager.issue_token(
                operation=f"test_op_{i}",
                ethics_verified=True,
                human_approval=True
            )
            self.log.append(f"test_op_{i}", {"index": i}, token)
        
        is_valid, error = self.log.verify_integrity()
        
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_verify_integrity_tampered(self):
        """Test integrity verification detects tampering."""
        # Append entries
        for i in range(3):
            token = self.manager.issue_token(
                operation=f"test_op_{i}",
                ethics_verified=True,
                human_approval=True
            )
            self.log.append(f"test_op_{i}", {"index": i}, token)
        
        # Tamper with the log file
        with open(self.log_path, 'r') as f:
            lines = f.readlines()
        
        if len(lines) > 1:
            # Modify the second entry
            entry_dict = json.loads(lines[1])
            entry_dict['data']['tampered'] = True
            lines[1] = json.dumps(entry_dict) + '\n'
            
            with open(self.log_path, 'w') as f:
                f.writelines(lines)
            
            # Reload and verify
            log2 = AppendOnlyAuditLog(self.log_path, self.manager)
            is_valid, error = log2.verify_integrity()
            
            self.assertFalse(is_valid)
            self.assertIsNotNone(error)
    
    def test_get_entries_by_operation(self):
        """Test filtering entries by operation."""
        # Append mixed operations
        for i in range(5):
            op = "op_a" if i % 2 == 0 else "op_b"
            token = self.manager.issue_token(
                operation=op,
                ethics_verified=True,
                human_approval=True
            )
            self.log.append(op, {"index": i}, token)
        
        op_a_entries = self.log.get_entries_by_operation("op_a")
        op_b_entries = self.log.get_entries_by_operation("op_b")
        
        self.assertEqual(len(op_a_entries), 3)  # indices 0, 2, 4
        self.assertEqual(len(op_b_entries), 2)  # indices 1, 3
    
    def test_persistence(self):
        """Test that entries persist across log instances."""
        # Append entries
        for i in range(3):
            token = self.manager.issue_token(
                operation=f"test_op_{i}",
                ethics_verified=True,
                human_approval=True
            )
            self.log.append(f"test_op_{i}", {"index": i}, token)
        
        # Create new log instance with same path
        log2 = AppendOnlyAuditLog(self.log_path, self.manager)
        
        # Should load existing entries
        self.assertEqual(log2.get_entry_count(), 4)
        
        entries = log2.read_all()
        self.assertEqual(entries[1].operation, "test_op_0")
    
    def test_entry_id_sequence(self):
        """Test that entry IDs are sequential."""
        for i in range(5):
            token = self.manager.issue_token(
                operation=f"test_op_{i}",
                ethics_verified=True,
                human_approval=True
            )
            self.log.append(f"test_op_{i}", {"index": i}, token)
        
        entries = self.log.read_all()
        
        for i, entry in enumerate(entries):
            self.assertEqual(entry.entry_id, i)


class TestAuditLogConsentTokenIntegration(unittest.TestCase):
    """Test integration between audit log and consent tokens."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_key = b"test_key_for_integration_tests_12"
        self.manager = ConsentTokenManager(self.test_key)
        
        self.temp_dir = tempfile.mkdtemp()
        self.log_path = os.path.join(self.temp_dir, "test_audit.jsonl")
        self.log = AppendOnlyAuditLog(self.log_path, self.manager)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_consent_token_attached_to_entry(self):
        """Test that consent tokens are attached to entries."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True,
            user_id="test_user"
        )
        
        entry = self.log.append("test_op", {"data": "value"}, token)
        
        self.assertIsNotNone(entry.consent_token)
        self.assertEqual(entry.consent_token.operation, "test_op")
        self.assertEqual(entry.consent_token.user_id, "test_user")
    
    def test_consent_token_validation_after_read(self):
        """Test that consent tokens remain valid after reading from log."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True
        )
        
        self.log.append("test_op", {"data": "value"}, token)
        
        # Read back and validate
        entries = self.log.read_all()
        for entry in entries[1:]:  # Skip genesis (different key in test)
            is_valid = self.manager.validate_token(entry.consent_token)
            self.assertTrue(is_valid, f"Token invalid for entry {entry.entry_id}")
    
    def test_consent_token_serialization_in_log(self):
        """Test that consent tokens are properly serialized in JSONL."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval="approved_by_admin"
        )
        
        self.log.append("test_op", {"data": "value"}, token)
        
        # Read raw JSONL
        with open(self.log_path, 'r') as f:
            lines = f.readlines()
        
        # Parse last entry
        entry_dict = json.loads(lines[-1])
        
        self.assertIn("consent_token", entry_dict)
        self.assertEqual(entry_dict["consent_token"]["operation"], "test_op")
        self.assertEqual(entry_dict["consent_token"]["human_approval"], "approved_by_admin")


if __name__ == "__main__":
    unittest.main()
