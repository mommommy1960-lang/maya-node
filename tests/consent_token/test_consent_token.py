# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Tests for Consent Token System

Test coverage:
- Token generation
- Token validation
- Signature verification
- Serialization/deserialization
- Key management
- Tamper detection
"""

import sys
import os
import unittest
import time
from datetime import datetime, timezone

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from sovereign.consent_token import (
    ConsentToken,
    ConsentTokenManager,
    generate_trust_root_key
)


class TestConsentToken(unittest.TestCase):
    """Test cases for ConsentToken dataclass."""
    
    def test_token_creation(self):
        """Test creating a consent token."""
        token = ConsentToken(
            operation="test_op",
            ethics_verified=True,
            human_approval=True,
            timestamp="2025-11-12T00:00:00+00:00",
            user_id="test_user",
            signature="abc123"
        )
        
        self.assertEqual(token.operation, "test_op")
        self.assertTrue(token.ethics_verified)
        self.assertTrue(token.human_approval)
        self.assertEqual(token.user_id, "test_user")
        self.assertEqual(token.signature, "abc123")
    
    def test_token_to_dict(self):
        """Test converting token to dictionary."""
        token = ConsentToken(
            operation="test_op",
            ethics_verified=True,
            human_approval=False,
            timestamp="2025-11-12T00:00:00+00:00",
            user_id="test_user",
            signature="abc123"
        )
        
        token_dict = token.to_dict()
        
        self.assertIsInstance(token_dict, dict)
        self.assertEqual(token_dict["operation"], "test_op")
        self.assertTrue(token_dict["ethics_verified"])
        self.assertFalse(token_dict["human_approval"])
    
    def test_token_to_json(self):
        """Test serializing token to JSON."""
        token = ConsentToken(
            operation="test_op",
            ethics_verified=True,
            human_approval=True,
            timestamp="2025-11-12T00:00:00+00:00",
            user_id="test_user",
            signature="abc123"
        )
        
        json_str = token.to_json()
        
        self.assertIsInstance(json_str, str)
        self.assertIn("test_op", json_str)
        self.assertIn("abc123", json_str)
    
    def test_token_from_dict(self):
        """Test creating token from dictionary."""
        token_dict = {
            "operation": "test_op",
            "ethics_verified": True,
            "human_approval": True,
            "timestamp": "2025-11-12T00:00:00+00:00",
            "user_id": "test_user",
            "signature": "abc123"
        }
        
        token = ConsentToken.from_dict(token_dict)
        
        self.assertEqual(token.operation, "test_op")
        self.assertTrue(token.ethics_verified)
    
    def test_token_from_json(self):
        """Test deserializing token from JSON."""
        json_str = '{"operation": "test_op", "ethics_verified": true, "human_approval": true, "timestamp": "2025-11-12T00:00:00+00:00", "user_id": "test_user", "signature": "abc123"}'
        
        token = ConsentToken.from_json(json_str)
        
        self.assertEqual(token.operation, "test_op")
        self.assertTrue(token.ethics_verified)
    
    def test_token_default_user_id(self):
        """Test default user_id value."""
        token = ConsentToken(
            operation="test_op",
            ethics_verified=True,
            human_approval=True,
            timestamp="2025-11-12T00:00:00+00:00",
            signature="abc123"
        )
        
        self.assertEqual(token.user_id, "system_placeholder")


class TestConsentTokenManager(unittest.TestCase):
    """Test cases for ConsentTokenManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_key = b"test_key_for_unit_testing_only_123456"
        self.manager = ConsentTokenManager(self.test_key)
    
    def test_manager_initialization(self):
        """Test manager initialization."""
        manager = ConsentTokenManager(self.test_key)
        self.assertIsNotNone(manager.trust_root_key)
    
    def test_issue_token(self):
        """Test issuing a consent token."""
        token = self.manager.issue_token(
            operation="test_operation",
            ethics_verified=True,
            human_approval=True,
            user_id="test_user"
        )
        
        self.assertEqual(token.operation, "test_operation")
        self.assertTrue(token.ethics_verified)
        self.assertTrue(token.human_approval)
        self.assertEqual(token.user_id, "test_user")
        self.assertIsNotNone(token.signature)
        self.assertGreater(len(token.signature), 0)
    
    def test_issue_token_timestamp(self):
        """Test that issued token has valid timestamp."""
        before = datetime.now(timezone.utc)
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True
        )
        after = datetime.now(timezone.utc)
        
        token_time = datetime.fromisoformat(token.timestamp)
        
        self.assertGreaterEqual(token_time, before)
        self.assertLessEqual(token_time, after)
    
    def test_validate_token_valid(self):
        """Test validating a valid token."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True
        )
        
        is_valid = self.manager.validate_token(token)
        self.assertTrue(is_valid)
    
    def test_validate_token_tampered_operation(self):
        """Test detecting tampered operation field."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True
        )
        
        # Tamper with operation
        token.operation = "tampered_operation"
        
        is_valid = self.manager.validate_token(token)
        self.assertFalse(is_valid)
    
    def test_validate_token_tampered_ethics(self):
        """Test detecting tampered ethics_verified field."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True
        )
        
        # Tamper with ethics_verified
        token.ethics_verified = False
        
        is_valid = self.manager.validate_token(token)
        self.assertFalse(is_valid)
    
    def test_validate_token_tampered_approval(self):
        """Test detecting tampered human_approval field."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True
        )
        
        # Tamper with human_approval
        token.human_approval = False
        
        is_valid = self.manager.validate_token(token)
        self.assertFalse(is_valid)
    
    def test_validate_token_tampered_timestamp(self):
        """Test detecting tampered timestamp field."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True
        )
        
        # Tamper with timestamp
        token.timestamp = "2020-01-01T00:00:00+00:00"
        
        is_valid = self.manager.validate_token(token)
        self.assertFalse(is_valid)
    
    def test_validate_token_tampered_user_id(self):
        """Test detecting tampered user_id field."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True,
            user_id="original_user"
        )
        
        # Tamper with user_id
        token.user_id = "attacker_user"
        
        is_valid = self.manager.validate_token(token)
        self.assertFalse(is_valid)
    
    def test_validate_token_wrong_key(self):
        """Test that tokens from different keys are invalid."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True
        )
        
        # Try to validate with different key
        different_manager = ConsentTokenManager(b"different_key_12345")
        is_valid = different_manager.validate_token(token)
        
        self.assertFalse(is_valid)
    
    def test_validate_token_dict(self):
        """Test validating token from dictionary."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True
        )
        
        token_dict = token.to_dict()
        is_valid = self.manager.validate_token_dict(token_dict)
        
        self.assertTrue(is_valid)
    
    def test_validate_token_dict_invalid(self):
        """Test validating invalid token dictionary."""
        token_dict = {
            "operation": "test_op",
            "ethics_verified": True,
            "human_approval": True,
            "timestamp": "2025-11-12T00:00:00+00:00",
            "user_id": "test_user",
            "signature": "invalid_signature_abc123"
        }
        
        is_valid = self.manager.validate_token_dict(token_dict)
        self.assertFalse(is_valid)
    
    def test_get_truncated_signature(self):
        """Test getting truncated signature."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True
        )
        
        truncated = self.manager.get_truncated_signature(token, length=12)
        
        self.assertEqual(len(truncated), 15)  # 12 + "..."
        self.assertTrue(truncated.endswith("..."))
    
    def test_token_roundtrip_serialization(self):
        """Test complete roundtrip: issue -> serialize -> deserialize -> validate."""
        # Issue token
        original_token = self.manager.issue_token(
            operation="roundtrip_test",
            ethics_verified=True,
            human_approval="approved",
            user_id="test_user"
        )
        
        # Serialize to JSON
        json_str = original_token.to_json()
        
        # Deserialize from JSON
        restored_token = ConsentToken.from_json(json_str)
        
        # Validate
        is_valid = self.manager.validate_token(restored_token)
        
        self.assertTrue(is_valid)
        self.assertEqual(restored_token.operation, "roundtrip_test")
        self.assertEqual(restored_token.user_id, "test_user")


class TestGenerateTrustRootKey(unittest.TestCase):
    """Test cases for trust root key generation."""
    
    def test_generate_key(self):
        """Test generating a trust root key."""
        key = generate_trust_root_key()
        
        self.assertIsInstance(key, bytes)
        self.assertEqual(len(key), 32)
    
    def test_generate_key_randomness(self):
        """Test that generated keys are random."""
        key1 = generate_trust_root_key()
        key2 = generate_trust_root_key()
        
        self.assertNotEqual(key1, key2)
    
    def test_generated_key_works_with_manager(self):
        """Test that generated key works with ConsentTokenManager."""
        key = generate_trust_root_key()
        manager = ConsentTokenManager(key)
        
        token = manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True
        )
        
        is_valid = manager.validate_token(token)
        self.assertTrue(is_valid)


class TestConsentTokenEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_key = b"test_key_edge_cases_12345678901234"
        self.manager = ConsentTokenManager(self.test_key)
    
    def test_human_approval_none(self):
        """Test token with human_approval=None."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=None
        )
        
        self.assertIsNone(token.human_approval)
        self.assertTrue(self.manager.validate_token(token))
    
    def test_human_approval_string(self):
        """Test token with human_approval as string."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval="approved_by_admin"
        )
        
        self.assertEqual(token.human_approval, "approved_by_admin")
        self.assertTrue(self.manager.validate_token(token))
    
    def test_ethics_verified_false(self):
        """Test token with ethics_verified=False."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=False,
            human_approval=True
        )
        
        self.assertFalse(token.ethics_verified)
        self.assertTrue(self.manager.validate_token(token))
    
    def test_operation_with_special_characters(self):
        """Test operation names with special characters."""
        token = self.manager.issue_token(
            operation="test_op_with-special.chars_123",
            ethics_verified=True,
            human_approval=True
        )
        
        self.assertTrue(self.manager.validate_token(token))
    
    def test_user_id_with_special_characters(self):
        """Test user IDs with special characters."""
        token = self.manager.issue_token(
            operation="test_op",
            ethics_verified=True,
            human_approval=True,
            user_id="user@example.com"
        )
        
        self.assertEqual(token.user_id, "user@example.com")
        self.assertTrue(self.manager.validate_token(token))


if __name__ == "__main__":
    unittest.main()
