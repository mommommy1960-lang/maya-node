# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors

"""Tests for Runtime Bridge Integration."""

import unittest
from src.sovereign.runtime_bridge import RuntimeBridge, BridgeConfig
from src.sovereign.runtime import RuntimeConfig
from src.sovereign.consent_tokens import ConsentScope


class TestRuntimeBridge(unittest.TestCase):
    def setUp(self):
        self.bridge = RuntimeBridge(
            runtime_config=RuntimeConfig(enable_ethics_checks=True, require_human_approval=False, audit_logging=True),
            bridge_config=BridgeConfig(require_consent=True, require_attestation=False, ledger_enabled=True)
        )

    def test_initialization(self):
        self.assertIsNotNone(self.bridge.runtime); self.assertIsNotNone(self.bridge.ledger); self.assertIsNotNone(self.bridge.consent_manager)

    def test_consent_request(self):
        token = self.bridge.request_consent("user123", "test_operation", ConsentScope.SINGLE_OPERATION)
        self.assertEqual(token.user_id, "user123"); self.assertEqual(token.operation, "test_operation")

    def test_execute_with_valid_consent(self):
        token = self.bridge.request_consent("user123", "process_data")
        result = self.bridge.execute_with_consent("user123", "process_data", {"test": "data"}, token)
        self.assertTrue(result["bridge_metadata"]["consent_verified"])

    def test_execute_without_consent_fails(self):
        with self.assertRaisesRegex(RuntimeError, "Consent token required"):
            self.bridge.execute_with_consent("user123", "process_data", {"test": "data"}, None)

    def test_execute_with_mismatched_operation_fails(self):
        token = self.bridge.request_consent("user123", "operation_a")
        with self.assertRaisesRegex(RuntimeError, "operation mismatch"):
            self.bridge.execute_with_consent("user123", "operation_b", {"test": "data"}, token)

    def test_ledger_integration(self):
        initial = len(self.bridge.ledger.entries)
        token = self.bridge.request_consent("user123", "test_op")
        self.bridge.execute_with_consent("user123", "test_op", {"test": "data"}, token)
        self.assertGreater(len(self.bridge.ledger.entries), initial)
        self.assertTrue(self.bridge.ledger.verify_integrity())

    def test_get_audit_trail(self):
        for op in ("op1", "op2"):
            token = self.bridge.request_consent("user123", op)
            self.bridge.execute_with_consent("user123", op, {"test": op}, token)
        self.assertGreater(len(self.bridge.get_audit_trail()), 0)

    def test_get_runtime_status(self):
        status = self.bridge.get_runtime_status()
        self.assertIn("runtime_state", status); self.assertIn("ledger_enabled", status); self.assertIn("consent_required", status)
        self.assertTrue(status["ledger_integrity"])

    def test_generate_attestation_report(self):
        report = self.bridge.generate_attestation_report()
        self.assertIn("timestamp", report); self.assertIn("runtime_status", report); self.assertIn("ledger_verification", report)
        self.assertEqual(report["status"], "not_configured")


class TestBridgeWithoutConsent(unittest.TestCase):
    def setUp(self):
        self.bridge = RuntimeBridge(bridge_config=BridgeConfig(require_consent=False, ledger_enabled=True))

    def test_execute_without_consent_enabled(self):
        result = self.bridge.execute_with_consent("user123", "test_op", {"test": "data"}, None)
        self.assertFalse(result["bridge_metadata"]["consent_verified"])


class TestBridgeWithAttestation(unittest.TestCase):
    def setUp(self):
        self.bridge = RuntimeBridge(bridge_config=BridgeConfig(require_consent=False, require_attestation=True, ledger_enabled=True))

    def test_attestation_fails_closed_without_verified_platform(self):
        # Hosted CI has no trusted TPM. Requiring attestation must therefore deny execution,
        # not silently treat simulated/stub measurements as verified hardware evidence.
        with self.assertRaisesRegex(RuntimeError, "Platform attestation not verified"):
            self.bridge.execute_with_consent("user123", "test_op", {"test": "data"}, None)


if __name__ == '__main__':
    unittest.main()
