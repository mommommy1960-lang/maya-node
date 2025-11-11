# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Runtime Bridge - Phase Omega Integration

This module bridges the sovereign runtime with ledger, consent tokens,
and TPM attestation for Phase Omega system scale.

Key Features:
- Runtime-to-ledger audit integration
- Consent token requirement enforcement
- TPM attestation verification
- Enhanced security and oversight
"""

import logging
import time
from typing import Any, Dict, Optional
from dataclasses import dataclass

from .runtime import SovereignRuntime, RuntimeConfig, RuntimeState
from .consent_tokens import ConsentTokenManager, ConsentToken, ConsentScope
from .tpm_attestation import TPMAttestationStub, AttestationStatus
from ..services.ledger.ledger import ImmutableLedger

logger = logging.getLogger(__name__)


@dataclass
class BridgeConfig:
    """Configuration for runtime bridge"""
    require_consent: bool = True
    require_attestation: bool = False  # Set to True when TPM available
    ledger_enabled: bool = True


class RuntimeBridge:
    """
    Bridges sovereign runtime with security and audit systems.
    
    Phase Omega integration connecting:
    - Runtime operations to immutable ledger
    - Consent token verification
    - TPM attestation checks
    """
    
    def __init__(
        self,
        runtime_config: Optional[RuntimeConfig] = None,
        bridge_config: Optional[BridgeConfig] = None
    ):
        """
        Initialize the runtime bridge.
        
        Args:
            runtime_config: Runtime configuration
            bridge_config: Bridge configuration
        """
        self.runtime = SovereignRuntime(runtime_config)
        self.config = bridge_config or BridgeConfig()
        
        # Initialize subsystems
        self.ledger = ImmutableLedger() if self.config.ledger_enabled else None
        self.consent_manager = ConsentTokenManager() if self.config.require_consent else None
        self.attestation = TPMAttestationStub() if self.config.require_attestation else None
        
        logger.info("RuntimeBridge initialized")
        logger.info(f"  Ledger: {'enabled' if self.ledger else 'disabled'}")
        logger.info(f"  Consent tokens: {'required' if self.consent_manager else 'disabled'}")
        logger.info(f"  TPM attestation: {'required' if self.attestation else 'disabled'}")
        
        # Log initialization to ledger
        if self.ledger:
            self.ledger.append("runtime_bridge_init", {
                "timestamp": time.time(),
                "consent_required": self.config.require_consent,
                "attestation_required": self.config.require_attestation
            })
    
    def execute_with_consent(
        self,
        user_id: str,
        operation: str,
        input_data: Dict[str, Any],
        consent_token: Optional[ConsentToken] = None
    ) -> Dict[str, Any]:
        """
        Execute operation with consent token verification.
        
        Args:
            user_id: User ID executing the operation
            operation: Operation name
            input_data: Operation input data
            consent_token: Consent token (if already generated)
            
        Returns:
            Operation result
            
        Raises:
            RuntimeError: If consent verification fails
        """
        logger.info(f"Execute with consent: {operation} by user {user_id}")
        
        # Verify consent token if required
        if self.config.require_consent:
            if not consent_token:
                raise RuntimeError("Consent token required but not provided")
            
            if not self.consent_manager.verify_token(consent_token):
                raise RuntimeError("Invalid or expired consent token")
            
            # Check token matches operation
            if consent_token.operation != operation:
                raise RuntimeError(f"Token operation mismatch: expected {operation}, got {consent_token.operation}")
            
            logger.info(f"Consent verified: token {consent_token.token_id}")
        
        # Verify platform attestation if required
        if self.config.require_attestation:
            attestation_result = self.attestation.verify_platform_integrity()
            if attestation_result.status == AttestationStatus.FAILED:
                raise RuntimeError(f"Platform attestation failed: {attestation_result.notes}")
            
            logger.info(f"Attestation status: {attestation_result.status.value}")
        
        # Log operation start to ledger
        if self.ledger:
            self.ledger.append("operation_start", {
                "user_id": user_id,
                "operation": operation,
                "consent_token_id": consent_token.token_id if consent_token else None,
                "timestamp": time.time()
            })
        
        try:
            # Execute through runtime
            result = self.runtime.process(input_data)
            
            # Mark consent token as used if single-use
            if consent_token and self.consent_manager:
                self.consent_manager.use_token(consent_token.token_id)
            
            # Log success to ledger
            if self.ledger:
                self.ledger.append("operation_complete", {
                    "user_id": user_id,
                    "operation": operation,
                    "status": "success",
                    "timestamp": time.time()
                })
            
            # Add bridge metadata to result
            result["bridge_metadata"] = {
                "consent_verified": self.config.require_consent,
                "attestation_verified": self.config.require_attestation,
                "ledger_recorded": self.config.ledger_enabled
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Operation failed: {e}")
            
            # Log failure to ledger
            if self.ledger:
                self.ledger.append("operation_failed", {
                    "user_id": user_id,
                    "operation": operation,
                    "error": str(e),
                    "timestamp": time.time()
                })
            
            raise
    
    def request_consent(
        self,
        user_id: str,
        operation: str,
        scope: ConsentScope = ConsentScope.SINGLE_OPERATION,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ConsentToken:
        """
        Request consent token for an operation.
        
        Args:
            user_id: User requesting consent
            operation: Operation requiring consent
            scope: Consent scope
            metadata: Additional metadata
            
        Returns:
            Generated consent token
            
        Raises:
            RuntimeError: If consent manager not initialized
        """
        if not self.consent_manager:
            raise RuntimeError("Consent manager not initialized")
        
        token = self.consent_manager.generate_token(
            user_id=user_id,
            operation=operation,
            scope=scope,
            metadata=metadata
        )
        
        # Log consent request to ledger
        if self.ledger:
            self.ledger.append("consent_requested", {
                "user_id": user_id,
                "operation": operation,
                "token_id": token.token_id,
                "scope": scope.value,
                "timestamp": time.time()
            })
        
        return token
    
    def get_audit_trail(self, operation: Optional[str] = None) -> list:
        """
        Get audit trail from ledger.
        
        Args:
            operation: Filter by operation type
            
        Returns:
            List of audit entries
        """
        if not self.ledger:
            return self.runtime.get_audit_trail()
        
        entries = self.ledger.get_entries(operation)
        return [
            {
                "index": e.index,
                "timestamp": e.timestamp,
                "operation": e.operation,
                "data": e.data
            }
            for e in entries
        ]
    
    def get_runtime_status(self) -> Dict[str, Any]:
        """
        Get comprehensive runtime status.
        
        Returns:
            Status dictionary
        """
        status = {
            "runtime_state": self.runtime.state.value,
            "iteration_count": self.runtime.iteration_count,
            "ethics_checks_enabled": self.runtime.config.enable_ethics_checks,
            "human_approval_required": self.runtime.config.require_human_approval,
            "ledger_enabled": self.config.ledger_enabled,
            "consent_required": self.config.require_consent,
            "attestation_required": self.config.require_attestation
        }
        
        if self.ledger:
            status["ledger_entries"] = len(self.ledger.entries)
            status["ledger_integrity"] = self.ledger.verify_integrity()
        
        if self.consent_manager:
            status["active_tokens"] = len([
                t for t in self.consent_manager.tokens.values()
                if t.status.value == "active"
            ])
        
        if self.attestation:
            status["tpm_available"] = self.attestation.check_tpm_available()
        
        return status
    
    def generate_attestation_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive attestation report.
        
        Returns:
            Attestation report
        """
        report = {
            "timestamp": time.time(),
            "runtime_status": self.get_runtime_status()
        }
        
        if self.attestation:
            report["tpm_attestation"] = self.attestation.generate_attestation_report()
        
        if self.ledger:
            report["ledger_verification"] = {
                "total_entries": len(self.ledger.entries),
                "integrity_verified": self.ledger.verify_integrity()
            }
        
        return report


