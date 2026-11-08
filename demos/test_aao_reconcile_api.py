"""API boundary checks for operator-only synthetic reconciliation."""
import tempfile, unittest
from pathlib import Path
from demos import aao_service as service

class ReconcileAPI(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        service.DB=str(Path(self.tmp.name)/"test.sqlite")
        service.TOKEN="demo-operator-token-at-least-24"
        service.SYNTHETIC_ONLY=True
        self.client=service.app.test_client()
        self.records=[{"synthetic":True,"kind":"order","order_id":"demo-42","quantity":10,"amount":"20.00"},{"synthetic":True,"kind":"delivery","order_id":"demo-42","quantity":7}]
    def tearDown(self):self.tmp.cleanup()
    def test_requires_operator_and_reports_only(self):
        self.assertEqual(self.client.post("/api/reconcile",json={"records":self.records}).status_code,401)
        resp=self.client.post("/api/reconcile",headers={"Authorization":"Bearer "+service.TOKEN},json={"records":self.records})
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.json["findings"][0]["type"],"missing_delivery")
        self.assertFalse(resp.json["automated_actions"])
        self.assertTrue(resp.json["human_approval_required"])
    def test_real_data_rejected(self):
        bad=[{"kind":"order","order_id":"demo-42","quantity":10}]
        resp=self.client.post("/api/reconcile",headers={"Authorization":"Bearer "+service.TOKEN},json={"records":bad})
        self.assertEqual(resp.status_code,400)
    def test_disabled_outside_synthetic_mode(self):
        service.SYNTHETIC_ONLY=False
        resp=self.client.post("/api/reconcile",headers={"Authorization":"Bearer "+service.TOKEN},json={"records":self.records})
        self.assertEqual(resp.status_code,403)

if __name__=="__main__":unittest.main()
