# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Tests for Ethics Engine

Test coverage:
- Constraint verification
- Violation detection
- Prohibited pattern matching
- Ethics enforcement
- Transparency checks
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import unittest
from sovereign.ethics_engine import EthicsEngine, ViolationSeverity


class TestEthicsEngine(unittest.TestCase):
    """Test cases for EthicsEngine."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = EthicsEngine()
    
    def test_initialization(self):
        """Test ethics engine initialization."""
        self.assertIsNotNone(self.engine.prohibited_patterns)
        self.assertGreater(len(self.engine.constraints), 0)
    
    def test_clean_data_passes(self):
        """Test that clean data passes verification."""
        clean_data = {
            "operation": "optimize_energy",
            "context": "microgrid"
        }
        
        violations = self.engine.verify(clean_data)
        self.assertEqual(len(violations), 0)
    
    def test_weaponization_detection(self):
        """Test detection of weaponization patterns."""
        prohibited_data = {
            "operation": "weapon_targeting",
            "context": "missile guidance"
        }
        
        violations = self.engine.verify(prohibited_data)
        self.assertGreater(len(violations), 0)
        
        # Check that violations are related to weaponization
        violation_constraints = [v.constraint for v in violations]
        self.assertTrue(any("weapon" in c for c in violation_constraints))
    
    def test_surveillance_detection(self):
        """Test detection of surveillance patterns."""
        prohibited_data = {
            "operation": "track_individuals",
            "context": "surveillance system"
        }
        
        violations = self.engine.verify(prohibited_data)
        self.assertGreater(len(violations), 0)
    
    def test_harm_detection(self):
        """Test detection of harm patterns."""
        prohibited_data = {
            "operation": "cause_harm",
            "target": "individuals"
        }
        
        violations = self.engine.verify(prohibited_data)
        self.assertGreater(len(violations), 0)
    
    def test_transparency_requirement(self):
        """Test transparency requirement checking."""
        data_without_explanation = {
            "ai_operation": "classification",
            "result": "positive"
        }
        
        violations = self.engine.verify(data_without_explanation)
        
        # Should flag missing explanation
        transparency_violations = [
            v for v in violations
            if v.constraint == "require_transparency"
        ]
        self.assertGreater(len(transparency_violations), 0)
    
    def test_enforcement_blocks_violations(self):
        """Test that enforcement blocks prohibited content."""
        prohibited_data = {
            "operation": "weapon_system"
        }
        
        # Should raise RuntimeError on enforcement
        with self.assertRaises(RuntimeError):
            self.engine.enforce(prohibited_data)
    
    def test_enforcement_allows_clean_data(self):
        """Test that enforcement allows clean data."""
        clean_data = {
            "operation": "optimize_energy"
        }
        
        # Should not raise
        result = self.engine.enforce(clean_data)
        self.assertTrue(result)
    
    def test_violation_history_tracking(self):
        """Test that violations are tracked in history."""
        self.engine.clear_history()
        
        prohibited_data = {
            "operation": "weapon_targeting"
        }
        
        self.engine.verify(prohibited_data)
        
        history = self.engine.get_violation_history()
        self.assertGreater(len(history), 0)


class TestViolationSeverity(unittest.TestCase):
    """Test cases for violation severity levels."""
    
    def test_severity_levels(self):
        """Test that all severity levels are defined."""
        levels = [
            ViolationSeverity.INFO,
            ViolationSeverity.WARNING,
            ViolationSeverity.ERROR,
            ViolationSeverity.CRITICAL
        ]
        
        for level in levels:
            self.assertIsNotNone(level.value)


if __name__ == "__main__":
    unittest.main()
