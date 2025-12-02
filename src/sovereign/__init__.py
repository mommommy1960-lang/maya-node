# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Sovereign AI Runtime Module

This module provides ethical AI runtime capabilities with:
- Transparent decision-making
- Ethical constraint enforcement
- Human oversight integration
- Vetted model management
- Consent token generation and validation
- Append-only audit logging
"""

from .runtime import SovereignRuntime, RuntimeConfig, RuntimeState
from .ethics_engine import EthicsEngine, EthicsViolation, ViolationSeverity
from .model_interface import ModelInterface, ModelMetadata, ModelStatus
from .hitl import HumanInTheLoop, ApprovalRequest, ApprovalStatus
from .consent_token import (
    ConsentToken, 
    ConsentTokenManager, 
    generate_trust_root_key
)
from .audit_log import (
    AppendOnlyAuditLog,
    AuditLogEntry
)

__all__ = [
    # Runtime
    'SovereignRuntime',
    'RuntimeConfig',
    'RuntimeState',
    
    # Ethics
    'EthicsEngine',
    'EthicsViolation',
    'ViolationSeverity',
    
    # Models
    'ModelInterface',
    'ModelMetadata',
    'ModelStatus',
    
    # Human-in-Loop
    'HumanInTheLoop',
    'ApprovalRequest',
    'ApprovalStatus',
    
    # Consent Tokens
    'ConsentToken',
    'ConsentTokenManager',
    'generate_trust_root_key',
    
    # Audit Log
    'AppendOnlyAuditLog',
    'AuditLogEntry',
]

__version__ = '0.1.0-bootstrap'
