# MAYA Node - Compliance System

This directory contains the license enforcement, validation, and compliance infrastructure for MAYA Node deployments.

## Structure

```
compliance/
├── license_enforcement.py      # Core license validation and enforcement
├── ENFORCEMENT-POLICY.md       # Detailed enforcement policies
├── examples/                   # Example license files
│   ├── license-community.json
│   ├── license-standard.json
│   ├── license-professional.json
│   └── license-enterprise.json
└── README.md                   # This file
```

## Overview

The MAYA Node compliance system provides:

1. **License Validation** - Cryptographic verification of license files
2. **Feature Enforcement** - Tier-based feature gating
3. **Capacity Enforcement** - Deployment capacity monitoring and limits
4. **Telemetry Compliance** - Required telemetry for license tiers
5. **Expiry Management** - Grace periods and renewal workflows

## Quick Start

### Installation

The compliance module is included with MAYA Node firmware. To use it:

```python
from compliance.license_enforcement import get_enforcer, require_feature

# Get the global enforcer instance
enforcer = get_enforcer()

# Validate license
status, message = enforcer.validate()
print(f"License status: {status.value} - {message}")

# Check license information
info = enforcer.get_license_info()
print(f"Licensed tier: {info['tier']}")
print(f"Features: {', '.join(info['features'])}")
```

### Using Feature Enforcement

Protect features with the `@require_feature` decorator:

```python
from compliance.license_enforcement import require_feature

@require_feature("extended_forecasting")
def advanced_forecast_algorithm():
    """This function requires Professional or Enterprise license"""
    # Implementation here
    pass

@require_feature("ml_optimization")
def ml_based_optimization():
    """This function requires Enterprise license"""
    # Implementation here
    pass
```

### Checking Capacity

```python
from compliance.license_enforcement import get_enforcer

enforcer = get_enforcer()

# Check if current capacity is within limits
current_capacity = 150.0  # kW
is_valid, message = enforcer.enforce_capacity(current_capacity)

if not is_valid:
    print(f"Capacity violation: {message}")
    # Handle over-capacity situation
```

## License File Format

License files are JSON documents stored at `/etc/maya-node/license.json`:

```json
{
  "license_id": "MAYA-STD-123456-78AB",
  "tier": "standard",
  "deployment_type": "production",
  "issue_date": "2025-11-10T00:00:00Z",
  "expiry_date": "2028-11-10T00:00:00Z",
  "max_capacity_kw": 250,
  "max_sites": 1,
  "site_id": "SITE-EXAMPLE-001",
  "features": ["basic_dispatch", "priority_loads", ...],
  "telemetry_required": true,
  "signature": "cryptographic_signature_here"
}
```

See `examples/` directory for complete examples for each tier.

## License Tiers

| Tier | Production | Max Capacity | Support | Telemetry |
|------|------------|--------------|---------|-----------|
| Community | ✗ | N/A | None | Required |
| Standard | ✓ | 250 kW | 48h | Required |
| Professional | ✓ | 1 MW | 24h | Required |
| Enterprise | ✓ | Unlimited | 4h | Optional |

## Feature Matrix

### Core Features (All Tiers)
- Basic power dispatch
- Priority load management (P1-P3)
- SOC-aware scheduling
- Brownout protection
- Local HMI
- Modbus TCP

### Standard+
- OPC UA
- Web dashboard
- REST API
- Automatic updates

### Professional+
- Extended forecasting (24h)
- Weather API integration
- Mobile app
- Cloud analytics
- Remote diagnostics

### Enterprise Only
- ML optimization
- Multi-site coordination
- V2G/VPP participation
- Custom protocols
- White-labeling
- Predictive maintenance

## Integration Examples

### In Controller Code

```python
# firmware/controller/main.py
from compliance.license_enforcement import get_enforcer

def main():
    # Initialize license enforcement
    enforcer = get_enforcer()
    status, message = enforcer.validate()
    
    if status.value not in ['valid', 'grace_period']:
        print(f"License issue: {message}")
        # Run in safe mode
        run_safe_mode()
        return
    
    # Normal operation
    sensors = SensorBus()
    actuators = ActuatorBus()
    scheduler = PowerScheduler(sensors, actuators)
    
    while True:
        # Check capacity compliance periodically
        if scheduler.tick_count % 3600 == 0:  # Every hour
            current_kw = sensors.total_capacity_kw()
            valid, msg = enforcer.enforce_capacity(current_kw)
            if not valid:
                scheduler.limit_capacity(enforcer.license.max_capacity_kw)
        
        # Normal control loop
        scheduler.update_forecasts()
        scheduler.dispatch()
        scheduler.log_tick()
        actuators.idle_sleep(0.25)
```

### In Scheduler Code

