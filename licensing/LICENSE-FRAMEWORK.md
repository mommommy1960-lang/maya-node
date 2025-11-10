# MAYA Node - Licensing Framework

## Dual-License Model

MAYA Node uses a dual-licensing approach to balance open-source principles with commercial sustainability:

### 1. Business Source License 1.1 (BUSL-1.1)
**Applies to:** Core business logic, control algorithms, proprietary features

**Key Terms:**
- Source code is available and viewable
- Non-production use is permitted (development, testing, research)
- Production use requires a commercial license
- After 4 years, automatically converts to Apache 2.0
- Additional Use Grant may permit specific production scenarios

**Protected Components:**
- `firmware/controller/scheduler.py` - Power scheduling logic
- `firmware/controller/main.py` - Control loop
- Thermal integration algorithms
- Advanced forecasting models
- Priority load management system

**Change Date:** 4 years from release date
**Change License:** Apache License 2.0

### 2. Apache License 2.0
**Applies to:** Supporting infrastructure, examples, tools, documentation

**Key Terms:**
- Permissive open-source license
- Commercial and non-commercial use permitted
- Attribution required
- Patent grant included

**Open Components:**
- Documentation (`docs/`)
- Configuration examples (`examples/`)
- Web dashboard UI (`ui/web-dashboard/`)
- Test utilities (`firmware/edge-tests/`)
- API specifications

## License Tiers

### Community Edition (Non-Production)
**Cost:** Free
**License:** BUSL-1.1 Additional Use Grant

**Includes:**
- Full source code access
- Development and testing rights
- Educational use
- Research and evaluation
- Single-site non-production deployment

**Restrictions:**
- No production/commercial use
- No revenue-generating deployments
- Telemetry must be enabled
- No warranty or support SLA

### Standard Edition (Production)
**Cost:** Per-deployment fee
**License:** BUSL-1.1 Commercial License

**Includes:**
- Production deployment rights
- Up to 250 kW total capacity per license
- Email support (48h response SLA)
- Security updates and patches
- Deployment at single site

**Restrictions:**
- Single site per license
- No redistribution rights
- No modification of core algorithms
- Must maintain telemetry connection (anonymized)

### Professional Edition
**Cost:** Annual subscription per deployment
**License:** BUSL-1.1 Commercial License + Extended Grant

**Includes:**
- Production deployment rights
- Up to 1 MW total capacity per license
- Priority support (24h response SLA)
- Custom integrations assistance
- Advanced analytics and monitoring
- Multi-site management (up to 5 sites)
- Right to modify non-core components

**Restrictions:**
- No redistribution without written approval
- Core algorithms remain proprietary
- Telemetry required

### Enterprise Edition
**Cost:** Custom pricing
**License:** Custom Commercial License

**Includes:**
- Unlimited capacity and sites
- White-glove support (4h response SLA)
- Source code escrow
- Custom feature development
- Training and certification
- Extended modification rights
- Optional: source code license for integration
- Optional: OEM/redistribution rights

**Customizable:**
- SLA terms
- Feature priorities
- Integration requirements
- Regional deployment restrictions

## Additional Use Grants

### Research and Education Grant
Organizations may use MAYA Node in production for non-commercial research and educational purposes under BUSL-1.1 with Additional Use Grant upon application and approval.

### Humanitarian Use Grant
Qualified humanitarian organizations may receive free or reduced-cost licenses for disaster relief, refugee services, or emergency medical facilities.

### Open Source Contributor Grant
Significant open-source contributors may receive complimentary Standard Edition licenses.

## Feature Matrix by License Tier

| Feature | Community | Standard | Professional | Enterprise |
|---------|-----------|----------|--------------|------------|
| Source Code Access | ✓ | ✓ | ✓ | ✓ |
| Production Use | ✗ | ✓ | ✓ | ✓ |
| Max Capacity | N/A | 250 kW | 1 MW | Unlimited |
| Max Sites | 0 | 1 | 5 | Unlimited |
| Support SLA | None | 48h | 24h | 4h |
| Firmware Updates | Manual | Auto | Auto | Auto + Custom |
| Telemetry | Required | Required | Required | Optional |
| API Access | Read-only | Full | Full | Full + Custom |
| Custom Integration | ✗ | ✗ | Limited | Full |
| Modify Core Logic | ✗ | ✗ | ✗ | By Agreement |
| Redistribution | ✗ | ✗ | ✗ | By Agreement |
| White-labeling | ✗ | ✗ | ✗ | ✓ |
| Source Escrow | ✗ | ✗ | ✗ | ✓ |

## License Compliance

### Required Notices
All deployments must:
1. Retain copyright notices in source files
2. Include LICENSE file in distributions
3. Display license information in UI/documentation
4. Attribute third-party open-source components

### Audit Rights
- Commercial licensees agree to periodic license compliance audits
- Audit notice provided 30 days in advance
- Audits conducted remotely where possible

### Violations and Remediation
1. **First Violation:** Written notice, 30-day cure period
2. **Continued Violation:** License suspension, legal action
3. **Willful Violation:** Immediate termination, damages

## License Key Management

### Activation
- Licenses tied to deployment site identifier
- Requires online activation (offline activation available for remote sites)
- Hardware fingerprinting for license binding

### Transfer
- Standard/Professional licenses non-transferable without approval
- Enterprise licenses may include transfer rights
- Transfer fee may apply

### Renewal
- Annual renewals for Professional/Enterprise
- 90-day notice before expiration
- Grace period: 30 days

## How to Obtain a License

1. **Community Edition:** Download from GitHub, accept BUSL-1.1 terms
2. **Commercial Licenses:** Contact sales@maya-node.example.com
3. **Special Grants:** Apply at grants@maya-node.example.com

## Version-Specific Licensing

Each major version release may have different Change Dates and terms. Refer to the LICENSE file in the specific version tag.

## Contact

**Sales Inquiries:** sales@maya-node.example.com  
**License Support:** licensing@maya-node.example.com  
**Legal Questions:** legal@maya-node.example.com

---
*Last Updated: 2025-11-10*
*Document Version: 1.0*
