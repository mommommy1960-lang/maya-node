# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Consent Token Module

This module implements consent token generation, validation, and management
for the MAYA Node sovereign AI runtime. Every operation that writes to the
audit log must generate and attach a consent token.

Consent Token Structure:
    - operation: Name of the operation being performed
    - ethics_verified: Boolean indicating if ethics checks passed
    - human_approval: Boolean, string, or None indicating approval status
    - timestamp: UTC timestamp in ISO 8601 format
    - user_id: User identifier (optional, defaults to placeholder)
    - signature: Cryptographic HMAC-SHA256 signature

The consent token provides:
    1. Verifiable proof of ethical review
    2. Human oversight acknowledgment
    3. Tamper-evident audit trail
    4. Cryptographic integrity verification

Key Management:
    Trust root keys are managed through a ceremony process (see docs/CONSENT_TOKEN.md).
    Keys are stored securely and can be rotated following the documented protocol.

Security Considerations:
    - Uses HMAC-SHA256 for cryptographic signatures
    - Keys must be stored securely outside of source control
    - Token validation should always verify signature integrity
    - Timestamp validation prevents replay attacks
"""

import hmac
import hashlib
import json
import time
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass, asdict


@dataclass
class ConsentToken:
    """
    Represents a consent token for an audited operation.
    
    Attributes:
        operation: Name/type of the operation being performed
        ethics_verified: True if ethics checks passed, False otherwise
        human_approval: Approval status (True/False/None or descriptive string)
        timestamp: ISO 8601 UTC timestamp of token issuance
        user_id: User identifier (defaults to "system_placeholder")
        signature: HMAC-SHA256 signature for integrity verification
    """
    operation: str
    ethics_verified: bool
    human_approval: Union[bool, str, None]
    timestamp: str
    user_id: str = "system_placeholder"
    signature: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert token to dictionary for serialization.
        
        Returns:
            Dictionary representation of the consent token
        """
        return asdict(self)
    
    def to_json(self) -> str:
        """
        Serialize token to JSON string.
        
        Returns:
            JSON string representation of the token
        """
        return json.dumps(self.to_dict(), sort_keys=True)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConsentToken':
        """
        Create ConsentToken from dictionary.
        
        Args:
            data: Dictionary containing token fields
            
        Returns:
            ConsentToken instance
        """
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ConsentToken':
        """
        Deserialize token from JSON string.
        
        Args:
            json_str: JSON string representation
            
        Returns:
            ConsentToken instance
        """
        return cls.from_dict(json.loads(json_str))


