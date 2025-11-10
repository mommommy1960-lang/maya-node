"""
MAYA Node - License Validation and Enforcement

This module provides license key validation, deployment authorization,
and feature enforcement for MAYA Node installations.

License: BUSL-1.1 (converts to Apache 2.0 after 4 years)
"""

import hashlib
import json
import time
from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


class LicenseTier(Enum):
    """License tier enumeration"""
    COMMUNITY = "community"
    STANDARD = "standard"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    RESEARCH = "research"
    HUMANITARIAN = "humanitarian"


class DeploymentType(Enum):
    """Deployment type enumeration"""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    STAGING = "staging"
    RESEARCH = "research"


class LicenseStatus(Enum):
    """License status enumeration"""
    VALID = "valid"
    EXPIRED = "expired"
    INVALID = "invalid"
    SUSPENDED = "suspended"
    GRACE_PERIOD = "grace_period"
    NOT_ACTIVATED = "not_activated"


class License:
    """
    Represents a MAYA Node license with validation and feature checking
    """
    
    def __init__(self, license_data: Dict):
        """
        Initialize license from license data dictionary
        
        Args:
            license_data: Dictionary containing license information
        """
        self.license_id = license_data.get("license_id", "")
        self.tier = LicenseTier(license_data.get("tier", "community"))
        self.deployment_type = DeploymentType(license_data.get("deployment_type", "development"))
        self.issue_date = datetime.fromisoformat(license_data.get("issue_date", datetime.now().isoformat()))
        self.expiry_date = datetime.fromisoformat(license_data.get("expiry_date", datetime.now().isoformat()))
        self.max_capacity_kw = license_data.get("max_capacity_kw", 0)
        self.max_sites = license_data.get("max_sites", 0)
        self.features = license_data.get("features", [])
        self.site_id = license_data.get("site_id", "")
        self.signature = license_data.get("signature", "")
        self.telemetry_required = license_data.get("telemetry_required", True)
        
    def verify_signature(self, public_key: str) -> bool:
        """
        Verify the license signature (placeholder implementation)
        
        Args:
            public_key: Public key for signature verification
            
        Returns:
            True if signature is valid, False otherwise
        """
        # In production, implement proper RSA/ECDSA signature verification
        # This is a placeholder for the scaffolding
        license_content = f"{self.license_id}:{self.tier.value}:{self.expiry_date}"
        expected_signature = hashlib.sha256(license_content.encode()).hexdigest()
        return self.signature == expected_signature
    
    def get_status(self) -> LicenseStatus:
        """
        Get current license status
        
        Returns:
            LicenseStatus enum value
        """
        from datetime import timezone
        
        # Ensure we're comparing timezone-aware datetimes
        now = datetime.now(timezone.utc)
        
        # Make expiry_date timezone-aware if it isn't
        expiry = self.expiry_date
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        
        if not self.license_id or not self.signature:
            return LicenseStatus.NOT_ACTIVATED
            
        if now > expiry:
            # Check if within grace period (30 days)
            grace_end = expiry + timedelta(days=30)
            if now <= grace_end:
                return LicenseStatus.GRACE_PERIOD
            return LicenseStatus.EXPIRED
            
        return LicenseStatus.VALID
    
    def is_production_allowed(self) -> bool:
        """
        Check if production deployment is allowed
        
        Returns:
            True if production deployment is authorized
        """
        if self.tier == LicenseTier.COMMUNITY:
            return False
        return self.deployment_type == DeploymentType.PRODUCTION
    
    def check_capacity(self, current_capacity_kw: float) -> Tuple[bool, str]:
        """
        Check if current capacity is within license limits
        
        Args:
            current_capacity_kw: Current system capacity in kW
            
        Returns:
            Tuple of (is_valid, message)
        """
        if self.max_capacity_kw == 0:  # Unlimited
            return True, "Capacity OK"
        
        if current_capacity_kw > self.max_capacity_kw:
            return False, f"Capacity {current_capacity_kw}kW exceeds license limit {self.max_capacity_kw}kW"
        
        return True, "Capacity OK"
    
    def has_feature(self, feature_name: str) -> bool:
        """
        Check if a feature is enabled in this license
        
        Args:
            feature_name: Name of the feature to check
            
        Returns:
            True if feature is enabled
        """
        return feature_name in self.features


