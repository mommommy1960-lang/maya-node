# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
#
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""API Endpoint Layer - Phase Omega.

Security defaults are intentionally fail-closed: human approval remains required,
and cross-origin access is restricted unless an operator explicitly configures
MAYA_ALLOWED_ORIGINS.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import os
from typing import Dict, Any

from src.sovereign.runtime_bridge import RuntimeBridge, BridgeConfig
from src.sovereign.runtime import RuntimeConfig
from src.sovereign.consent_tokens import ConsentScope

logger = logging.getLogger(__name__)

app = Flask(__name__)
_allowed_origins = [
    origin.strip()
    for origin in os.getenv("MAYA_ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]
CORS(app, resources={r"/api/*": {"origins": _allowed_origins}})

bridge = RuntimeBridge(
    runtime_config=RuntimeConfig(
        enable_ethics_checks=True,
        require_human_approval=True,
        audit_logging=True
    ),
    bridge_config=BridgeConfig(
        require_consent=True,
        require_attestation=False,
        ledger_enabled=True
    )
)

logger.info("API endpoint layer initialized")


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'maya-node-api', 'version': '1.0.0-omega'})


@app.route('/api/bridge/status', methods=['GET'])
def get_bridge_status():
    try:
        return jsonify(bridge.get_runtime_status())
    except Exception as e:
        logger.error("Error getting bridge status: %s", e)
        return jsonify({'error': 'Failed to retrieve bridge status'}), 500


@app.route('/api/runtime/status', methods=['GET'])
def get_runtime_status():
    try:
        return jsonify({
            'state': bridge.runtime.state.value,
            'ethicsChecksEnabled': bridge.runtime.config.enable_ethics_checks,
            'humanOversightEnabled': bridge.runtime.config.require_human_approval,
            'vettedModelsCount': 0,
            'iterationCount': bridge.runtime.iteration_count
        })
    except Exception as e:
        logger.error("Error getting runtime status: %s", e)
        return jsonify({'error': 'Failed to retrieve runtime status'}), 500


@app.route('/api/audit/trail', methods=['GET'])
def get_audit_trail():
    try:
        operation = request.args.get('operation', None)
        return jsonify(bridge.get_audit_trail(operation))
    except Exception as e:
        logger.error("Error getting audit trail: %s", e)
        return jsonify({'error': 'Failed to retrieve audit trail'}), 500


@app.route('/api/audit/verify', methods=['GET'])
def verify_ledger_integrity():
    try:
        if not bridge.ledger:
            return jsonify({'error': 'Ledger not enabled'}), 400
        verified = bridge.ledger.verify_integrity()
        return jsonify({'verified': verified, 'message': 'Ledger integrity verified' if verified else 'Ledger integrity check failed'})
    except Exception as e:
        logger.error("Error verifying ledger integrity: %s", e)
        return jsonify({'error': 'Failed to verify ledger integrity'}), 500


@app.route('/api/consent/request', methods=['POST'])
def request_consent():
    """Request a consent token."""
    try:
        data: Dict[str, Any] = request.get_json(silent=True) or {}
        user_id = data.get('user_id')
        operation = data.get('operation')
        scope_value = data.get('scope')
        if not user_id or not operation or not scope_value:
            return jsonify({'error': 'user_id, operation, and scope are required'}), 400
        scope = ConsentScope(scope_value)
        token = bridge.request_consent(user_id, operation, scope)
        return jsonify(token.to_dict()), 201
    except (ValueError, KeyError) as e:
        return jsonify({'error': f'Invalid consent request: {e}'}), 400
    except Exception as e:
        logger.error("Error requesting consent: %s", e)
        return jsonify({'error': 'Failed to request consent'}), 500
