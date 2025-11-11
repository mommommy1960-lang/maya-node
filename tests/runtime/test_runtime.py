# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Tests for Sovereign Runtime

Test coverage:
- Runtime initialization
- Processing pipeline
- State management
- Error handling
- Audit logging
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import unittest
from sovereign.runtime import SovereignRuntime, RuntimeConfig, RuntimeState


class TestSovereignRuntime(unittest.TestCase):
    """Test cases for SovereignRuntime."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = RuntimeConfig(
            enable_ethics_checks=True,
            require_human_approval=False,  # For testing
            audit_logging=True
        )
        self.runtime = SovereignRuntime(self.config)
    
    def test_initialization(self):
        """Test runtime initialization."""
        self.assertEqual(self.runtime.state, RuntimeState.READY)
        self.assertEqual(self.runtime.iteration_count, 0)
        self.assertEqual(len(self.runtime.audit_log), 0)
    
    def test_process_simple_input(self):
        """Test processing simple input."""
        input_data = {"test": "data"}
        result = self.runtime.process(input_data)
        
        self.assertIn("status", result)
        self.assertEqual(result["status"], "processed")
        self.assertEqual(self.runtime.iteration_count, 1)
    
    def test_audit_logging(self):
        """Test audit trail creation."""
        input_data = {"test": "data"}
        self.runtime.process(input_data)
        
        audit_trail = self.runtime.get_audit_trail()
        self.assertGreater(len(audit_trail), 0)
        
        # Check for expected events
        events = [entry["event"] for entry in audit_trail]
        self.assertIn("process_start", events)
        self.assertIn("process_complete", events)
    
    def test_halt(self):
        """Test runtime halt."""
        self.runtime.halt()
        self.assertEqual(self.runtime.state, RuntimeState.HALTED)
        
        # Should not be able to process after halt
        with self.assertRaises(RuntimeError):
            self.runtime.process({"test": "data"})
    
    def test_ethics_verification_enabled(self):
        """Test that ethics checks run when enabled."""
        self.assertTrue(self.config.enable_ethics_checks)
        
        # Process with potentially flagged content
        input_data = {"content": "test"}
        result = self.runtime.process(input_data)
        
        self.assertTrue(result["ethics_verified"])


class TestRuntimeConfig(unittest.TestCase):
    """Test cases for RuntimeConfig."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = RuntimeConfig()
        
        self.assertTrue(config.enable_ethics_checks)
        self.assertTrue(config.require_human_approval)
        self.assertTrue(config.audit_logging)
        self.assertTrue(config.fail_safe_mode)


if __name__ == "__main__":
    unittest.main()
