# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
API Endpoint Layer - Phase Omega

This module provides HTTP API endpoints for the web dashboard to
communicate with the sovereign runtime bridge.

Key Features:
- REST API for runtime operations
- Ethics decision streaming
- Audit trail access
- Consent token management
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from typing import Dict, Any

from src.sovereign.runtime_bridge import RuntimeBridge, BridgeConfig
from src.sovereign.runtime import RuntimeConfig
from src.sovereign.consent_tokens import ConsentScope

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for web dashboard

# Initialize runtime bridge
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

logger.info("API endpoint layer initialized")


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'maya-node-api',
        'version': '1.0.0-omega'
    })


@app.route('/api/bridge/status', methods=['GET'])
def get_bridge_status():
    """Get runtime bridge status"""
    try:
        status = bridge.get_runtime_status()
        return jsonify(status)
    except Exception as e:
        logger.error(f"Error getting bridge status: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/runtime/status', methods=['GET'])
def get_runtime_status():
    """Get sovereign runtime status"""
    try:
        return jsonify({
            'state': bridge.runtime.state.value,
            'ethicsChecksEnabled': bridge.runtime.config.enable_ethics_checks,
            'humanOversightEnabled': bridge.runtime.config.require_human_approval,
            'vettedModelsCount': 0,  # TODO: Implement model registry
            'iterationCount': bridge.runtime.iteration_count
        })
    except Exception as e:
        logger.error(f"Error getting runtime status: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/audit/trail', methods=['GET'])
def get_audit_trail():
    """Get audit trail from ledger"""
    try:
        operation = request.args.get('operation', None)
        trail = bridge.get_audit_trail(operation)
        return jsonify(trail)
    except Exception as e:
        logger.error(f"Error getting audit trail: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/audit/verify', methods=['GET'])
def verify_ledger_integrity():
    """Verify ledger integrity"""
    try:
        if not bridge.ledger:
            return jsonify({'error': 'Ledger not enabled'}), 400
        
        verified = bridge.ledger.verify_integrity()
        return jsonify({
            'verified': verified,
            'message': 'Ledger integrity verified' if verified else 'Ledger integrity check failed'
        })
    except Exception as e:
        logger.error(f"Error verifying ledger: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/consent/request', methods=['POST'])
def request_consent():
    """Request consent token"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        operation = data.get('operation')
        scope = data.get('scope', 'single_operation')
        metadata = data.get('metadata', {})
        
        if not user_id or not operation:
            return jsonify({'error': 'user_id and operation required'}), 400
        
        # Map string scope to enum
        scope_enum = ConsentScope[scope.upper()] if hasattr(ConsentScope, scope.upper()) else ConsentScope.SINGLE_OPERATION
        
        token = bridge.request_consent(
            user_id=user_id,
            operation=operation,
            scope=scope_enum,
            metadata=metadata
        )
        
        return jsonify(token.to_dict())
    except Exception as e:
        logger.error(f"Error requesting consent: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/runtime/execute', methods=['POST'])
def execute_operation():
    """Execute operation with consent"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        operation = data.get('operation')
        input_data = data.get('input_data', {})
        consent_token_id = data.get('consent_token_id')
        
        if not user_id or not operation or not consent_token_id:
            return jsonify({'error': 'user_id, operation, and consent_token_id required'}), 400
        
        # Get consent token
        if not bridge.consent_manager:
            return jsonify({'error': 'Consent manager not initialized'}), 400
        
        token = bridge.consent_manager.get_token(consent_token_id)
        if not token:
            return jsonify({'error': 'Invalid consent token'}), 400
        
        # Execute with consent
        result = bridge.execute_with_consent(
            user_id=user_id,
            operation=operation,
            input_data=input_data,
            consent_token=token
        )
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        logger.error(f"Error executing operation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ethics/violations', methods=['GET'])
def get_ethics_violations():
    """Get recent ethics violations"""
    try:
        # TODO: Integrate with ethics engine to get real violations
        # For now, return empty array
        return jsonify([])
    except Exception as e:
        logger.error(f"Error getting ethics violations: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/ethics/decisions', methods=['GET'])
def get_ethics_decisions():
    """Get ethics decisions"""
    try:
        # TODO: Integrate with ethics engine to get real decisions
        # For now, return empty array
        return jsonify([])
    except Exception as e:
        logger.error(f"Error getting ethics decisions: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/runtime/operations', methods=['GET'])
def get_runtime_operations():
    """Get recent runtime operations"""
    try:
        # Get from audit trail
        operations = bridge.get_audit_trail()
        
        # Format for UI
        formatted = []
        for i, op in enumerate(operations[-10:]):  # Last 10 operations
            formatted.append({
                'id': f"op_{op['index']}",
                'timestamp': op['timestamp'],
                'operation': op['operation'],
                'status': 'completed',
                'ethicsVerified': True
            })
        
        return jsonify(formatted)
    except Exception as e:
        logger.error(f"Error getting operations: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/attestation/report', methods=['GET'])
def get_attestation_report():
    """Get TPM attestation report"""
    try:
        report = bridge.generate_attestation_report()
        return jsonify(report)
    except Exception as e:
        logger.error(f"Error generating attestation report: {e}")
        return jsonify({'error': str(e)}), 500


def main():
    """Run the API server"""
    import os
    
    # Security: Use environment variable to control debug mode
    # In production, set FLASK_ENV=production
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    host = os.environ.get('FLASK_HOST', '127.0.0.1')  # Default to localhost for security
    port = int(os.environ.get('FLASK_PORT', '5000'))
    
    logger.info(f"Starting MAYA Node API server on {host}:{port}")
    logger.info(f"Debug mode: {debug_mode}")
    
    if debug_mode:
        logger.warning("Running in DEBUG mode - not suitable for production!")
    
    app.run(host=host, port=port, debug=debug_mode)


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    main()
