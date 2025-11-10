"""
Simple validation test for license enforcement module

This test verifies the basic functionality of the license enforcement system.
"""

import json
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compliance.license_enforcement import (
    License, LicenseEnforcer, LicenseTier, DeploymentType, 
    LicenseStatus, FeatureFlags
)


def test_license_creation():
    """Test basic license creation and validation"""
    print("Testing license creation...")
    
    license_data = {
        "license_id": "TEST-123",
        "tier": "standard",
        "deployment_type": "production",
        "issue_date": datetime.now().isoformat(),
        "expiry_date": (datetime.now() + timedelta(days=365)).isoformat(),
        "max_capacity_kw": 250,
        "max_sites": 1,
        "site_id": "TEST-SITE-001",
        "features": ["basic_dispatch", "web_dashboard"],
        "telemetry_required": True,
        "signature": "test_signature"
    }
    
    license = License(license_data)
    
    assert license.license_id == "TEST-123"
    assert license.tier == LicenseTier.STANDARD
    assert license.max_capacity_kw == 250
    assert license.has_feature("basic_dispatch")
    assert not license.has_feature("ml_optimization")
    
    print("✓ License creation test passed")


def test_license_status():
    """Test license status checking"""
    print("Testing license status...")
    
    # Valid license
    valid_license = License({
        "license_id": "VALID-123",
        "tier": "professional",
        "deployment_type": "production",
        "issue_date": datetime.now().isoformat(),
        "expiry_date": (datetime.now() + timedelta(days=365)).isoformat(),
        "max_capacity_kw": 1000,
        "max_sites": 5,
        "features": [],
        "signature": "test_sig"
    })
    
    status = valid_license.get_status()
    assert status == LicenseStatus.VALID
    
    # Expired license
    expired_license = License({
        "license_id": "EXPIRED-123",
        "tier": "standard",
        "deployment_type": "production",
        "issue_date": (datetime.now() - timedelta(days=400)).isoformat(),
        "expiry_date": (datetime.now() - timedelta(days=35)).isoformat(),
        "max_capacity_kw": 250,
        "max_sites": 1,
        "features": [],
        "signature": "test_sig"
    })
    
    status = expired_license.get_status()
    assert status == LicenseStatus.EXPIRED
    
    print("✓ License status test passed")


def test_capacity_checking():
    """Test capacity enforcement"""
    print("Testing capacity checking...")
    
    license = License({
        "license_id": "CAP-TEST-123",
        "tier": "standard",
        "deployment_type": "production",
        "issue_date": datetime.now().isoformat(),
        "expiry_date": (datetime.now() + timedelta(days=365)).isoformat(),
        "max_capacity_kw": 250,
        "max_sites": 1,
        "features": [],
        "signature": "test_sig"
    })
    
    # Within capacity
    valid, msg = license.check_capacity(200)
    assert valid
    
    # Over capacity
    valid, msg = license.check_capacity(300)
    assert not valid
    
    print("✓ Capacity checking test passed")


def test_production_allowed():
    """Test production deployment authorization"""
    print("Testing production authorization...")
    
    # Community license - no production
    community = License({
        "tier": "community",
        "deployment_type": "development",
        "issue_date": datetime.now().isoformat(),
        "expiry_date": (datetime.now() + timedelta(days=365)).isoformat(),
        "max_capacity_kw": 0,
        "max_sites": 0,
        "features": [],
        "signature": "test"
    })
    assert not community.is_production_allowed()
    
    # Standard license - production OK
    standard = License({
        "tier": "standard",
        "deployment_type": "production",
        "issue_date": datetime.now().isoformat(),
        "expiry_date": (datetime.now() + timedelta(days=365)).isoformat(),
        "max_capacity_kw": 250,
        "max_sites": 1,
        "features": [],
        "signature": "test"
    })
    assert standard.is_production_allowed()
    
    print("✓ Production authorization test passed")


def test_feature_flags():
    """Test feature availability matrix"""
    print("Testing feature flags...")
    
    # Community tier
    community_features = FeatureFlags.get_features_for_tier(LicenseTier.COMMUNITY)
    assert "basic_dispatch" in community_features
    assert "ml_optimization" not in community_features
    
    # Professional tier
    pro_features = FeatureFlags.get_features_for_tier(LicenseTier.PROFESSIONAL)
    assert "extended_forecasting" in pro_features
    assert "ml_optimization" not in pro_features
    
    # Enterprise tier
    ent_features = FeatureFlags.get_features_for_tier(LicenseTier.ENTERPRISE)
    assert "ml_optimization" in ent_features
    assert "v2g_vpp" in ent_features
    
    print("✓ Feature flags test passed")


def test_example_licenses():
    """Test that example license files are valid JSON"""
    print("Testing example license files...")
    
    examples_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "compliance", "examples"
    )
    
    for filename in ["license-community.json", "license-standard.json", 
                     "license-professional.json", "license-enterprise.json"]:
        filepath = os.path.join(examples_dir, filename)
        
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        # Create license from example
        license = License(data)
        assert license.license_id
        assert license.tier
        
    print("✓ Example license files test passed")


def run_all_tests():
    """Run all validation tests"""
    print("\n" + "="*60)
    print("MAYA Node License Enforcement - Validation Tests")
    print("="*60 + "\n")
    
    tests = [
        test_license_creation,
        test_license_status,
        test_capacity_checking,
        test_production_allowed,
        test_feature_flags,
        test_example_licenses
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