class LicenseEnforcer:
    """
    Enforces license restrictions and validates deployment compliance
    """
    
    def __init__(self, license_file: str = "/etc/maya-node/license.json"):
        """
        Initialize the license enforcer
        
        Args:
            license_file: Path to license file
        """
        self.license_file = license_file
        self.license: Optional[License] = None
        self.last_check = 0
        self.check_interval = 3600  # Check every hour
        
    def load_license(self) -> bool:
        """
        Load and validate license from file
        
        Returns:
            True if license loaded successfully
        """
        try:
            with open(self.license_file, 'r') as f:
                license_data = json.load(f)
            self.license = License(license_data)
            return True
        except Exception as e:
            print(f"Failed to load license: {e}")
            # Default to community license
            self.license = License({
                "tier": "community",
                "deployment_type": "development",
                "issue_date": datetime.now().isoformat(),
                "expiry_date": (datetime.now() + timedelta(days=365)).isoformat(),
                "max_capacity_kw": 0,
                "max_sites": 0,
                "features": ["basic_dispatch", "local_hmi"],
                "telemetry_required": True
            })
            return False
    
    def validate(self, force: bool = False) -> Tuple[LicenseStatus, str]:
        """
        Validate the current license
        
        Args:
            force: Force validation even if recently checked
            
        Returns:
            Tuple of (status, message)
        """
        now = time.time()
        if not force and (now - self.last_check) < self.check_interval:
            return LicenseStatus.VALID, "Recently validated"
        
        self.last_check = now
        
        if not self.license:
            self.load_license()
        
        status = self.license.get_status()
        
        if status == LicenseStatus.VALID:
            return status, "License is valid"
        elif status == LicenseStatus.GRACE_PERIOD:
            days_left = (self.license.expiry_date + timedelta(days=30) - datetime.now()).days
            return status, f"License expired, {days_left} days remaining in grace period"
        elif status == LicenseStatus.EXPIRED:
            return status, "License has expired"
        elif status == LicenseStatus.NOT_ACTIVATED:
            return status, "License not activated"
        else:
            return status, "License status unknown"
    
    def enforce_feature(self, feature_name: str) -> bool:
        """
        Check if a feature is allowed and enforce restriction
        
        Args:
            feature_name: Name of the feature to check
            
        Returns:
            True if feature is allowed
        """
        if not self.license:
            self.load_license()
        
        status, _ = self.validate()
        if status in [LicenseStatus.EXPIRED, LicenseStatus.INVALID, LicenseStatus.SUSPENDED]:
            # In expired state, only allow basic safety features
            if feature_name in ["safety_check", "emergency_shutdown"]:
                return True
            return False
        
        return self.license.has_feature(feature_name)
    
    def enforce_capacity(self, current_capacity_kw: float) -> Tuple[bool, str]:
        """
        Enforce capacity restrictions
        
        Args:
            current_capacity_kw: Current system capacity in kW
            
        Returns:
            Tuple of (is_allowed, message)
        """
        if not self.license:
            self.load_license()
        
        return self.license.check_capacity(current_capacity_kw)
    
    def get_license_info(self) -> Dict:
        """
        Get license information for display/logging
        
        Returns:
            Dictionary with license information
        """
        if not self.license:
            self.load_license()
        
        status, message = self.validate()
        
        return {
            "license_id": self.license.license_id or "UNLICENSED",
            "tier": self.license.tier.value,
            "status": status.value,
            "message": message,
            "expiry_date": self.license.expiry_date.isoformat(),
            "max_capacity_kw": self.license.max_capacity_kw,
            "deployment_type": self.license.deployment_type.value,
            "features": self.license.features
        }


class FeatureFlags:
    """
    Feature availability matrix based on license tier
    """
    
    # Core features available in all tiers
    CORE_FEATURES = [
        "basic_dispatch",
        "priority_loads",
        "soc_scheduling",
        "brownout_protection",
        "local_hmi",
        "modbus_tcp"
    ]
    
    # Features by tier
    TIER_FEATURES = {
        LicenseTier.COMMUNITY: CORE_FEATURES + [
            "basic_forecasting",
            "mqtt_telemetry"
        ],
        LicenseTier.STANDARD: CORE_FEATURES + [
            "basic_forecasting",
            "mqtt_telemetry",
            "opc_ua",
            "web_dashboard",
            "auto_updates",
            "rest_api"
        ],
        LicenseTier.PROFESSIONAL: CORE_FEATURES + [
            "basic_forecasting",
            "extended_forecasting",
            "weather_api",
            "mqtt_telemetry",
            "opc_ua",
            "web_dashboard",
            "mobile_app",
            "cloud_analytics",
            "auto_updates",
            "rest_api",
            "remote_diagnostics"
        ],
        LicenseTier.ENTERPRISE: CORE_FEATURES + [
            "basic_forecasting",
            "extended_forecasting",
            "weather_api",
            "ml_optimization",
            "multi_site",
            "v2g_vpp",
            "mqtt_telemetry",
            "opc_ua",
            "custom_protocols",
            "web_dashboard",
            "mobile_app",
            "cloud_analytics",
            "custom_reporting",
            "auto_updates",
            "rest_api",
            "remote_diagnostics",
            "predictive_maintenance",
            "white_labeling"
        ],
        LicenseTier.RESEARCH: CORE_FEATURES + [
            "basic_forecasting",
            "extended_forecasting",
            "mqtt_telemetry",
            "web_dashboard",
            "rest_api"
        ],
        LicenseTier.HUMANITARIAN: CORE_FEATURES + [
            "basic_forecasting",
            "mqtt_telemetry",
            "web_dashboard",
            "rest_api"
        ]
    }
    
    @staticmethod
    def get_features_for_tier(tier: LicenseTier) -> List[str]:
        """
        Get list of available features for a license tier
        
        Args:
            tier: License tier
            
        Returns:
            List of feature names
        """
        return FeatureFlags.TIER_FEATURES.get(tier, FeatureFlags.CORE_FEATURES)
    
    @staticmethod
    def is_feature_available(tier: LicenseTier, feature: str) -> bool:
        """
        Check if a feature is available in a license tier
        
        Args:
            tier: License tier
            feature: Feature name
            
        Returns:
            True if feature is available
        """
        return feature in FeatureFlags.get_features_for_tier(tier)


# Global enforcer instance
_enforcer: Optional[LicenseEnforcer] = None


def get_enforcer() -> LicenseEnforcer:
    """
    Get the global license enforcer instance
    
    Returns:
        LicenseEnforcer instance
    """
    global _enforcer
    if _enforcer is None:
        _enforcer = LicenseEnforcer()
        _enforcer.load_license()
    return _enforcer


def require_feature(feature_name: str):
    """
    Decorator to enforce feature availability
    
    Args:
        feature_name: Name of required feature
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            enforcer = get_enforcer()
            if not enforcer.enforce_feature(feature_name):
                raise PermissionError(f"Feature '{feature_name}' not available in current license")
            return func(*args, **kwargs)
        return wrapper
    return decorator
