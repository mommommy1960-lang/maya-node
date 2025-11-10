# MAYA Node - Compliance and Enforcement Policies

## Overview
This document defines compliance requirements, enforcement mechanisms, and monitoring policies for MAYA Node deployments.

## License Compliance

### Activation Requirements

#### Community Edition
- **Activation:** Optional but recommended
- **Telemetry:** Required (anonymized usage data)
- **Connectivity:** Online check every 72 hours
- **Restrictions:** Non-production use only

#### Standard Edition
- **Activation:** Required within 30 days of deployment
- **License Key:** Site-specific hardware-bound key
- **Telemetry:** Required (anonymized)
- **Connectivity:** Online check every 30 days
- **Offline Grace:** 30 days maximum

#### Professional Edition
- **Activation:** Required before production use
- **License Key:** Hardware-bound with optional HSM
- **Telemetry:** Required (can be anonymized)
- **Connectivity:** Online check every 90 days
- **Offline Grace:** 90 days with pre-approval

#### Enterprise Edition
- **Activation:** Custom process
- **License Key:** Optional air-gapped activation
- **Telemetry:** Configurable
- **Connectivity:** Optional
- **Offline Grace:** Unlimited with proper license

### Hardware Fingerprinting

License keys are bound to hardware characteristics:
- CPU serial number or UUID
- Network MAC addresses
- Storage device identifiers
- TPM chip (if available)

**Hardware Changes:**
- Minor changes (1-2 components): Automatic re-activation
- Major changes (motherboard/multiple): Requires license transfer request
- Virtual machines: Special licensing required

### License Transfer

#### Standard/Professional
- **Allowed:** With written approval
- **Process:** Submit transfer request via licensing portal
- **Fee:** 15% of original license value
- **Timeline:** 5 business days
- **Limit:** 1 transfer per year

#### Enterprise
- **Allowed:** Per agreement terms
- **Process:** Through account manager
- **Fee:** None or per agreement
- **Timeline:** Expedited processing

## Enforcement Mechanisms

### Technical Enforcement

#### License Validation
```python
# Performed at startup and periodically
1. Load license file from /etc/maya-node/license.json
2. Verify cryptographic signature
3. Check expiry date
4. Validate hardware fingerprint
5. Confirm capacity limits
6. Check online if connected
```

#### Feature Gating
- Core safety features: Always enabled
- Licensed features: Checked before execution
- Advanced features: Require valid license + feature flag
- API endpoints: License-tier restricted

#### Capacity Enforcement
- Monitor total system capacity (PV + storage + genset)
- Compare against license limit
- Soft limit warning at 90%
- Hard limit blocks deployment above licensed capacity
- Grace period: 7 days to upgrade license

#### Telemetry Requirements
- Community/Standard/Professional: Telemetry mandatory
- Enterprise: Configurable
- Data collected:
  - System capacity and utilization (anonymized)
  - Feature usage statistics
  - Error/fault logging
  - Performance metrics
  - No personally identifiable information
  - No site-specific location data (unless opted in)

### Operational Enforcement

#### Expired License Behavior

**Standard/Professional:**
- **Day 0 (Expiry):** Warning displayed, full functionality maintained
- **Days 1-30 (Grace Period):** 
  - Daily warning notifications
  - Email to license admin
  - Reduced telemetry upload frequency
  - Full functionality maintained
- **Day 31+:**
  - Core safety features only
  - No dispatch optimization
  - No remote access
  - Local HMI displays renewal notice
  - System runs in safe fallback mode

**Enterprise:**
- Custom grace period per agreement
- Coordinated with account manager
- Typically 90 days

#### Capacity Violations

**Over-Capacity Deployment:**
1. **Detection:** System capacity exceeds license limit
2. **Warning Phase (7 days):**
   - Warning displayed on HMI
   - Email notifications sent
   - Option to upgrade license presented
3. **Enforcement:**
   - If not resolved: System limits output to licensed capacity
   - P3 loads automatically shed
   - P2 loads limited if necessary
   - P1 (critical) loads always maintained

**Resolution:**
- Upgrade license to higher tier
- Reduce system capacity
- Add additional site license

#### Multi-Site Violations

**Detecting Unauthorized Sites:**
- License keys include site identifier
- Hardware fingerprint mismatch triggers alert
- Telemetry data cross-referenced with site ID

**Enforcement:**
1. Automated detection via telemetry
2. Investigation by compliance team
3. Contact license holder
4. 30-day cure period
5. If unresolved: License suspension, legal action

### Audit Process

