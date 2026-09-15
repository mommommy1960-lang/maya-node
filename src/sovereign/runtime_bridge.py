# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors

"""Runtime bridge with consent, attestation, and ledger enforcement."""

import logging
import time
from typing import Any, Dict, Optional
from dataclasses import dataclass

from .runtime import SovereignRuntime, RuntimeConfig
from .consent_tokens import ConsentTokenManager, ConsentToken, ConsentScope
from .tpm_attestation import TPMAttestationStub, AttestationStatus
from ..services.ledger.ledger import ImmutableLedger

logger = logging.getLogger(__name__)

@dataclass
class BridgeConfig:
    require_consent: bool = True
    require_attestation: bool = False
    ledger_enabled: bool = True

class RuntimeBridge:
    def __init__(self, runtime_config: Optional[RuntimeConfig] = None,
                 bridge_config: Optional[BridgeConfig] = None):
        self.runtime = SovereignRuntime(runtime_config)
        self.config = bridge_config or BridgeConfig()
        self.ledger = ImmutableLedger() if self.config.ledger_enabled else None
        self.consent_manager = ConsentTokenManager() if self.config.require_consent else None
        self.attestation = TPMAttestationStub() if self.config.require_attestation else None
        if self.ledger:
            self.ledger.append("runtime_bridge_init", {
                "timestamp": time.time(),
                "consent_required": self.config.require_consent,
                "attestation_required": self.config.require_attestation,
            })

    def execute_with_consent(self, user_id: str, operation: str,
                             input_data: Dict[str, Any],
                             consent_token: Optional[ConsentToken] = None) -> Dict[str, Any]:
        if self.config.require_consent:
            if not consent_token or not self.consent_manager:
                raise RuntimeError("Consent token required but not provided")
            if not self.consent_manager.verify_token(consent_token):
                raise RuntimeError("Invalid or expired consent token")
            if consent_token.user_id != user_id:
                raise RuntimeError("Consent token user mismatch")
            if consent_token.operation != operation:
                raise RuntimeError("Consent token operation mismatch")

        if self.config.require_attestation:
            if not self.attestation:
                raise RuntimeError("Attestation required but verifier unavailable")
            attestation_result = self.attestation.verify_platform_integrity()
            if attestation_result.status != AttestationStatus.VERIFIED:
                raise RuntimeError("Platform attestation not verified")

        if self.ledger:
            self.ledger.append("operation_start", {
                "user_id": user_id, "operation": operation,
                "consent_token_id": consent_token.token_id if consent_token else None,
                "timestamp": time.time(),
            })
        try:
            result = self.runtime.process(input_data)
            if consent_token and self.consent_manager:
                if not self.consent_manager.use_token(consent_token.token_id):
                    raise RuntimeError("Consent token could not be consumed")
            if self.ledger:
                self.ledger.append("operation_complete", {
                    "user_id": user_id, "operation": operation,
                    "status": "success", "timestamp": time.time(),
                })
            result["bridge_metadata"] = {
                "consent_verified": self.config.require_consent,
                "attestation_verified": self.config.require_attestation,
                "ledger_recorded": self.config.ledger_enabled,
            }
            return result
        except Exception as exc:
            if self.ledger:
                self.ledger.append("operation_failed", {
                    "user_id": user_id, "operation": operation,
                    "error": str(exc), "timestamp": time.time(),
                })
            raise

    def request_consent(self, user_id: str, operation: str,
                        scope: ConsentScope = ConsentScope.SINGLE_OPERATION,
                        metadata: Optional[Dict[str, Any]] = None) -> ConsentToken:
        if not self.consent_manager:
            raise RuntimeError("Consent manager not initialized")
        token = self.consent_manager.generate_token(user_id=user_id, operation=operation,
                                                    scope=scope, metadata=metadata)
        if self.ledger:
            self.ledger.append("consent_requested", {
                "user_id": user_id, "operation": operation, "token_id": token.token_id,
                "scope": scope.value, "timestamp": time.time(),
            })
        return token

    def get_audit_trail(self, operation: Optional[str] = None) -> list:
        if not self.ledger:
            return self.runtime.get_audit_trail()
        return [{"index": e.index, "timestamp": e.timestamp,
                 "operation": e.operation, "data": e.data}
                for e in self.ledger.get_entries(operation)]

    def get_runtime_status(self) -> Dict[str, Any]:
        return {
            "runtime_state": self.runtime.state.value,
            "iteration_count": self.runtime.iteration_count,
            "ethics_checks_enabled": self.runtime.config.enable_ethics_checks,
            "human_approval_required": self.runtime.config.require_human_approval,
            "ledger_enabled": self.config.ledger_enabled,
            "ledger_integrity": self.ledger.verify_integrity() if self.ledger else None,
            "consent_required": self.config.require_consent,
            "attestation_required": self.config.require_attestation,
        }

    def generate_attestation_report(self) -> Dict[str, Any]:
        now = time.time()
        runtime_status = self.get_runtime_status()
        if not self.attestation:
            return {
                "enabled": False,
                "status": "not_configured",
                "timestamp": now,
                "runtime_status": runtime_status,
                "ledger_verification": runtime_status["ledger_integrity"],
            }
        result = self.attestation.verify_platform_integrity()
        return {
            "enabled": True,
            "status": result.status.value,
            "notes": result.notes,
            "timestamp": now,
            "runtime_status": runtime_status,
            "ledger_verification": runtime_status["ledger_integrity"],
        }
