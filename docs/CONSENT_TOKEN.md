# Consent Token System

## Overview

The Consent Token system provides cryptographically-signed proof of ethical review and human oversight for every operation in the MAYA Node sovereign AI runtime. Each operation that writes to the audit log must generate and attach a consent token, creating a tamper-evident audit trail.

## Purpose and Goals

The consent token system ensures:

1. **Ethical Verification**: Every operation undergoes ethics checks before execution
2. **Human Oversight**: Human approval status is recorded and verifiable
3. **Cryptographic Integrity**: Tokens are signed using HMAC-SHA256 for tamper detection
4. **Audit Trail**: All operations are logged with verifiable consent tokens
5. **Accountability**: User IDs and timestamps provide clear attribution
6. **Transparency**: Token structure is human-readable and inspectable

## Token Structure

A consent token is a JSON object containing the following fields:

```json
{
  "operation": "string - name/type of the operation",
  "ethics_verified": "boolean - true if ethics checks passed",
  "human_approval": "boolean|string|null - approval status",
  "timestamp": "string - ISO 8601 UTC timestamp",
  "user_id": "string - user identifier",
  "signature": "string - HMAC-SHA256 signature (hex)"
}
```

### Field Descriptions

#### `operation` (required, string)
The name or type of the operation being performed. Examples:
- `"process_input"` - Processing user input through the runtime
- `"runtime_init"` - Initializing the runtime environment
- `"data_write"` - Writing data to storage
- `"model_load"` - Loading an AI model

#### `ethics_verified` (required, boolean)
Indicates whether the operation passed ethics verification checks. 

- `true`: All ethics constraints were satisfied
- `false`: Ethics checks failed or were not performed

The ethics verification process examines operations against predefined ethical constraints (see `ethics_engine.py`) including:
- Prohibited use patterns (weaponization, surveillance, harm)
- Content safety requirements
- Transparency obligations
- Human rights considerations

#### `human_approval` (required, boolean|string|null)
Records the human oversight status for this operation.

Possible values:
- `true`: Human explicitly approved the operation
- `false`: No human approval obtained (but may not be required)
- `null`: Human approval status unknown or not applicable
- `"approved_by_admin"`: Descriptive string indicating approval source
- `"auto_approved_dev"`: Auto-approved in development mode

The system can require human approval for sensitive operations while allowing routine operations to proceed without manual intervention.

#### `timestamp` (required, string)
ISO 8601 formatted UTC timestamp of when the token was issued.

Format: `YYYY-MM-DDTHH:MM:SS.ssssss+00:00`

Example: `"2025-11-12T03:45:30.123456+00:00"`

The timestamp serves multiple purposes:
- Provides temporal ordering of operations
- Enables time-based audit queries
- Helps prevent replay attacks
- Documents when consent was granted

#### `user_id` (required, string)
Identifier of the user or system component that initiated the operation.

Examples:
- `"user_alice"` - Named user account
- `"system"` - System-initiated operation
- `"system_placeholder"` - Default value before identity integration
- `"admin_bob"` - Administrative user

User IDs are currently placeholders. Full identity integration will tie user IDs to cryptographic identities established during the trust ceremony (see section on Identity Integration below).

#### `signature` (required, string)
HMAC-SHA256 signature of the token data, providing cryptographic integrity.

Format: 64-character hexadecimal string

Example: `"a1b2c3d4e5f6...789"`

The signature is computed over the canonical representation:
```
operation|ethics_verified|human_approval|timestamp|user_id
```

This ensures that any modification to the token can be detected through signature verification.

## Token Issuance

### Process Flow

1. **Operation Initiation**: An operation is about to be performed
2. **Ethics Verification**: The operation is checked against ethics constraints
3. **Human Approval Check**: If required, human approval is obtained
4. **Token Generation**: A consent token is issued with:
   - Operation name
   - Ethics verification result
   - Human approval status
   - Current UTC timestamp
   - User identifier
5. **Signature Computation**: HMAC-SHA256 signature is generated using the trust root key
6. **Token Attachment**: Token is attached to the audit log entry
7. **Persistence**: Entry with token is written to append-only audit log

### Code Example

```python
from sovereign.consent_token import ConsentTokenManager

# Initialize the token manager with trust root key
manager = ConsentTokenManager(trust_root_key)

# Issue a token for an operation
token = manager.issue_token(
    operation="data_processing",
    ethics_verified=True,
    human_approval=True,
    user_id="user_alice"
)

# Token is now ready to be logged
print(f"Token issued: {token.to_json()}")
```

### CLI Usage

The CLI automatically generates consent tokens for all operations:

```bash
# Initialize runtime (creates consent token)
python src/cli.py init

# Process input (creates consent token)
python src/cli.py process --input "optimize energy distribution"

# View audit log with consent tokens
python src/cli.py audit --limit 10
```

