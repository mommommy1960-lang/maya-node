"""Executable synthetic-only reconciliation acceptance journey.

Run: python -m unittest demos.test_aao_reconciliation_journey -v
No network, customer data, billing, or dispatch.
"""
import tempfile
import unittest
from pathlib import Path
from demos import aao_service as service

TOKEN="demo-operator-reconciliation-token-0001"
FIXTURE=[
    {"synthetic":True,"kind":"order","order_id":"demo-food-001","quantity":120,"amount":"240.00"},
    {"synthetic":True,"kind":"delivery","order_id":"demo-food-001","quantity":90},
    {"synthetic":True,"kind":"inventory","order_id":"demo-food-001","quantity":75},
    {"synthetic":True,"kind":"payment","order_id":"demo-food-001","quantity":0,"amount":"260.00"},
    {"synthetic":True,"kind":"order","order_id":"demo-food-002","quantity":40,"amount":"80.00"},
    {"synthetic":True,"kind":"delivery","order_id":"demo-food-002","quantity":40},
    {"synthetic":True,"kind":"inventory","order_id":"demo-food-002","quantity":40},
    {"synthetic":True,"kind":"payment","order_id":"demo-food-002","quantity":0,"amount":"80.00"},
]
class FullReconciliationJourney(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        service.DB=str(Path(self.tmp.name)/"reconciliation.sqlite")
        service.TOKEN=TOKEN
        service.SYNTHETIC_ONLY=True
        self.client=service.app.test_client()
        self.headers={"Authorization":"Bearer "+TOKEN}
    def tearDown(self):
        self.tmp.cleanup()
    def test_complete_business_analysis_and_receipt(self):
        response=self.client.post("/api/reconcile",headers=self.headers,json={"records":FIXTURE})
        self.assertEqual(response.status_code,200,response.get_data(as_text=True))
        report=response.get_json()
        self.assertEqual(report["orders_reviewed"],2)
        self.assertEqual(len(report["findings"]),3)
        self.assertEqual({f["type"]:f["difference"] for f in report["findings"]},{
            "missing_delivery":30,
            "unaccounted_inventory":15,
            "payment_exceeds_order":"20.00",
        })
        self.assertTrue(report["human_approval_required"])
        self.assertFalse(report["automated_actions"])
        self.assertIn("not evidence of theft",report["disclaimer"])
        events=self.client.get("/api/events",headers=self.headers).get_json()["events"]
        self.assertTrue(any(e["kind"]=="synthetic_reconciliation" for e in events))
        self.assertFalse(any(e["kind"] in ("dispatch","payment","approve") for e in events))
        self.assertEqual(self.client.get("/health").get_json()["mode"],"synthetic")
if __name__=="__main__":unittest.main()
