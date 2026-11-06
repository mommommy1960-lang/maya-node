"""Synthetic AAO operator smoke tests; no network, telephony, or customer data."""
import importlib.util, os, tempfile, unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location("aao_service",Path(__file__).with_name("aao_service.py"))
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class TestAAO(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        module.DB=str(Path(self.tmp.name)/"test.sqlite")
        module.TOKEN="synthetic-test-token-long-enough"
        module.SYNTHETIC_ONLY=True
        self.client=module.app.test_client()
        self.headers={"Authorization":"Bearer synthetic-test-token-long-enough"}
    def tearDown(self): self.tmp.cleanup()
    def test_permissions_and_transitions(self):
        self.assertEqual(self.client.get("/api/cases").status_code,401)
        r=self.client.post("/api/cases",headers=self.headers,json={"pantry":"Demo A","item":"Tomatoes","quantity":50,"deadline":"2026-11-07"})
        self.assertEqual(r.status_code,201)
        id=r.json["id"]
        url=f"/api/cases/{id}/transition"
        self.assertEqual(self.client.post(url,headers=self.headers,json={"action":"dispatch"}).status_code,409)
        self.assertEqual(self.client.post(url,headers=self.headers,json={"action":"propose","recipient":"Demo B"}).json["status"],"proposed")
        self.assertEqual(self.client.post(url,headers=self.headers,json={"action":"approve"}).status_code,403)
        self.assertEqual(self.client.post(url,headers=self.headers,json={"action":"approve","human_approved":True}).json["status"],"approved")
        self.assertEqual(self.client.post(url,headers=self.headers,json={"action":"dispatch","human_approved":True,"recipient":"Demo B","transport":"Demo Driver"}).json["status"],"dispatched")
        self.assertEqual(self.client.post(url,headers=self.headers,json={"action":"confirm_delivery","human_approved":True}).json["status"],"delivered")
        self.assertGreaterEqual(len(self.client.get("/api/events",headers=self.headers).json["events"]),5)
    def test_no_live_notifications_or_public_collection(self):
        self.assertEqual(self.client.post("/api/notify",headers=self.headers).status_code,503)
        self.assertEqual(self.client.post("/api/survey",json={"consent":True,"problem":"Need better transport"}).status_code,503)
    def test_health(self):
        self.assertEqual(self.client.get("/health").json["mode"],"synthetic")

if __name__=="__main__": unittest.main()
