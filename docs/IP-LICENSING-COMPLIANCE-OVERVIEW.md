# MAYA Node - IP Control, Licensing, and Compliance Overview

## Executive Summary

This document provides a comprehensive overview of the intellectual property (IP) control, licensing framework, deployment matrix, and enforcement structure implemented for MAYA Node.

## Components

### 1. Intellectual Property Control

**Location:** `docs/ip/IP-REGISTRY.md`

**Purpose:** Track and protect MAYA Node intellectual property assets

**Key Elements:**
- Patent portfolio tracking (pending and potential)
- Trade secret identification and classification
- Proprietary algorithm documentation
- Third-party component tracking
- Geographic protection strategy
- Confidentiality guidelines

**Protected Assets:**
- Predictive power dispatch algorithms
- Thermal integration control systems
- Fast load shedding protocols (<50ms)
- Battery SOC forecasting models
- Load prediction algorithms
- Efficiency optimization techniques

**Protection Mechanism:** Dual-license model (BUSL-1.1 + Apache 2.0)

### 2. Licensing Framework

**Location:** `licensing/LICENSE-FRAMEWORK.md`

**Purpose:** Define clear licensing terms, tiers, and usage rights

#### Dual-License Model

##### Business Source License 1.1 (BUSL-1.1)
- Applies to core business logic and control algorithms
- Source viewable but production use requires commercial license
- Automatically converts to Apache 2.0 after 4 years
- Additional Use Grants for specific scenarios

##### Apache License 2.0
- Applies to supporting infrastructure, examples, tools
- Permissive open-source license
- Free commercial and non-commercial use

#### License Tiers

| Tier | Cost | Production | Capacity | Sites | Support |
|------|------|------------|----------|-------|---------|
| **Community** | Free | ✗ | N/A | 0 | None |
| **Standard** | Per-deployment | ✓ | 250 kW | 1 | 48h |
| **Professional** | Annual subscription | ✓ | 1 MW | 5 | 24h |
| **Enterprise** | Custom | ✓ | Unlimited | Unlimited | 4h |

#### Special Grants
- Research and Education Grant
- Humanitarian Use Grant
- Open Source Contributor Grant

#### Feature Matrix
Comprehensive feature availability across tiers:
- Core features: Available in all tiers
- Advanced features: Professional+ (forecasting, analytics)
- Enterprise features: ML optimization, VPP, white-labeling

### 3. Deployment Matrix

**Location:** `licensing/DEPLOYMENT-MATRIX.md`

**Purpose:** Define supported deployments, features, and regional requirements

#### Environment Types

**Production Environments:**
- Critical Infrastructure (telecom, data centers, hospitals)
- Industrial (manufacturing, fleet depots)
- Commercial (retail, offices)
- Residential Microgrids
- Humanitarian (refugee camps, clinics)
- Remote/Off-Grid

**Non-Production:**
- Development
- Staging
- Research
- Training

#### Regional Compliance Matrix

Comprehensive coverage of:
- North America (UL 1741 SB, IEEE 1547)
- Caribbean (Hurricane-rated, island deployments)
- Latin America (NOM, CFE standards)
- Europe (EN 50549, CE marking, GDPR)
- Africa (IEC 62109, priority deployment region)
- Asia-Pacific (AS/NZS 4777, high-temp variants)
- Middle East (DEWA, SEC, high-temp variants)

#### Deployment Size Categories
- Small (10-50 kW): Clinics, small communities
- Medium (50-250 kW): Telecom towers, industrial
- Large (250-1000 kW): Data centers, campuses
- Very Large (1+ MW): Community microgrids, VPP

#### Environmental Operating Conditions
- Standard: -10°C to +45°C
- Extended: -20°C to +55°C
- Extreme: -40°C to +65°C (custom)

### 4. Enforcement Structure

**Location:** `compliance/`

**Purpose:** Technical and operational license enforcement

#### Components

##### A. License Enforcement Module (`license_enforcement.py`)

**Features:**
- License file validation with cryptographic signatures
- Tier-based feature gating
- Capacity monitoring and enforcement
- Expiry management with grace periods
- Hardware fingerprinting
- Telemetry compliance checking

**Key Classes:**
- `License`: Represents a license with validation methods
- `LicenseEnforcer`: Core enforcement engine
- `FeatureFlags`: Feature availability matrix
- `LicenseTier`, `DeploymentType`, `LicenseStatus`: Enums

**Usage:**
```python
from compliance.license_enforcement import get_enforcer, require_feature

enforcer = get_enforcer()
status, message = enforcer.validate()

@require_feature("extended_forecasting")
def advanced_feature():
    pass
```

##### B. Enforcement Policy (`ENFORCEMENT-POLICY.md`)

**Defines:**
- Activation requirements by tier
- Hardware fingerprinting mechanism
- License transfer procedures
- Technical enforcement (validation, feature gating, capacity)
- Operational enforcement (expiry, violations, capacity)
- Audit process and procedures
- Violation categories and remediation
- Monitoring and detection systems
- Data privacy and security
- Compliance support resources

**Violation Categories:**
1. Administrative (grace period, documentation)
2. Capacity (exceeds limits, unauthorized features)
3. Material (production use on Community, key sharing)
4. Willful (forgery, cracking, redistribution)

**Enforcement Timeline:**
- Expiry Day 0: Warning, full functionality
- Days 1-30: Grace period, daily warnings
- Day 31+: Safe mode only (critical features)

##### C. Example Licenses (`examples/`)

Complete example license files for each tier:
- `license-community.json`: Development/testing
- `license-standard.json`: Single-site production (250 kW)
- `license-professional.json`: Multi-site production (1 MW, 5 sites)
- `license-enterprise.json`: Unlimited deployment

