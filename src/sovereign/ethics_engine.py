# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Ethics Engine - Constraint Verification and Boundary Enforcement

This module implements the ethical constraint verification system that ensures
all AI operations comply with CERL-1.0 requirements.

Key Responsibilities:
- Verify ethical boundaries before and after operations
- Detect prohibited use patterns
- Enforce transparency requirements
- Maintain audit trail of all decisions
- Provide explainable constraint violations
"""

import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ViolationSeverity(Enum):
    """Severity levels for ethical violations"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class EthicsViolation:
    """Represents an ethical constraint violation"""
    severity: ViolationSeverity
    constraint: str
    description: str
    data: Optional[Dict[str, Any]] = None
    recommendation: Optional[str] = None


class EthicsEngine:
    """
    Ethics constraint verification engine.
    
    Enforces CERL-1.0 ethical constraints including:
    - Prohibition of weaponization and harm
    - Privacy and surveillance restrictions
    - AI transparency requirements
    - Human autonomy preservation
    """
    
    def __init__(self):
        """Initialize the ethics engine with CERL-1.0 constraints."""
        logger.info("Initializing Ethics Engine")
        
        # Define prohibited use patterns
        self.prohibited_patterns = {
            "weaponization": ["weapon", "military", "missile", "explosive", "warfare"],
            "surveillance": ["track", "monitor", "surveil", "spy", "stalk"],
            "harm": ["harm", "hurt", "damage", "injure", "kill"],
            "manipulation": ["manipulate", "deceive", "coerce", "trick", "exploit"],
            "discrimination": ["discriminate", "bias", "prejudice", "exclude"]
        }
        
        # Constraint rules
        self.constraints = [
            "no_weaponization",
            "no_surveillance",
            "no_harm",
            "no_manipulation",
            "no_discrimination",
            "require_transparency",
            "require_auditability",
            "respect_autonomy"
        ]
        
        self.violation_history = []
        logger.info(f"Loaded {len(self.constraints)} ethical constraints")
    
    def verify(self, data: Dict[str, Any], context: str = "") -> List[EthicsViolation]:
        """
        Verify data against all ethical constraints.
        
        Args:
            data: Data to verify
            context: Context information for better violation detection
            
        Returns:
            List of violations found (empty if all constraints satisfied)
        """
        violations = []
        
        # Check for prohibited patterns
        violations.extend(self._check_prohibited_patterns(data))
        
        # Check transparency requirements
        violations.extend(self._check_transparency(data))
        
        # Check autonomy preservation
        violations.extend(self._check_autonomy(data))
        
        # Log all violations
        for violation in violations:
            self.violation_history.append(violation)
            logger.warning(f"Ethics violation: {violation.constraint} - {violation.description}")
        
        if not violations:
            logger.info(f"Ethics verification passed for context: {context}")
        
        return violations
    
    def _check_prohibited_patterns(self, data: Dict[str, Any]) -> List[EthicsViolation]:
        """
        Check for prohibited use patterns.
        
        Args:
            data: Data to check
            
        Returns:
            List of violations found
        """
        violations = []
        data_str = str(data).lower()
        
        for category, patterns in self.prohibited_patterns.items():
            for pattern in patterns:
                if pattern in data_str:
                    violation = EthicsViolation(
                        severity=ViolationSeverity.ERROR,
                        constraint=f"no_{category}",
                        description=f"Prohibited pattern detected: {pattern}",
                        data={"pattern": pattern, "category": category},
                        recommendation="Remove prohibited content or context"
                    )
                    violations.append(violation)
        
        return violations
    
    def _check_transparency(self, data: Dict[str, Any]) -> List[EthicsViolation]:
        """
        Check transparency requirements.
        
        Args:
            data: Data to check
            
        Returns:
            List of violations found
        """
        violations = []
        
        # TODO: Implement actual transparency checks
        # Placeholder: Check if AI operations are documented
        
        if "ai_operation" in data and "explanation" not in data:
            violation = EthicsViolation(
                severity=ViolationSeverity.WARNING,
                constraint="require_transparency",
                description="AI operation lacks explanation",
                recommendation="Add explanation field for transparency"
            )
            violations.append(violation)
        
        return violations
    
    def _check_autonomy(self, data: Dict[str, Any]) -> List[EthicsViolation]:
        """
        Check human autonomy preservation.
        
        Args:
            data: Data to check
            
        Returns:
            List of violations found
        """
        violations = []
        
        # TODO: Implement actual autonomy checks
        # Placeholder: Check for override capability
        
        if "automated_decision" in data and "human_override" not in data:
            violation = EthicsViolation(
                severity=ViolationSeverity.WARNING,
                constraint="respect_autonomy",
                description="Automated decision lacks human override option",
                recommendation="Add human override capability"
            )
            violations.append(violation)
        
        return violations
    
    def enforce(self, data: Dict[str, Any], context: str = "") -> bool:
        """
        Enforce ethical constraints - verify and raise on violations.
        
        Args:
            data: Data to enforce constraints on
            context: Context information
            
        Returns:
            True if all constraints satisfied
            
        Raises:
            RuntimeError: If critical violations found
        """
        violations = self.verify(data, context)
        
        # Check for critical violations
        critical = [v for v in violations if v.severity == ViolationSeverity.CRITICAL]
        errors = [v for v in violations if v.severity == ViolationSeverity.ERROR]
        
        if critical:
            raise RuntimeError(
                f"Critical ethics violation: {critical[0].constraint} - {critical[0].description}"
            )
        
        if errors:
            logger.error(f"Ethics enforcement failed: {len(errors)} error(s)")
            raise RuntimeError(
                f"Ethics violation: {errors[0].constraint} - {errors[0].description}"
            )
        
        return True
    
    def get_violation_history(self) -> List[EthicsViolation]:
        """
        Get complete violation history.
        
        Returns:
            List of all violations detected
        """
        return self.violation_history.copy()
    
    def clear_history(self) -> None:
        """Clear violation history (for testing purposes)."""
        self.violation_history.clear()
        logger.info("Ethics violation history cleared")


def main():
    """Example usage of the ethics engine."""
    
    engine = EthicsEngine()
    
    # Test 1: Clean data
    clean_data = {
        "operation": "optimize_energy",
        "context": "microgrid balancing"
    }
    
    violations = engine.verify(clean_data, "test_clean")
    print(f"Clean data violations: {len(violations)}")
    
    # Test 2: Data with prohibited pattern
    prohibited_data = {
        "operation": "weapon_targeting",
        "context": "military application"
    }
    
    violations = engine.verify(prohibited_data, "test_prohibited")
    print(f"Prohibited data violations: {len(violations)}")
    for v in violations:
        print(f"  - {v.constraint}: {v.description}")
    
    # Test 3: Enforcement
    try:
        engine.enforce(prohibited_data, "test_enforce")
    except RuntimeError as e:
        print(f"Enforcement blocked: {e}")


if __name__ == "__main__":
    main()