```python
# firmware/controller/scheduler.py
from compliance.license_enforcement import require_feature, get_enforcer

class PowerScheduler:
    def __init__(self, sensors, actuators):
        self.s = sensors
        self.a = actuators
        self.enforcer = get_enforcer()
    
    @require_feature("basic_forecasting")
    def update_forecasts(self):
        """Basic forecasting - available in all tiers"""
        self.gen_forecast = self.s.irradiance_forecast(6*60)
        self.load_forecast = self.s.load_forecast(6*60)
    
    @require_feature("extended_forecasting")
    def update_extended_forecasts(self):
        """Extended forecasting - Professional+ only"""
        self.gen_forecast_24h = self.s.irradiance_forecast(24*60)
        self.load_forecast_24h = self.s.load_forecast(24*60)
    
    @require_feature("ml_optimization")
    def ml_optimize(self):
        """ML optimization - Enterprise only"""
        # Advanced ML-based optimization
        pass
```

### In API Code

```python
# ui/web-dashboard/src/api.py (hypothetical Python backend)
from compliance.license_enforcement import get_enforcer

def get_system_status():
    enforcer = get_enforcer()
    license_info = enforcer.get_license_info()
    
    return {
        "license_tier": license_info["tier"],
        "license_status": license_info["status"],
        "available_features": license_info["features"],
        "capacity_limit": license_info["max_capacity_kw"],
        # ... other system status
    }

def enable_feature(feature_name):
    enforcer = get_enforcer()
    if not enforcer.enforce_feature(feature_name):
        return {
            "error": "Feature not available in current license tier",
            "feature": feature_name,
            "required_tier": get_required_tier(feature_name)
        }
    
    # Enable the feature
    return {"success": True}
```

## Testing

### Development/Testing
Use the Community Edition license during development:

```bash
# Copy the example community license
cp compliance/examples/license-community.json /etc/maya-node/license.json

# Or run without a license (defaults to Community)
# The system will auto-create a default license
```

### Production Testing
For production validation, request a test license from licensing@maya-node.example.com

## License Activation

### Online Activation
1. Obtain license key from MAYA Node portal
2. Run activation utility:
   ```bash
   maya-node-activate --key YOUR-LICENSE-KEY
   ```
3. License file created at `/etc/maya-node/license.json`
4. Restart controller: `systemctl restart maya-node-controller`

### Offline Activation
For air-gapped deployments (Enterprise only):
1. Generate hardware fingerprint:
   ```bash
   maya-node-fingerprint > hardware.json
   ```
2. Submit hardware.json to licensing portal
3. Download signed license file
4. Install license:
   ```bash
   maya-node-activate --file downloaded-license.json
   ```

## Troubleshooting

### License Not Found
**Symptom:** System runs in Community mode despite having license

**Solutions:**
- Check file exists: `ls -la /etc/maya-node/license.json`
- Verify permissions: `chmod 644 /etc/maya-node/license.json`
- Check file format: `python -m json.tool < /etc/maya-node/license.json`

### License Validation Failed
**Symptom:** "License signature invalid" error

**Solutions:**
- Re-download license from portal
- Check file wasn't corrupted during transfer
- Verify system date/time is correct
- Contact support if issue persists

### Feature Not Available
**Symptom:** `PermissionError: Feature 'xxx' not available`

**Solutions:**
- Check license tier: `maya-node-license --info`
- Verify feature is included in your tier (see LICENSE-FRAMEWORK.md)
- Upgrade license if needed
- Contact sales for license upgrade

### Capacity Exceeded
**Symptom:** System limiting power output

**Solutions:**
- Check current vs. licensed capacity: `maya-node-license --capacity`
- Reduce system capacity or upgrade license
- Temporary grace period may be available

### License Expired
**Symptom:** System in grace period or safe mode

**Solutions:**
- Check expiry date: `maya-node-license --info`
- Renew license at portal.maya-node.example.com
- Contact renewals@maya-node.example.com
- 30-day grace period available

## Support

- **Technical Issues:** support@maya-node.example.com
- **License Activation:** licensing@maya-node.example.com
- **License Renewal:** renewals@maya-node.example.com
- **Compliance Questions:** compliance@maya-node.example.com

## Security

### Reporting Security Issues
If you discover a security vulnerability in the licensing system:
- **DO NOT** open a public issue
- Email: security@maya-node.example.com
- Use PGP key available at: https://maya-node.example.com/security/pgp-key.asc
- Expect response within 48 hours

### License Key Security
- Never commit license files to version control
- Protect `/etc/maya-node/license.json` with appropriate permissions
- Regularly rotate license keys (handled automatically on renewal)
- Report lost or stolen license keys immediately

## Related Documentation

- [License Framework](../licensing/LICENSE-FRAMEWORK.md) - Detailed licensing terms and tiers
- [Deployment Matrix](../licensing/DEPLOYMENT-MATRIX.md) - Deployment configurations and requirements
- [Enforcement Policy](./ENFORCEMENT-POLICY.md) - Compliance and enforcement procedures
- [IP Registry](../docs/ip/IP-REGISTRY.md) - Intellectual property tracking

---
*Last Updated: 2025-11-10*
*Compliance Module Version: 1.0*
