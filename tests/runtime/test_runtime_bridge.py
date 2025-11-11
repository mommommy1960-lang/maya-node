# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Tests for Runtime Bridge Integration
"""

import unittest
from src.sovereign.runtime_bridge import RuntimeBridge, BridgeConfig
from src.sovereign.runtime import RuntimeConfig
from src.sovereign.consent_tokens import ConsentScope


class TestRuntimeBridge(unittest.TestCase):
    """Test cases for runtime bridge"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.bridge = RuntimeBridge(
            runtime_config=RuntimeConfig(
                enable_ethics_checks=True,
                require_human_approval=False,
                audit_logging=True
            ),
            bridge_config=BridgeConfig(
                require_consent=True,
                require_attestation=False,
                ledger_enabled=True
            )
        )
    
    def test_initialization(self):
        """Test bridge initialization"""
        self.assertIsNotNone(self.bridge)
        self.assertIsNotNone(self.bridge.runtime)
        self.assertIsNotNone(self.bridge.ledger)
        self.assertIsNotNone(self.bridge.consent_manager)
    
    def test_consent_request(self):
        """Test consent token request"""
        token = self.bridge.request_consent(
            user_id="user123",
            operation="test_operation",
            scope=ConsentScope.SINGLE_OPERATION
        )
        
        self.assertIsNotNone(token)
        self.assertEqual(token.user_id, "user123")
        self.assertEqual(token.operation, "test_operation")
    
    def test_execute_with_valid_consent(self):
        """Test execution with valid consent token"""
        # Request consent
        token = self.bridge.request_consent(
            user_id="user123",
            operation="process_data"
        )
        
        # Execute with consent
        result = self.bridge.execute_with_consent(
            user_id="user123",
            operation="process_data",
            input_data={"test": "data"},
            consent_token=token
        )
        
        self.assertIsNotNone(result)
        self.assertIn("bridge_metadata", result)
        self.assertTrue(result["bridge_metadata"]["consent_verified"])
    
    def test_execute_without_consent_fails(self):
        """Test execution fails without consent token"""
        with self.assertRaises(RuntimeError) as context:
            self.bridge.execute_with_consent(
                user_id="user123",
                operation="process_data",
                input_data={"test": "data"},
                consent_token=None
            )
        
        self.assertIn("Consent token required", str(context.exception))
    
    def test_execute_with_mismatched_operation_fails(self):
        """Test execution fails with mismatched operation"""
        # Request consent for one operation
        token = self.bridge.request_consent(
            user_id="user123",
            operation="operation_a"
        )
        
        # Try to use for different operation
        with self.assertRaises(RuntimeError) as context:
            self.bridge.execute_with_consent(
                user_id="user123",
                operation="operation_b",
                input_data={"test": "data"},
                consent_token=token
            )
        
        self.assertIn("operation mismatch", str(context.exception))
    
    def test_ledger_integration(self):
        """Test operations are logged to ledger"""
        initial_entries = len(self.bridge.ledger.entries)
        
        # Execute operation
        token = self.bridge.request_consent(
            user_id="user123",
            operation="test_op"
        )
        
        self.bridge.execute_with_consent(
            user_id="user123",
            operation="test_op",
            input_data={"test": "data"},
            consent_token=token
        )
        
        # Check ledger has new entries
        final_entries = len(self.bridge.ledger.entries)
        self.assertGreater(final_entries, initial_entries)
        
        # Verify ledger integrity
        self.assertTrue(self.bridge.ledger.verify_integrity())
    
    def test_get_audit_trail(self):
        """Test getting audit trail"""
        # Execute some operations
        token1 = self.bridge.request_consent("user123", "op1")
        self.bridge.execute_with_consent(
            "user123", "op1", {"test": "1"}, token1
        )
        
        token2 = self.bridge.request_consent("user123", "op2")
        self.bridge.execute_with_consent(
            "user123", "op2", {"test": "2"}, token2
        )
        
        # Get audit trail
        trail = self.bridge.get_audit_trail()
        self.assertIsInstance(trail, list)
        self.assertGreater(len(trail), 0)
    
    def test_get_runtime_status(self):
        """Test getting runtime status"""
        status = self.bridge.get_runtime_status()
        
        self.assertIsInstance(status, dict)
        self.assertIn("runtime_state", status)
        self.assertIn("ledger_enabled", status)
        self.assertIn("consent_required", status)
        self.assertIn("ledger_integrity", status)
        
        self.assertTrue(status["ledger_integrity"])
    
    def test_generate_attestation_report(self):
        """Test generating attestation report"""
        report = self.bridge.generate_attestation_report()
        
        self.assertIsInstance(report, dict)
        self.assertIn("timestamp", report)
        self.assertIn("runtime_status", report)
        self.assertIn("ledger_verification", report)


class TestBridgeWithoutConsent(unittest.TestCase):
    """Test bridge operation without consent requirement"""
    
    def setUp(self):
        """Set up bridge without consent requirement"""
        self.bridge = RuntimeBridge(
            bridge_config=BridgeConfig(
                require_consent=False,
                ledger_enabled=True
            )
        )
    
    def test_execute_without_consent_enabled(self):
        """Test execution when consent not required"""
        # Should work without consent token
        result = self.bridge.execute_with_consent(
            user_id="user123",
            operation="test_op",
            input_data={"test": "data"},
            consent_token=None
        )
        
        self.assertIsNotNone(result)
        self.assertFalse(result["bridge_metadata"]["consent_verified"])


class TestBridgeWithAttestation(unittest.TestCase):
    """Test bridge with attestation requirement"""
    
    def setUp(self):
        """Set up bridge with attestation"""
        self.bridge = RuntimeBridge(
            bridge_config=BridgeConfig(
                require_consent=False,
                require_attestation=True,
                ledger_enabled=True
            )
        )
    
    def test_attestation_checked(self):
        """Test that attestation is checked when required"""
        result = self.bridge.execute_with_consent(
            user_id="user123",
            operation="test_op",
            input_data={"test": "data"},
            consent_token=None
        )
        
        self.assertIsNotNone(result)
        self.assertTrue(result["bridge_metadata"]["attestation_verified"])


if __name__ == '__main__':
    unittest.main()