## Token Verification

### Verification Process

Token verification ensures:
1. **Signature Validity**: The signature matches the token data
2. **Data Integrity**: No fields have been tampered with
3. **Key Consistency**: The correct trust root key was used

### Code Example

```python
from sovereign.consent_token import ConsentTokenManager, ConsentToken

# Load token from audit log
token_dict = {"operation": "...", "signature": "...", ...}
token = ConsentToken.from_dict(token_dict)

# Verify the token
manager = ConsentTokenManager(trust_root_key)
is_valid = manager.validate_token(token)

if is_valid:
    print("✓ Token is valid")
else:
    print("✗ Token is INVALID - possible tampering detected")
```

### CLI Usage

```bash
# Verify all consent tokens and hash chain
python src/cli.py verify --detailed
```

The verify command checks:
- Hash chain integrity of the audit log
- Signature validity of all consent tokens
- Sequential entry ID consistency

## Trust Root Key Management

The trust root key is the secret key used to sign consent tokens. Proper key management is critical for system security.

### Key Properties

- **Algorithm**: HMAC-SHA256
- **Length**: 256 bits (32 bytes)
- **Format**: Binary (stored as base64 for transport/storage)
- **Generation**: Cryptographically secure random number generator

### Key Generation Ceremony

The initial trust root key should be generated in a secure ceremony:

#### 1. Generate the Key

```bash
python src/cli.py keygen --output /secure/path/trust_root.key
```

This creates a cryptographically secure 256-bit key.

#### 2. Record Key Metadata

Document:
- Date and time of generation
- Ceremony participants (if applicable)
- Key fingerprint (first 12 characters of base64)
- Intended use (production, staging, development)
- Rotation schedule

#### 3. Secure Storage

Store the key using one of these methods:

**Option A: Filesystem (Development)**
```bash
# Store with restricted permissions
chmod 600 /secure/path/trust_root.key

# Set environment variable
export MAYA_TRUST_ROOT_KEY=$(cat /secure/path/trust_root.key)
```

**Option B: Environment Variable**
```bash
export MAYA_TRUST_ROOT_KEY='<base64-encoded-key>'
```

**Option C: Secrets Manager (Production)**
- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault
- Google Secret Manager

Load key at runtime:
```python
import boto3

# Example: AWS Secrets Manager
secrets_client = boto3.client('secretsmanager')
response = secrets_client.get_secret_value(SecretId='maya/trust-root-key')
key = base64.b64decode(response['SecretString'])

manager = ConsentTokenManager(key)
```

**Option D: Hardware Security Module (High Security)**
- Use HSM for key storage and signing operations
- Keys never leave the HSM
- Provides additional physical security

#### 4. Backup the Key

