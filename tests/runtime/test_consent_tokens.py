# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Tests for Consent Token System
"""

import unittest
import time
from src.sovereign.consent_tokens import (
    ConsentTokenManager,
    ConsentToken,
    ConsentScope,
    ConsentStatus
)


class TestConsentTokens(unittest.TestCase):
    """Test cases for consent token system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = ConsentTokenManager(secret_key="test_secret_key")
    
    def test_token_generation(self):
        """Test basic token generation"""
        token = self.manager.generate_token(
            user_id="user123",
            operation="test_operation",
            scope=ConsentScope.SINGLE_OPERATION
        )
        
        self.assertIsNotNone(token)
        self.assertEqual(token.user_id, "user123")
        self.assertEqual(token.operation, "test_operation")
        self.assertEqual(token.scope, ConsentScope.SINGLE_OPERATION)
        self.assertEqual(token.status, ConsentStatus.ACTIVE)
        self.assertIsNotNone(token.signature)
    
    def test_token_verification(self):
        """Test token verification"""
        token = self.manager.generate_token(
            user_id="user123",
            operation="test_operation"
        )
        
        # Should verify successfully
        self.assertTrue(self.manager.verify_token(token))
    
    def test_token_signature_integrity(self):
        """Test that signature prevents tampering"""
        token = self.manager.generate_token(
            user_id="user123",
            operation="test_operation"
        )
        
        # Tamper with token
        token.user_id = "attacker"
        
        # Should fail verification
        self.assertFalse(self.manager.verify_token(token))
    
    def test_single_use_token(self):
        """Test single-use token consumption"""
        token = self.manager.generate_token(
            user_id="user123",
            operation="test_operation",
            scope=ConsentScope.SINGLE_OPERATION
        )
        
        # First use should succeed
        self.assertTrue(self.manager.use_token(token.token_id))
        
        # Second use should fail (token is consumed)
        self.assertFalse(self.manager.use_token(token.token_id))
    
    def test_session_token_reuse(self):
        """Test session tokens can be reused"""
        token = self.manager.generate_token(
            user_id="user123",
            operation="test_operation",
            scope=ConsentScope.SESSION
        )
        
        # Multiple uses should succeed
        self.assertTrue(self.manager.use_token(token.token_id))
        self.assertTrue(self.manager.use_token(token.token_id))
    
    def test_token_expiration(self):
        """Test token expiration"""
        token = self.manager.generate_token(
            user_id="user123",
            operation="test_operation",
            ttl_seconds=1  # Very short TTL
        )
        
        # Should verify initially
        self.assertTrue(self.manager.verify_token(token))
        
        # Wait for expiration
        time.sleep(1.5)
        
        # Should fail after expiration
        self.assertFalse(self.manager.verify_token(token))
    
    def test_token_revocation(self):
        """Test token revocation"""
        token = self.manager.generate_token(
            user_id="user123",
            operation="test_operation"
        )
        
        # Should verify initially
        self.assertTrue(self.manager.verify_token(token))
        
        # Revoke token
        self.assertTrue(self.manager.revoke_token(token.token_id))
        
        # Should fail after revocation
        self.assertFalse(self.manager.verify_token(token))
    
    def test_get_user_tokens(self):
        """Test getting tokens for a specific user"""
        user1_tokens = [
            self.manager.generate_token("user1", f"op{i}")
            for i in range(3)
        ]
        
        user2_token = self.manager.generate_token("user2", "op_user2")
        
        # Get user1 tokens
        tokens = self.manager.get_user_tokens("user1")
        self.assertEqual(len(tokens), 3)
        
        # Verify all are user1's tokens
        for token in tokens:
            self.assertEqual(token.user_id, "user1")
    
    def test_token_metadata(self):
        """Test token metadata storage"""
        metadata = {
            "reason": "testing",
            "priority": "high",
            "department": "engineering"
        }
        
        token = self.manager.generate_token(
            user_id="user123",
            operation="test_operation",
            metadata=metadata
        )
        
        self.assertEqual(token.metadata, metadata)
    
    def test_token_serialization(self):
        """Test token to/from dictionary conversion"""
        token = self.manager.generate_token(
            user_id="user123",
            operation="test_operation",
            metadata={"key": "value"}
        )
        
        # Convert to dict
        token_dict = token.to_dict()
        self.assertIsInstance(token_dict, dict)
        self.assertEqual(token_dict['user_id'], "user123")
        
        # Convert back
        restored_token = ConsentToken.from_dict(token_dict)
        self.assertEqual(restored_token.user_id, token.user_id)
        self.assertEqual(restored_token.operation, token.operation)
        self.assertEqual(restored_token.signature, token.signature)


class TestConsentScopes(unittest.TestCase):
    """Test cases for consent scope behavior"""
    
    def test_scope_types(self):
        """Test different consent scope types"""
        scopes = [
            ConsentScope.SINGLE_OPERATION,
            ConsentScope.SESSION,
            ConsentScope.BATCH
        ]
        
        for scope in scopes:
            self.assertIsInstance(scope, ConsentScope)
            self.assertIsInstance(scope.value, str)


if __name__ == '__main__':
    unittest.main()
