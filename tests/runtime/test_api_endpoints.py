# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors

"""Tests for API endpoints."""

import unittest
import json
from src.api.endpoints import app


class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app; self.app.config['TESTING'] = True; self.client = self.app.test_client()

    def test_health_check(self):
        r=self.client.get('/api/health'); self.assertEqual(r.status_code,200); d=json.loads(r.data); self.assertEqual(d['status'],'healthy'); self.assertIn('version',d)

    def test_get_bridge_status(self):
        r=self.client.get('/api/bridge/status'); self.assertEqual(r.status_code,200); d=json.loads(r.data); self.assertIn('runtime_state',d); self.assertIn('ledger_enabled',d); self.assertIn('consent_required',d); self.assertIn('ledger_integrity',d)

    def test_get_runtime_status(self):
        r=self.client.get('/api/runtime/status'); self.assertEqual(r.status_code,200); d=json.loads(r.data); self.assertIn('state',d); self.assertIn('ethicsChecksEnabled',d); self.assertIn('humanOversightEnabled',d)

    def test_get_audit_trail(self):
        r=self.client.get('/api/audit/trail'); self.assertEqual(r.status_code,200); self.assertGreaterEqual(len(json.loads(r.data)),1)

    def test_verify_ledger_integrity(self):
        r=self.client.get('/api/audit/verify'); self.assertEqual(r.status_code,200); self.assertTrue(json.loads(r.data)['verified'])

    def test_request_consent(self):
        p={'user_id':'test_user','operation':'test_operation','scope':'single_operation','metadata':{'reason':'testing'}}
        r=self.client.post('/api/consent/request',data=json.dumps(p),content_type='application/json'); self.assertEqual(r.status_code,200)
        d=json.loads(r.data); self.assertIn('token_id',d); self.assertEqual(d['user_id'],'test_user'); self.assertEqual(d['operation'],'test_operation')

    def test_execute_operation_fails_closed_without_verified_attestation(self):
        p={'user_id':'test_user','operation':'test_op','scope':'single_operation'}
        c=self.client.post('/api/consent/request',data=json.dumps(p),content_type='application/json'); token_id=json.loads(c.data)['token_id']
        e={'user_id':'test_user','operation':'test_op','input_data':{'test':'data'},'consent_token_id':token_id}
        r=self.client.post('/api/runtime/execute',data=json.dumps(e),content_type='application/json')
        # Production API requires platform attestation. Hosted CI uses a TPM stub,
        # so execution must be denied rather than simulated as trusted hardware.
        self.assertEqual(r.status_code,500); self.assertFalse(json.loads(r.data)['success'])

    def test_get_runtime_operations(self):
        r=self.client.get('/api/runtime/operations'); self.assertEqual(r.status_code,200); self.assertIsInstance(json.loads(r.data),list)

    def test_get_attestation_report(self):
        r=self.client.get('/api/attestation/report'); self.assertEqual(r.status_code,200); d=json.loads(r.data)
        self.assertIn('timestamp',d); self.assertIn('runtime_status',d); self.assertIn('ledger_verification',d)
        self.assertNotEqual(d['status'],'verified')


class TestAPIErrorHandling(unittest.TestCase):
    def setUp(self):
        self.app=app; self.app.config['TESTING']=True; self.client=self.app.test_client()

    def test_request_consent_missing_fields(self):
        r=self.client.post('/api/consent/request',data=json.dumps({'user_id':'test_user'}),content_type='application/json'); self.assertEqual(r.status_code,400); self.assertIn('error',json.loads(r.data))

    def test_execute_without_consent(self):
        p={'user_id':'test_user','operation':'test_op','input_data':{'test':'data'},'consent_token_id':'invalid_token'}
        r=self.client.post('/api/runtime/execute',data=json.dumps(p),content_type='application/json'); self.assertEqual(r.status_code,400); self.assertIn('error',json.loads(r.data))


if __name__ == '__main__':
    unittest.main()