##### D. Compliance Documentation (`README.md`)

Comprehensive integration guide covering:
- Quick start and installation
- Feature enforcement patterns
- Capacity checking
- License file format
- Integration examples (controller, scheduler, API)
- Testing procedures
- Activation (online and offline)
- Troubleshooting
- Security best practices

## Integration Points

### Firmware Controller

```python
# firmware/controller/main.py
from compliance.license_enforcement import get_enforcer

enforcer = get_enforcer()
status, message = enforcer.validate()

if status not in ['valid', 'grace_period']:
    run_safe_mode()
```

### Power Scheduler

```python
# firmware/controller/scheduler.py
from compliance.license_enforcement import require_feature

@require_feature("extended_forecasting")
def update_extended_forecasts(self):
    # Professional+ feature
    pass
```

### Web Dashboard

Display license status, tier, and available features in UI.

### API Endpoints

Gate advanced API endpoints based on license tier.

## Telemetry and Privacy

### Data Collected (When Required)
- System capacity and utilization (anonymized)
- Feature usage statistics
- Error and fault logging
- Performance metrics

### Data NOT Collected
- Personally identifiable information
- Site-specific location data (unless opted in)
- Customer business data

### Privacy Compliance
- GDPR compliant
- CCPA compliant
- Regional privacy laws

### Telemetry by Tier
- Community/Standard/Professional: Required
- Enterprise: Optional/configurable

## Security Considerations

### License Security
- Cryptographically signed license files
- Hardware fingerprinting prevents unauthorized transfer
- Regular signature key rotation
- HSM storage for private keys

### Runtime Security
- License validation at startup and periodic checks
- Tamper detection for license files
- Secure storage at `/etc/maya-node/license.json`
- Permission controls (644 recommended)

### Vulnerability Reporting
- Dedicated security contact: security@maya-node.example.com
- PGP-encrypted reporting encouraged
- 48-hour response time commitment

## Support and Resources

### Documentation
- IP Registry: `docs/ip/IP-REGISTRY.md`
- License Framework: `licensing/LICENSE-FRAMEWORK.md`
- Deployment Matrix: `licensing/DEPLOYMENT-MATRIX.md`
- Enforcement Policy: `compliance/ENFORCEMENT-POLICY.md`
- Compliance README: `compliance/README.md`

### Contact Points
- **Sales:** sales@maya-node.example.com
- **Licensing:** licensing@maya-node.example.com
- **Renewals:** renewals@maya-node.example.com
- **Technical Support:** support@maya-node.example.com
- **Compliance:** compliance@maya-node.example.com
- **Security:** security@maya-node.example.com
- **Legal:** legal@maya-node.example.com

### Self-Service Tools
- License Portal: portal.maya-node.example.com
- Capacity calculator
- License upgrade wizard
- Renewal automation
- Audit report generation

## Deployment Workflow

### For Developers (Community Edition)
1. Clone repository
2. Accept BUSL-1.1 terms
3. Use for development/testing/research
4. System defaults to Community license
5. Full source access, no production use

### For Commercial Deployment (Standard+)
1. Contact sales for licensing
2. Receive license key
3. Deploy hardware
4. Activate license (online or offline)
5. System validates and enables features
6. Periodic validation checks
7. Annual renewal (Professional/Enterprise)

### For Enterprise
1. Custom engagement with account manager
2. Tailored licensing terms
3. Optional source code escrow
4. OEM/redistribution rights available
5. White-labeling options
6. Extended modification rights

## Compliance Verification

### Self-Check
- Verify license status: `maya-node-license --info`
- Check capacity: `maya-node-license --capacity`
- Review features: `maya-node-license --features`

### Regular Audits
- Professional: Annual
- Enterprise: Per agreement
- 30-day advance notice
- Remote review preferred
- Documentation and telemetry review

### Voluntary Disclosure
Self-reported compliance issues receive:
- Extended cure period (60 days)
- Waived late fees (first occurrence)
- No penalties if resolved promptly

## Future Enhancements

### Planned Features
- Automated license renewal system
- Usage-based billing options (metered licensing)
- Fleet management dashboard
- Multi-tenant licensing for resellers
- Blockchain-based license registry
- AI-powered compliance anomaly detection

### Roadmap Alignment
- V2G/VPP aggregation (Enterprise feature)
- Advanced ML optimization (Enterprise feature)
- Multi-site coordination (Professional+)
- Custom protocol development (Enterprise)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-10 | Initial IP control, licensing, deployment matrix, and enforcement structure |

## License

This documentation and compliance framework itself:
- **Documentation:** Apache 2.0
- **Enforcement Code:** BUSL-1.1 (converts to Apache 2.0 after 4 years)

## Conclusion

The MAYA Node IP control, licensing, deployment matrix, and enforcement structure provides:

1. **Clear IP Protection:** Comprehensive tracking and legal protection of proprietary assets
2. **Flexible Licensing:** Multiple tiers to serve different markets and use cases
3. **Global Deployment:** Regional compliance and certification matrix
4. **Fair Enforcement:** Balanced enforcement with grace periods and support
5. **Open Core Model:** Core safety features always available, advanced features gated
6. **Sustainable Business:** Commercial viability while supporting open-source principles

This foundation enables MAYA Node to:
- Protect intellectual property investments
- Generate sustainable revenue
- Support open-source community
- Scale globally with regional compliance
- Provide clear value differentiation across tiers
- Maintain fairness and transparency in licensing

---
*Document Version: 1.0*
*Last Updated: 2025-11-10*
*Classification: Public*