Create secure backups:
- Encrypted backup files
- Offline storage (air-gapped)
- Geographic redundancy
- Split key custody (Shamir's Secret Sharing)

#### 5. Document the Ceremony

Create a ceremony report including:
- Participants and roles
- Key generation method
- Storage location(s)
- Backup procedures
- Recovery procedures
- First use timestamp

### Key Storage Best Practices

**DO:**
- ✓ Store keys in secrets management systems
- ✓ Use filesystem permissions (600) for file storage
- ✓ Encrypt keys at rest
- ✓ Use environment variables for runtime loading
- ✓ Document key locations and procedures
- ✓ Create secure backups
- ✓ Limit access to need-to-know basis
- ✓ Log all key access attempts
- ✓ Use different keys for dev/staging/production

**DON'T:**
- ✗ Never commit keys to source control
- ✗ Never log keys (even truncated versions)
- ✗ Never send keys over insecure channels
- ✗ Never hardcode keys in source code
- ✗ Never share keys via email or chat
- ✗ Never store keys in plain text without permissions
- ✗ Never use the same key across environments
- ✗ Never skip key backups

### Key Rotation Protocol

Regular key rotation is a security best practice. The rotation process requires coordination between key issuance and verification.

#### When to Rotate

Rotate keys:
- On a regular schedule (e.g., every 90 days)
- After a security incident
- After team member departure
- When key may have been compromised
- During security audits

#### Rotation Process

**1. Generate New Key**
```bash
python src/cli.py keygen --output /secure/path/trust_root_new.key
```

**2. Update Key Store**

Update the secrets manager or environment variable with the new key.

**3. Transition Period**

During rotation, you need to support both old and new keys for verification of historical audit logs.

Strategy 1: Version Keys
```python
class VersionedConsentTokenManager:
    def __init__(self):
        self.keys = {
            'v1': load_key('trust_root_v1.key'),  # Historical
            'v2': load_key('trust_root_v2.key'),  # Current
        }
        self.current_version = 'v2'
    
    def issue_token(self, ...):
        # Always use current version for new tokens
        return issue_with_key(self.keys[self.current_version], ...)
    
    def validate_token(self, token):
        # Try all keys for verification
        for key in self.keys.values():
            if verify_with_key(key, token):
                return True
        return False
```

Strategy 2: Dated Keys
```python
# Store keys with effective dates
keys = {
    '2025-01-01': key_v1,  # Used before this date
    '2025-04-01': key_v2,  # Used after this date
}

def get_key_for_timestamp(timestamp):
    # Select appropriate key based on token timestamp
    ...
```

**4. Archive Old Key**

After all active systems use the new key:
- Archive the old key securely
- Retain for verification of historical audit logs
- Document the rotation in the key registry

**5. Verify Rotation**

- Confirm new operations use new key
- Test verification of old and new tokens
- Update documentation

#### Emergency Rotation

If a key is compromised:

1. **Immediate Actions**
   - Generate new key immediately
   - Update all production systems
   - Revoke compromised key
   - Document the incident

2. **Audit Review**
   - Review audit logs for suspicious activity
   - Verify integrity of existing entries
   - Flag potentially compromised operations

3. **Investigation**
   - Determine scope of compromise
   - Identify affected systems
   - Assess potential impact

4. **Communication**
   - Notify stakeholders
   - Document timeline
   - Plan remediation

## Audit Log Integration

Consent tokens are integrated with the append-only audit log system.

### Audit Log Structure

Each line in `audit.jsonl` is a JSON object:

```json
{
  "entry_id": 1,
  "timestamp": "2025-11-12T03:45:30.123456+00:00",
  "operation": "process_input",
  "data": {
    "input": "user input data",
    "result": "processing result"
  },
  "consent_token": {
    "operation": "process_input",
    "ethics_verified": true,
    "human_approval": false,
    "timestamp": "2025-11-12T03:45:30.123456+00:00",
    "user_id": "user_alice",
    "signature": "a1b2c3d4..."
  },
  "previous_hash": "0123456789abcdef...",
  "entry_hash": "fedcba9876543210..."
}
```

### Integrity Verification

The audit log provides dual integrity guarantees:

1. **Hash Chain**: Each entry links to the previous via hash
2. **Consent Tokens**: Each entry's consent token is cryptographically signed

To tamper with the log, an attacker would need:
- The trust root key (to forge consent token signatures)
- The ability to recompute all subsequent hashes (hash chain)

This makes the audit log tamper-evident and provides strong integrity guarantees.

### Append-Only Guarantee

The audit log system enforces append-only semantics:
- No update operations
- No delete operations
- Only append operations
- File locking prevents concurrent corruption
- `fsync()` ensures durability

Implementation:
```python
# Append to audit log with file locking
with open(log_file, 'a') as f:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    try:
        f.write(entry_json + '\n')
        f.flush()
        os.fsync(f.fileno())
    finally:
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
```

## Identity Integration (Future)

The current implementation uses placeholder user IDs. Full identity integration will tie user IDs to cryptographic identities.

### Planned Identity System

**Public Key Infrastructure (PKI)**
- Each user has a keypair
- User ID is derived from public key
- Operations are signed with user's private key
- Consent tokens include user signature

**Trust Ceremony Extensions**
- User enrollment process
- Key distribution
- Revocation protocol
- Identity verification

**Example Enhanced Token**
```json
{
  "operation": "process_input",
  "ethics_verified": true,
  "human_approval": true,
  "timestamp": "2025-11-12T03:45:30.123456+00:00",
  "user_id": "alice@example.com",
  "user_pubkey_fingerprint": "SHA256:abc123...",
  "user_signature": "user_sig_here...",
  "system_signature": "system_sig_here..."
}
```

This provides:
- User non-repudiation
- System accountability
- Dual signature verification

## Security Considerations

### Threat Model

**Threats Addressed:**
- ✓ Unauthorized operations (ethics verification required)
- ✓ Audit log tampering (hash chain + signatures)
- ✓ Consent token forgery (cryptographic signatures)
- ✓ Replay attacks (timestamps + hash chain)
- ✓ System compromise (append-only semantics)

**Threats Not Addressed:**
- ✗ Key compromise (requires key rotation)
- ✗ Root access to log file (requires OS-level protection)
- ✗ Social engineering (requires human vigilance)
- ✗ Side-channel attacks (requires physical security)

### Best Practices

1. **Key Management**: Follow trust root key management procedures
2. **Regular Audits**: Review audit logs frequently
3. **Integrity Checks**: Run `verify` command regularly
4. **Access Control**: Limit access to audit logs and keys
5. **Monitoring**: Alert on verification failures
6. **Backups**: Maintain secure backups of audit logs
7. **Separation of Duties**: Different people for different roles
8. **Security Updates**: Keep dependencies updated

### Monitoring and Alerting

Set up monitoring for:
- Consent token verification failures
- Hash chain breaks
- Unusual operation patterns
- Repeated ethics violations
- Key access attempts
- Audit log growth anomalies

Example monitoring:
```bash
# Cron job to verify integrity
0 */6 * * * /path/to/maya/src/cli.py verify --detailed || alert_admin.sh
```

## CLI Reference

### Commands

```bash
# Initialize runtime environment
python src/cli.py init [--data-dir PATH]

# Process input through runtime
python src/cli.py process [--input TEXT] [--require-approval]

# View audit log entries
python src/cli.py audit [--operation TYPE] [--limit N] [--verbose]

# Verify audit log integrity
python src/cli.py verify [--detailed]

# Generate trust root key
python src/cli.py keygen [--output PATH]
```

### Environment Variables

- `MAYA_DATA_DIR`: Data directory (default: `~/.maya`)
- `MAYA_TRUST_ROOT_KEY`: Trust root key (base64 encoded)

### Examples

```bash
# Complete workflow
python src/cli.py keygen --output ~/.maya/trust_root.key
python src/cli.py init
python src/cli.py process --input "optimize energy distribution"
python src/cli.py audit --limit 10
python src/cli.py verify

# Using environment variable
export MAYA_TRUST_ROOT_KEY='iYmZj2TGaazmwxkLJ6Y5HriY+H8Li1/YaYOWi+4D/QI='
python src/cli.py init

# Different data directory
python src/cli.py --data-dir /var/maya process --input "test"
```

## API Reference

See source code for detailed API documentation:
- `src/sovereign/consent_token.py` - Token generation and validation
- `src/sovereign/audit_log.py` - Audit log management
- `src/cli.py` - Command-line interface

## Troubleshooting

### Invalid Consent Tokens

**Problem**: `verify` command reports invalid tokens

**Causes**:
- Wrong trust root key being used
- Key file changed after tokens were issued
- Genesis entry created with different key

**Solution**:
1. Ensure consistent key usage across all operations
2. Use the same key for verification that was used for issuance
3. For genesis entries created during development, accept them as invalid or regenerate the audit log

### Hash Chain Broken

**Problem**: Hash chain verification fails

**Causes**:
- Audit log file was manually edited
- Concurrent writes without proper locking
- File corruption

**Solution**:
1. Restore from backup
2. Investigate what caused the break
3. If entries were added out of order, this is expected - audit log must be strictly sequential

### Key Not Found

**Problem**: CLI can't find trust root key

**Causes**:
- Key file doesn't exist
- Wrong path in environment variable
- Permissions issue

**Solution**:
1. Generate key: `python src/cli.py keygen --output ~/.maya/trust_root.key`
2. Check environment: `echo $MAYA_TRUST_ROOT_KEY`
3. Check file permissions: `ls -l ~/.maya/trust_root.key` (should be `-rw-------`)

## Compliance and Auditing

The consent token system supports compliance requirements:

### Audit Trail Requirements
- ✓ Every operation is logged
- ✓ Timestamps are immutable
- ✓ User attribution is recorded
- ✓ Ethics verification is documented
- ✓ Tamper detection is provided

### Regulatory Compliance
- GDPR: Documented consent and processing basis
- HIPAA: Audit trail for PHI access
- SOC 2: System monitoring and logging
- ISO 27001: Access control and accountability

### Audit Reports

Generate audit reports:
```bash
# Export audit log
python src/cli.py audit --verbose > audit_report.json

# Filter by operation
python src/cli.py audit --operation process_input > processing_audit.json

# Verify integrity
python src/cli.py verify --detailed > integrity_report.txt
```

## Future Enhancements

Planned improvements:
1. User identity integration (PKI)
2. Multi-signature support (multiple approvers)
3. Time-based access control
4. Automated compliance reporting
5. Blockchain anchoring (for high-value audits)
6. Hardware security module (HSM) integration
7. Distributed audit log replication
8. Machine-readable audit queries
9. Integration with SIEM systems
10. Grafana dashboards for monitoring

## References

- HMAC-SHA256: [RFC 2104](https://tools.ietf.org/html/rfc2104)
- ISO 8601 Timestamps: [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
- JSONL Format: [JSON Lines](https://jsonlines.org/)
- Ethics Engine: `src/sovereign/ethics_engine.py`
- Runtime System: `src/sovereign/runtime.py`

## Support

For questions or issues:
- Review source code documentation
- Check troubleshooting section above
- Review existing audit logs for examples
- Consult security team for key management questions

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-12  
**License**: CERL-1.0