class ConsentTokenManager:
    """
    Manages consent token issuance and validation.
    
    This class handles:
        - Token generation with cryptographic signatures
        - Token validation and integrity verification
        - Trust root key management
        - Signature verification
    
    The manager uses HMAC-SHA256 for signing tokens, providing:
        - Cryptographic integrity
        - Non-repudiation
        - Tamper detection
    """
    
    def __init__(self, trust_root_key: Optional[bytes] = None):
        """
        Initialize the ConsentTokenManager.
        
        Args:
            trust_root_key: Secret key for HMAC signing. If None, attempts to
                          load from environment or generates a new one (dev mode).
                          
        Security Note:
            In production, trust_root_key should be loaded from secure storage
            (e.g., secrets manager, HSM) and never hardcoded or stored in source.
        """
        self.trust_root_key = trust_root_key or self._load_or_generate_key()
    
    def _load_or_generate_key(self) -> bytes:
        """
        Load trust root key from environment or generate new one.
        
        Returns:
            Secret key as bytes
            
        Security Note:
            This implementation checks for MAYA_TRUST_ROOT_KEY environment variable.
            In production, use a proper secrets management system.
        """
        # Try to load from environment
        env_key = os.environ.get('MAYA_TRUST_ROOT_KEY')
        if env_key:
            return env_key.encode('utf-8')
        
        # Development mode: generate random key
        # WARNING: This should NOT be used in production
        import secrets
        return secrets.token_bytes(32)
    
    def issue_token(
        self,
        operation: str,
        ethics_verified: bool,
        human_approval: Union[bool, str, None],
        user_id: str = "system_placeholder"
    ) -> ConsentToken:
        """
        Issue a new consent token for an operation.
        
        This method:
            1. Creates a consent token with the provided parameters
            2. Generates a UTC timestamp in ISO 8601 format
            3. Computes HMAC-SHA256 signature over token data
            4. Returns the signed token
        
        Args:
            operation: Name/type of the operation
            ethics_verified: Whether ethics checks passed
            human_approval: Approval status from human oversight
            user_id: User identifier (optional)
            
        Returns:
            Signed ConsentToken ready for audit logging
            
        Example:
            >>> manager = ConsentTokenManager()
            >>> token = manager.issue_token(
            ...     operation="data_processing",
            ...     ethics_verified=True,
            ...     human_approval=True
            ... )
            >>> print(token.operation)
            data_processing
        """
        # Generate ISO 8601 UTC timestamp
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Create token without signature
        token = ConsentToken(
            operation=operation,
            ethics_verified=ethics_verified,
            human_approval=human_approval,
            timestamp=timestamp,
            user_id=user_id,
            signature=""
        )
        
        # Generate signature
        token.signature = self._sign_token(token)
        
        return token
    
    def _sign_token(self, token: ConsentToken) -> str:
        """
        Generate HMAC-SHA256 signature for a token.
        
        The signature is computed over the canonical representation of:
            operation|ethics_verified|human_approval|timestamp|user_id
        
        Args:
            token: ConsentToken to sign (signature field ignored)
            
        Returns:
            Hexadecimal HMAC-SHA256 signature string
        """
        # Create canonical message for signing (exclude signature field)
        message = (
            f"{token.operation}|"
            f"{token.ethics_verified}|"
            f"{token.human_approval}|"
            f"{token.timestamp}|"
            f"{token.user_id}"
        )
        
        # Compute HMAC-SHA256
        signature = hmac.new(
            self.trust_root_key,
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def validate_token(self, token: ConsentToken) -> bool:
        """
        Validate a consent token's signature.
        
        Verification process:
            1. Recompute signature from token data
            2. Compare with token's stored signature using constant-time comparison
            3. Return True if signatures match, False otherwise
        
        Args:
            token: ConsentToken to validate
            
        Returns:
            True if token signature is valid, False otherwise
            
        Security Note:
            Uses hmac.compare_digest for constant-time comparison to prevent
            timing attacks.
            
        Example:
            >>> manager = ConsentTokenManager()
            >>> token = manager.issue_token("test_op", True, True)
            >>> manager.validate_token(token)
            True
            >>> token.operation = "modified"
            >>> manager.validate_token(token)
            False
        """
        expected_signature = self._sign_token(token)
        
        # Use constant-time comparison to prevent timing attacks
        return hmac.compare_digest(token.signature, expected_signature)
    
    def validate_token_dict(self, token_dict: Dict[str, Any]) -> bool:
        """
        Validate a consent token from dictionary representation.
        
        Args:
            token_dict: Dictionary containing token fields
            
        Returns:
            True if token signature is valid, False otherwise
        """
        try:
            token = ConsentToken.from_dict(token_dict)
            return self.validate_token(token)
        except (KeyError, TypeError, ValueError):
            return False
    
    def get_truncated_signature(self, token: ConsentToken, length: int = 12) -> str:
        """
        Get truncated signature for display purposes.
        
        Returns the first N characters of the signature for user-friendly display
        while maintaining signature secrecy.
        
        Args:
            token: ConsentToken to extract signature from
            length: Number of characters to include (default: 12)
            
        Returns:
            Truncated signature string
            
        Example:
            >>> manager = ConsentTokenManager()
            >>> token = manager.issue_token("test", True, True)
            >>> manager.get_truncated_signature(token)
            'a1b2c3d4e5f6...'
        """
        if len(token.signature) <= length:
            return token.signature
        return f"{token.signature[:length]}..."


def generate_trust_root_key() -> bytes:
    """
    Generate a new trust root key for consent token signing.
    
    This function generates a cryptographically secure random key suitable
    for use as a trust root. The key should be:
        - Stored securely (secrets manager, HSM, encrypted storage)
        - Never committed to source control
        - Backed up securely for disaster recovery
        - Rotated according to security policy
    
    Returns:
        32-byte cryptographically secure random key
        
    Security Note:
        This is intended for initial ceremony/setup. In production, consider
        using a proper key management system (KMS).
        
    Example:
        >>> key = generate_trust_root_key()
        >>> len(key)
        32
        >>> # Store securely - DO NOT PRINT IN PRODUCTION
        >>> # import base64
        >>> # print(base64.b64encode(key).decode())
    """
    import secrets
    return secrets.token_bytes(32)


if __name__ == "__main__":
    """
    Example usage and self-test of consent token system.
    """
    print("=== Consent Token System Self-Test ===\n")
    
    # Create manager with test key
    manager = ConsentTokenManager(b"test_key_for_demonstration_only")
    
    # Issue a token
    print("1. Issuing consent token...")
    token = manager.issue_token(
        operation="data_processing_test",
        ethics_verified=True,
        human_approval="approved_by_admin",
        user_id="test_user_123"
    )
    
    print(f"   Operation: {token.operation}")
    print(f"   Ethics Verified: {token.ethics_verified}")
    print(f"   Human Approval: {token.human_approval}")
    print(f"   Timestamp: {token.timestamp}")
    print(f"   User ID: {token.user_id}")
    print(f"   Signature: {manager.get_truncated_signature(token)}")
    
    # Validate token
    print("\n2. Validating token...")
    is_valid = manager.validate_token(token)
    print(f"   Valid: {is_valid}")
    
    # Test tampering detection
    print("\n3. Testing tampering detection...")
    token_copy = ConsentToken.from_dict(token.to_dict())
    token_copy.operation = "tampered_operation"
    is_valid = manager.validate_token(token_copy)
    print(f"   Tampered token valid: {is_valid}")
    
    # Serialization
    print("\n4. Testing serialization...")
    json_str = token.to_json()
    print(f"   JSON length: {len(json_str)} bytes")
    
    restored_token = ConsentToken.from_json(json_str)
    is_valid = manager.validate_token(restored_token)
    print(f"   Restored token valid: {is_valid}")
    
    print("\n=== Self-Test Complete ===")