def main():
    """Example usage of runtime bridge."""
    
    # Initialize bridge with all features enabled
    bridge = RuntimeBridge(
        runtime_config=RuntimeConfig(
            enable_ethics_checks=True,
            require_human_approval=False,
            audit_logging=True
        ),
        bridge_config=BridgeConfig(
            require_consent=True,
            require_attestation=False,
            ledger_enabled=True
        )
    )
    
    # Request consent
    user_id = "user123"
    operation = "process_data"
    
    token = bridge.request_consent(
        user_id=user_id,
        operation=operation,
        metadata={"reason": "data analysis"}
    )
    
    print(f"Consent token generated: {token.token_id}")
    
    # Execute with consent
    input_data = {
        "query": "optimize energy distribution",
        "context": "microgrid"
    }
    
    result = bridge.execute_with_consent(
        user_id=user_id,
        operation=operation,
        input_data=input_data,
        consent_token=token
    )
    
    print(f"\nResult: {result['status']}")
    print(f"Bridge metadata: {result['bridge_metadata']}")
    
    # Get audit trail
    audit = bridge.get_audit_trail()
    print(f"\nAudit trail entries: {len(audit)}")
    
    # Get status
    status = bridge.get_runtime_status()
    print(f"\nRuntime status:")
    for key, value in status.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
