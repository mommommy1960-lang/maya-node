# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Tests for API Endpoints
"""

import unittest
import json
from src.api.endpoints import app


class TestAPIEndpoints(unittest.TestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('version', data)
    
    def test_get_bridge_status(self):
        """Test bridge status endpoint"""
        response = self.client.get('/api/bridge/status')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('runtime_state', data)
        self.assertIn('ledger_enabled', data)
        self.assertIn('consent_required', data)
    
    def test_get_runtime_status(self):
        """Test runtime status endpoint"""
        response = self.client.get('/api/runtime/status')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('state', data)
        self.assertIn('ethicsChecksEnabled', data)
        self.assertIn('humanOversightEnabled', data)
    
    def test_get_audit_trail(self):
        """Test audit trail endpoint"""
        response = self.client.get('/api/audit/trail')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        # Should have at least genesis entry
        self.assertGreaterEqual(len(data), 1)
    
    def test_verify_ledger_integrity(self):
        """Test ledger integrity verification endpoint"""
        response = self.client.get('/api/audit/verify')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('verified', data)
        self.assertTrue(data['verified'])
    
    def test_request_consent(self):
        """Test consent token request endpoint"""
        payload = {
            'user_id': 'test_user',
            'operation': 'test_operation',
            'scope': 'single_operation',
            'metadata': {'reason': 'testing'}
        }
        
        response = self.client.post(
            '/api/consent/request',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('token_id', data)
        self.assertEqual(data['user_id'], 'test_user')
        self.assertEqual(data['operation'], 'test_operation')
    
    def test_execute_operation(self):
        """Test operation execution endpoint"""
        # First, request consent
        consent_payload = {
            'user_id': 'test_user',
            'operation': 'test_op',
            'scope': 'single_operation'
        }
        
        consent_response = self.client.post(
            '/api/consent/request',
            data=json.dumps(consent_payload),
            content_type='application/json'
        )
        
        consent_data = json.loads(consent_response.data)
        token_id = consent_data['token_id']
        
        # Now execute with consent
        exec_payload = {
            'user_id': 'test_user',
            'operation': 'test_op',
            'input_data': {'test': 'data'},
            'consent_token_id': token_id
        }
        
        response = self.client.post(
            '/api/runtime/execute',
            data=json.dumps(exec_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('result', data)
    
    def test_get_runtime_operations(self):
        """Test getting runtime operations"""
        response = self.client.get('/api/runtime/operations')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_get_attestation_report(self):
        """Test attestation report endpoint"""
        response = self.client.get('/api/attestation/report')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
        self.assertIn('runtime_status', data)


class TestAPIErrorHandling(unittest.TestCase):
    """Test error handling in API endpoints"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_request_consent_missing_fields(self):
        """Test consent request with missing fields"""
        payload = {
            'user_id': 'test_user'
            # Missing 'operation'
        }
        
        response = self.client.post(
            '/api/consent/request',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_execute_without_consent(self):
        """Test execution with invalid token"""
        payload = {
            'user_id': 'test_user',
            'operation': 'test_op',
            'input_data': {'test': 'data'},
            'consent_token_id': 'invalid_token'
        }
        
        response = self.client.post(
            '/api/runtime/execute',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