#### Regular Audits
- Professional: Annual compliance review
- Enterprise: Per agreement (typically annual)
- Scope:
  - Deployment capacity verification
  - Site count confirmation
  - Feature usage review
  - License transfer history

#### Audit Procedure
1. **Notice:** 30-day advance notice (90 days for international)
2. **Information Request:**
   - Current deployment configuration
   - System capacity documentation
   - List of all sites with license IDs
3. **Review:** Remote review of telemetry data and documentation
4. **Site Visit:** Optional, for discrepancies or high-value deployments
5. **Report:** Audit findings within 30 days
6. **Remediation:** 60-day cure period for violations

#### Audit Rights
- Licensee agrees to cooperate with reasonable audit requests
- Access to deployment telemetry data
- Access to configuration documentation
- Right to inspect physical deployment (with notice)

### Violation Categories and Remediation

#### Category 1: Administrative Violations
**Examples:**
- Expired license during grace period
- Missing documentation
- Telemetry connectivity issues

**Remediation:**
- Notice sent
- 30-day cure period
- License renewal or documentation update
- No penalties for first occurrence

#### Category 2: Capacity Violations
**Examples:**
- Deployment exceeds licensed capacity
- Unauthorized feature usage
- Site count exceeds license

**Remediation:**
- Notice and explanation
- 30-day cure period
- License upgrade required
- True-up fees may apply
- Repeated violations: License suspension

#### Category 3: Material Violations
**Examples:**
- Unauthorized production use (Community license)
- License key sharing between sites
- Intentional circumvention of license checks
- Removal of license enforcement code

**Remediation:**
- Immediate notice
- 15-day cure period
- License termination
- Legal action
- Liquidated damages per agreement

#### Category 4: Willful Violations
**Examples:**
- Intentional license key generation/forgery
- Distribution of cracked software
- Commercial redistribution without OEM rights
- Trade secret theft

**Remediation:**
- Immediate license termination
- No cure period
- Legal action: injunction + damages
- Criminal referral if applicable

## Monitoring and Detection

### Automated Monitoring
- License expiry tracking
- Capacity utilization monitoring
- Feature usage analytics
- Telemetry health checks
- Anomaly detection (e.g., duplicate site IDs)

### Compliance Dashboard
Available to licensees at portal.maya-node.example.com:
- License status and expiry
- Current capacity vs. limit
- Active features
- Compliance status
- Renewal options

### Alerts and Notifications

#### Licensee Notifications
- 90 days before expiry
- 60 days before expiry
- 30 days before expiry
- Weekly during grace period
- Capacity warnings at 90%, 95%, 100%

#### Internal Notifications
- Compliance team alerted on violations
- Sales team notified of upcoming renewals
- Engineering notified of technical enforcement issues

## Data Privacy and Security

### Telemetry Data
- **Collection:** Automated, encrypted transmission
- **Storage:** Secure cloud database, encrypted at rest
- **Retention:** 2 years operational data, 7 years compliance records
- **Access:** Restricted to authorized personnel
- **Usage:** Compliance monitoring, product improvement, support
- **Privacy:** GDPR, CCPA, and regional privacy law compliant

### Data Subject Rights
- Right to access telemetry data
- Right to request data deletion (with license termination)
- Right to opt-out (Enterprise licenses only)
- Right to data portability

### License Key Security
- Cryptographically signed license files
- Private keys secured in HSM
- Regular key rotation
- Separate signing keys per major version

## Compliance Support

### Self-Service Tools
- License portal: portal.maya-node.example.com
- Capacity calculator
- License upgrade wizard
- Renewal automation
- Audit report generation

### Support Contacts
- **General Compliance:** compliance@maya-node.example.com
- **Audit Inquiries:** audit@maya-node.example.com
- **License Renewal:** renewals@maya-node.example.com
- **Technical Issues:** support@maya-node.example.com

### Voluntary Disclosure
Licensees who discover and self-report compliance issues receive:
- Extended cure period (60 days vs. 30)
- Waived late fees for first occurrence
- Prioritized resolution support
- No penalties if resolved within cure period

## Legal Framework

### Governing Terms
- Master License Agreement (MLA)
- Terms of Service
- Privacy Policy
- Export Control Compliance

### Jurisdiction
- Governed by laws of [jurisdiction TBD]
- Disputes resolved via arbitration per MLA
- Exceptions: injunctive relief, IP infringement

### Limitation of Liability
- License enforcement does not create warranty
- Compliance violations may void warranty
- Limitation of liability per MLA applies

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-10 | Initial enforcement policy document |

---
*Last Updated: 2025-11-10*
*Document Classification: Public*
*Applies to: MAYA Node v1.0 and later*
