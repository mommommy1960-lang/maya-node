#!/usr/bin/env python3
"""
Compliance Guardrails
Validates deployments against regulatory and safety requirements
"""

import sys
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class ComplianceLevel(Enum):
    """Compliance severity levels"""
    CRITICAL = "critical"  # Deployment blocker
    HIGH = "high"          # Requires remediation
    MEDIUM = "medium"      # Should be addressed
    LOW = "low"            # Advisory


@dataclass
class ComplianceCheck:
    """Individual compliance check"""
    name: str
    level: ComplianceLevel
    passed: bool
    message: str
    remediation: Optional[str] = None


class ComplianceGuardrails:
    """Enforces compliance policies for MAYA Node deployments"""
    
    def __init__(self):
        self.checks: List[ComplianceCheck] = []
        
    def validate_site(self, site_config: Dict) -> bool:
        """
        Validate site configuration against compliance requirements
        Returns: True if all critical checks pass
        """
        print("Running Compliance Validation...")
        print("=" * 60)
        
        # Electrical safety checks
        self._check_electrical_safety(site_config)
        
        # Network security checks
        self._check_network_security(site_config)
        
        # Certification requirements
        self._check_certifications(site_config)
        
        # Data protection
        self._check_data_protection(site_config)
        
        # Environmental compliance
        self._check_environmental(site_config)
        
        # Generate report
        return self._generate_report()
    
    def _check_electrical_safety(self, config: Dict):
        """Validate electrical safety requirements"""
        
        # Ground fault protection
        has_gfd = config.get('ground_fault_protection', False)
        self.checks.append(ComplianceCheck(
            name="Ground Fault Detection",
            level=ComplianceLevel.CRITICAL,
            passed=has_gfd,
            message="GFD/RCD protection required" if not has_gfd else "GFD enabled",
            remediation="Install ground fault detection circuit breakers"
        ))
        
        # Arc fault protection
        has_arc_fault = config.get('arc_fault_protection', False)
        self.checks.append(ComplianceCheck(
            name="Arc Fault Protection",
            level=ComplianceLevel.HIGH,
            passed=has_arc_fault,
            message="Arc fault protection required" if not has_arc_fault else "Arc fault protection enabled",
            remediation="Install arc fault circuit interrupters (AFCI)"
        ))
        
        # Surge protection
        has_surge = config.get('surge_protection', False)
        self.checks.append(ComplianceCheck(
            name="Surge Protection",
            level=ComplianceLevel.HIGH,
            passed=has_surge,
            message="Surge protection devices required" if not has_surge else "SPD installed",
            remediation="Install Type 1/Type 2 surge protection devices"
        ))
    
    def _check_network_security(self, config: Dict):
        """Validate network security requirements"""
        
        # Encryption in transit
        has_tls = config.get('encryption_in_transit', False)
        self.checks.append(ComplianceCheck(
            name="Encryption in Transit",
            level=ComplianceLevel.CRITICAL,
            passed=has_tls,
            message="TLS/mTLS required for control plane" if not has_tls else "Encryption enabled",
            remediation="Enable mTLS for all control plane communications"
        ))
        
        # Authentication
        has_auth = config.get('authentication', False)
        self.checks.append(ComplianceCheck(
            name="Authentication",
            level=ComplianceLevel.CRITICAL,
            passed=has_auth,
            message="Strong authentication required" if not has_auth else "Authentication configured",
            remediation="Configure certificate-based or token-based authentication"
        ))
    
    def _check_certifications(self, config: Dict):
        """Validate required certifications"""
        
        certifications = config.get('certifications', [])
        
        # UL certification
        has_ul = 'UL' in certifications
        self.checks.append(ComplianceCheck(
            name="UL Certification",
            level=ComplianceLevel.CRITICAL,
            passed=has_ul,
            message="UL listing required" if not has_ul else "UL certified",
            remediation="Obtain UL 1741 or UL 9540 certification"
        ))
        
        # IEEE standards
        has_ieee = 'IEEE' in certifications
        self.checks.append(ComplianceCheck(
            name="IEEE Compliance",
            level=ComplianceLevel.HIGH,
            passed=has_ieee,
            message="IEEE 1547 compliance required" if not has_ieee else "IEEE compliant",
            remediation="Verify IEEE 1547 grid interconnection compliance"
        ))
    
    def _check_data_protection(self, config: Dict):
        """Validate data protection requirements"""
        
        # Encryption at rest
        has_encryption = config.get('encryption_at_rest', False)
        self.checks.append(ComplianceCheck(
            name="Data Encryption at Rest",
            level=ComplianceLevel.HIGH,
            passed=has_encryption,
            message="Data encryption required" if not has_encryption else "Encryption enabled",
            remediation="Enable full-disk encryption for telemetry storage"
        ))
        
        # Audit logging
        has_audit = config.get('audit_trail', False)
        self.checks.append(ComplianceCheck(
            name="Audit Trail",
            level=ComplianceLevel.MEDIUM,
            passed=has_audit,
            message="Audit logging required" if not has_audit else "Audit trail enabled",
            remediation="Enable comprehensive audit logging for all operations"
        ))
    
    def _check_environmental(self, config: Dict):
        """Validate environmental compliance"""
        
        # Temperature monitoring
        has_temp_monitoring = config.get('temperature_monitoring', False)
        self.checks.append(ComplianceCheck(
            name="Temperature Monitoring",
            level=ComplianceLevel.MEDIUM,
            passed=has_temp_monitoring,
            message="Temperature monitoring recommended" if not has_temp_monitoring else "Monitoring enabled",
            remediation="Install temperature sensors for thermal management"
        ))
    
    def _generate_report(self) -> bool:
        """Generate compliance report and return pass/fail status"""
        
        critical_failures = []
        high_failures = []
        medium_failures = []
        low_failures = []
        
        for check in self.checks:
            status = "✓ PASS" if check.passed else "✗ FAIL"
            print(f"{status} [{check.level.value.upper()}] {check.name}")
            print(f"       {check.message}")
            
            if not check.passed:
                if check.remediation:
                    print(f"       Remediation: {check.remediation}")
                
                if check.level == ComplianceLevel.CRITICAL:
                    critical_failures.append(check)
                elif check.level == ComplianceLevel.HIGH:
                    high_failures.append(check)
                elif check.level == ComplianceLevel.MEDIUM:
                    medium_failures.append(check)
                else:
                    low_failures.append(check)
            print()
        
        print("=" * 60)
        print("Compliance Summary:")
        print(f"  Total Checks: {len(self.checks)}")
        print(f"  Passed: {sum(1 for c in self.checks if c.passed)}")
        print(f"  Failed: {sum(1 for c in self.checks if not c.passed)}")
        
        if critical_failures:
            print(f"\n  ⚠ CRITICAL Failures: {len(critical_failures)}")
            print("  Deployment BLOCKED - must resolve critical issues")
            return False
        
        if high_failures:
            print(f"\n  ⚠ HIGH Priority Issues: {len(high_failures)}")
            print("  Strongly recommend resolving before deployment")
        
        if medium_failures or low_failures:
            print(f"\n  ℹ Lower Priority Issues: {len(medium_failures) + len(low_failures)}")
            print("  Address during post-deployment optimization")
        
        print("\n✓ Compliance validation passed - deployment approved")
        return True


def main():
    """Example usage"""
    
    # Example site configuration
    example_config = {
        'site_id': 'fleet-depot-001',
        'ground_fault_protection': True,
        'arc_fault_protection': True,
        'surge_protection': True,
        'encryption_in_transit': True,
        'authentication': True,
        'certifications': ['UL', 'IEEE'],
        'encryption_at_rest': True,
        'audit_trail': True,
        'temperature_monitoring': True
    }
    
    guardrails = ComplianceGuardrails()
    passed = guardrails.validate_site(example_config)
    
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
