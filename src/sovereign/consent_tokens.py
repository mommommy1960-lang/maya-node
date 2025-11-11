# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Consent Token Signing Process

This module implements the consent token system for explicit user authorization
of AI operations. All operations requiring consent must be signed and verified.

Key Features:
- Cryptographic token generation and signing
- User consent verification
- Expiration and revocation support
- Audit trail integration
"""

import hashlib
import hmac
import json
import time
import secrets
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum

import logging

logger = logging.getLogger(__name__)


class ConsentScope(Enum):
    """Scope of consent granted"""
    SINGLE_OPERATION = "single_operation"
    SESSION = "session"
    BATCH = "batch"


class ConsentStatus(Enum):
    """Status of a consent token"""
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    USED = "used"


@dataclass
class ConsentToken:
    """Consent token with cryptographic signature"""
    token_id: str
    user_id: str
    operation: str
    scope: ConsentScope
    timestamp: float
    expires_at: float
    signature: str
    metadata: Dict[str, Any]
    status: ConsentStatus = ConsentStatus.ACTIVE
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['scope'] = self.scope.value
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConsentToken':
        """Create from dictionary"""
        data['scope'] = ConsentScope(data['scope'])
        data['status'] = ConsentStatus(data['status'])
        return cls(**data)


class ConsentTokenManager:
    """
    Manages consent token generation, signing, and verification.
    
    This system ensures that all sensitive operations require explicit
    user consent with cryptographic verification.
    """
    
    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize the consent token manager.
        
        Args:
            secret_key: Secret key for signing (generates random if None)
        """
        # In production, this should come from secure storage
        self.secret_key = secret_key or secrets.token_hex(32)
        self.tokens = {}  # token_id -> ConsentToken
        logger.info("ConsentTokenManager initialized")
    
    def generate_token(
        self,
        user_id: str,
        operation: str,
        scope: ConsentScope = ConsentScope.SINGLE_OPERATION,
        ttl_seconds: int = 300,  # 5 minutes default
        metadata: Optional[Dict[str, Any]] = None
    ) -> ConsentToken:
        """
        Generate a new consent token.
        
        Args:
            user_id: User granting consent
            operation: Operation requiring consent
            scope: Scope of consent
            ttl_seconds: Time to live in seconds
            metadata: Additional metadata
            
        Returns:
            Signed consent token
        """
        token_id = secrets.token_hex(16)
        timestamp = time.time()
        expires_at = timestamp + ttl_seconds
        
        # Build token data
        token_data = {
            'token_id': token_id,
            'user_id': user_id,
            'operation': operation,
            'scope': scope.value,
            'timestamp': timestamp,
            'expires_at': expires_at,
            'metadata': metadata or {}
        }
        
        # Sign the token
        signature = self._sign_token(token_data)
        
        token = ConsentToken(
            token_id=token_id,
            user_id=user_id,
            operation=operation,
            scope=scope,
            timestamp=timestamp,
            expires_at=expires_at,
            signature=signature,
            metadata=metadata or {},
            status=ConsentStatus.ACTIVE
        )
        
        self.tokens[token_id] = token
        logger.info(f"Consent token generated: {token_id} for user {user_id} operation {operation}")
        
        return token
    
    def _sign_token(self, token_data: Dict[str, Any]) -> str:
        """
        Generate cryptographic signature for token data.
        
        Args:
            token_data: Token data to sign
            
        Returns:
            HMAC signature hex string
        """
        # Create canonical representation
        canonical = json.dumps(token_data, sort_keys=True)
        
        # Generate HMAC-SHA256 signature
        signature = hmac.new(
            self.secret_key.encode(),
            canonical.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def verify_token(self, token: ConsentToken) -> bool:
        """
        Verify a consent token's signature and status.
        
        Args:
            token: Token to verify
            
        Returns:
            True if token is valid
        """
        # Check if token exists
        if token.token_id not in self.tokens:
            logger.warning(f"Token not found: {token.token_id}")
            return False
        
        stored_token = self.tokens[token.token_id]
        
        # Check signature
        token_data = {
            'token_id': token.token_id,
            'user_id': token.user_id,
            'operation': token.operation,
            'scope': token.scope.value,
            'timestamp': token.timestamp,
            'expires_at': token.expires_at,
            'metadata': token.metadata
        }
        
        expected_signature = self._sign_token(token_data)
        if token.signature != expected_signature:
            logger.error(f"Token signature mismatch: {token.token_id}")
            return False
        
        # Check expiration
        if time.time() > token.expires_at:
            logger.warning(f"Token expired: {token.token_id}")
            stored_token.status = ConsentStatus.EXPIRED
            return False
        
        # Check status
        if stored_token.status != ConsentStatus.ACTIVE:
            logger.warning(f"Token not active: {token.token_id} (status: {stored_token.status.value})")
            return False
        
        logger.info(f"Token verified: {token.token_id}")
        return True
    
    def use_token(self, token_id: str) -> bool:
        """
        Use/consume a token (for single-use tokens).
        
        Args:
            token_id: Token to consume
            
        Returns:
            True if token was successfully used
        """
        if token_id not in self.tokens:
            logger.error(f"Token not found: {token_id}")
            return False
        
        token = self.tokens[token_id]
        
        if not self.verify_token(token):
            return False
        
        # For single operation tokens, mark as used
        if token.scope == ConsentScope.SINGLE_OPERATION:
            token.status = ConsentStatus.USED
            logger.info(f"Token used: {token_id}")
        
        return True
    
    def revoke_token(self, token_id: str) -> bool:
        """
        Revoke a consent token.
        
        Args:
            token_id: Token to revoke
            
        Returns:
            True if token was revoked
        """
        if token_id not in self.tokens:
            logger.error(f"Token not found: {token_id}")
            return False
        
        token = self.tokens[token_id]
        token.status = ConsentStatus.REVOKED
        logger.info(f"Token revoked: {token_id}")
        
        return True
    
    def get_token(self, token_id: str) -> Optional[ConsentToken]:
        """
        Get a token by ID.
        
        Args:
            token_id: Token ID
            
        Returns:
            Token if found, None otherwise
        """
        return self.tokens.get(token_id)
    
    def get_user_tokens(self, user_id: str) -> list[ConsentToken]:
        """
        Get all tokens for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of tokens for the user
        """
        return [
            token for token in self.tokens.values()
            if token.user_id == user_id
        ]


def main():
    """Example usage of consent tokens."""
    
    manager = ConsentTokenManager()
    
    # Generate a token
    token = manager.generate_token(
        user_id="user123",
        operation="process_sensitive_data",
        scope=ConsentScope.SINGLE_OPERATION,
        ttl_seconds=300,
        metadata={"reason": "data analysis"}
    )
    
    print(f"Generated token: {token.token_id}")
    print(f"Signature: {token.signature[:16]}...")
    
    # Verify the token
    is_valid = manager.verify_token(token)
    print(f"Token valid: {is_valid}")
    
    # Use the token
    success = manager.use_token(token.token_id)
    print(f"Token used: {success}")
    
    # Try to use again (should fail for single-use)
    success = manager.use_token(token.token_id)
    print(f"Token reused: {success}")
    
    # Test revocation
    token2 = manager.generate_token(
        user_id="user123",
        operation="another_operation",
        scope=ConsentScope.SESSION
    )
    
    manager.revoke_token(token2.token_id)
    is_valid = manager.verify_token(token2)
    print(f"Revoked token valid: {is_valid}")


if __name__ == "__main__":
    main()
