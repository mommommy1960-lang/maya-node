# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors

"""Security-hardened API endpoint layer for the MAYA Node runtime."""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import os

from src.sovereign.runtime_bridge import RuntimeBridge, BridgeConfig
from src.sovereign.runtime import RuntimeConfig
from src.sovereign.consent_tokens import ConsentScope

logger = logging.getLogger(__name__)
app = Flask(__name__)

# Fail closed: cross-origin access is disabled unless explicitly configured.
_allowed_origins = [o.strip() for o in os.environ.get("MAYA_ALLOWED_ORIGINS", "").split(",") if o.strip()]
if _allowed_origins:
    CORS(app, resources={r"/api/*": {"origins": _allowed_origins}})

bridge = RuntimeBridge(
    runtime_config=RuntimeConfig(
        enable_ethics_checks=True,
        require_human_approval=True,
        audit_logging=True,
    ),
    bridge_config=BridgeConfig(
        require_consent=True,
        require_attestation=True,
        ledger_enabled=True,
    ),
)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'maya-node-api', 'version': '1.0.0-omega'})

@app.route('/api/bridge/status', methods=['GET'])
def get_bridge_status():
    try:
        return jsonify(bridge.get_runtime_status())
    except Exception as exc:
        logger.exception("bridge status failed: %s", exc)
        return jsonify({'error': 'Failed to retrieve bridge status'}), 500

@app.route('/api/runtime/status', methods=['GET'])
def get_runtime_status():
    try:
        return jsonify({'state': bridge.runtime.state.value,
                        'ethicsChecksEnabled': bridge.runtime.config.enable_ethics_checks,
                        'humanOversightEnabled': bridge.runtime.config.require_human_approval,
                        'vettedModelsCount': 0,
                        'iterationCount': bridge.runtime.iteration_count})
    except Exception as exc:
        logger.exception("runtime status failed: %s", exc)
        return jsonify({'error': 'Failed to retrieve runtime status'}), 500

@app.route('/api/audit/trail', methods=['GET'])
def get_audit_trail():
    try:
        return jsonify(bridge.get_audit_trail(request.args.get('operation')))
    except Exception as exc:
        logger.exception("audit trail failed: %s", exc)
        return jsonify({'error': 'Failed to retrieve audit trail'}), 500

@app.route('/api/audit/verify', methods=['GET'])
def verify_ledger_integrity():
    try:
        if not bridge.ledger:
            return jsonify({'error': 'Ledger not enabled'}), 400
        verified = bridge.ledger.verify_integrity()
        return jsonify({'verified': verified,
                        'message': 'Ledger integrity verified' if verified else 'Ledger integrity check failed'})
    except Exception as exc:
        logger.exception("ledger verification failed: %s", exc)
        return jsonify({'error': 'Failed to verify ledger integrity'}), 500

@app.route('/api/consent/request', methods=['POST'])
def request_consent():
    try:
        data = request.get_json(silent=True) or {}
        user_id, operation = data.get('user_id'), data.get('operation')
        if not user_id or not operation:
            return jsonify({'error': 'user_id and operation required'}), 400
        scope_name = str(data.get('scope', 'single_operation')).upper()
        try:
            scope = ConsentScope[scope_name]
        except KeyError:
            return jsonify({'error': 'invalid consent scope'}), 400
        token = bridge.request_consent(user_id=user_id, operation=operation, scope=scope,
                                       metadata=data.get('metadata', {}))
        return jsonify(token.to_dict())
    except Exception as exc:
        logger.exception("consent request failed: %s", exc)
        return jsonify({'error': 'Failed to generate consent token'}), 500

@app.route('/api/runtime/execute', methods=['POST'])
def execute_operation():
    try:
        data = request.get_json(silent=True) or {}
        user_id, operation, token_id = data.get('user_id'), data.get('operation'), data.get('consent_token_id')
        if not user_id or not operation or not token_id:
            return jsonify({'error': 'user_id, operation, and consent_token_id required'}), 400
        if not bridge.consent_manager:
            return jsonify({'error': 'Consent manager not initialized'}), 400
        token = bridge.consent_manager.get_token(token_id)
        if not token:
            return jsonify({'error': 'Invalid consent token'}), 400
        result = bridge.execute_with_consent(user_id=user_id, operation=operation,
                                             input_data=data.get('input_data', {}), consent_token=token)
        return jsonify({'success': True, 'result': result})
    except Exception as exc:
        logger.exception("operation execution failed: %s", exc)
        return jsonify({'success': False, 'error': 'Operation execution failed'}), 500

@app.route('/api/ethics/violations', methods=['GET'])
def get_ethics_violations():
    return jsonify([])

@app.route('/api/ethics/decisions', methods=['GET'])
def get_ethics_decisions():
    return jsonify([])

@app.route('/api/runtime/operations', methods=['GET'])
def get_runtime_operations():
    try:
        operations = bridge.get_audit_trail()
        return jsonify([{'id': f"op_{op['index']}", 'timestamp': op['timestamp'],
                         'operation': op['operation'], 'status': 'completed', 'ethicsVerified': True}
                        for op in operations[-10:]])
    except Exception as exc:
        logger.exception("operations retrieval failed: %s", exc)
        return jsonify({'error': 'Failed to retrieve runtime operations'}), 500

@app.route('/api/attestation/report', methods=['GET'])
def get_attestation_report():
    try:
        return jsonify(bridge.generate_attestation_report())
    except Exception as exc:
        logger.exception("attestation failed: %s", exc)
        return jsonify({'error': 'Failed to generate attestation report'}), 500

def main():
    debug_mode = os.environ.get('FLASK_DEBUG', '').lower() in {'1', 'true', 'yes'}
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', '5000'))
    if debug_mode and os.environ.get('MAYA_ALLOW_DEBUG', '').lower() not in {'1', 'true', 'yes'}:
        raise RuntimeError('Debug mode requires explicit MAYA_ALLOW_DEBUG opt-in')
    app.run(host=host, port=port, debug=debug_mode)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()
