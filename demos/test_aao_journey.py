"""Cross-service synthetic-only acceptance test. No network or real pantry data."""
import importlib.util, tempfile, unittest, base64, json, hmac, hashlib, time
from pathlib import Path
def load(name):
 spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+".py"))
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
aao=load("aao_service")
academy=load("aao_academy")
class SyntheticJourney(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory()
  aao.DB=str(Path(self.tmp.name)/"operator.sqlite")
  academy.DB=str(Path(self.tmp.name)/"academy.sqlite")
  aao.TOKEN="operator-demo-token-very-long"
  aao.APPROVER_TOKEN="separate-approver-demo-token"
  aao.APPROVER_ID="demo-approver-01"
  aao.SYNTHETIC_ONLY=True
  academy.OPERATOR_TOKEN="academy-operator-token-long"
  academy.INSTRUCTOR_TOKEN="academy-instructor-token-long"
  academy.INSTRUCTOR_ID="demo-instructor-01"
  academy.STAFF_SIGNING_KEY="synthetic-signing-secret-at-least-32-chars"
  academy.SUPERVISOR_TOKEN="academy-supervisor-token-long"
  academy.SUPERVISOR_ID="demo-supervisor-01"
  self.o=aao.app.test_client()
  self.t=academy.app.test_client()
 def tearDown(self):self.tmp.cleanup()
 def test_training_then_verified_synthetic_transfer(self):
  token={"Authorization":"Bearer academy-operator-token-long"}
  payload=base64.urlsafe_b64encode(json.dumps({"sub":"demo-learner-01","exp":int(time.time())+600}).encode()).decode().rstrip("=")
  sig=hmac.new(academy.STAFF_SIGNING_KEY.encode(),payload.encode(),hashlib.sha256).hexdigest()
  staff={**token,"X-Maya-Staff-Identity":payload+"."+sig}
  answers={"learner_id":"demo-learner-01","role":"coordinator","answers":["no","no","escalate","no","no"],"practical_passed":True}
  self.assertFalse(self.t.post("/api/training/complete",headers=staff,json=answers).json["passed"])
  verified=self.t.post("/api/training/complete",headers={**staff,"X-Maya-Instructor-Token":academy.INSTRUCTOR_TOKEN},json=answers)
  self.assertEqual(verified.status_code,201)
  self.assertTrue(verified.json["passed"])
  op={"Authorization":"Bearer operator-demo-token-very-long"}
  approver={**op,"X-Maya-Approver-Token":"separate-approver-demo-token"}
  create=self.o.post("/api/cases",headers=op,json={"pantry":"Demo Pantry A","item":"Tomatoes","quantity":50,"deadline":"2026-11-07"})
  self.assertEqual(create.status_code,201)
  route=f'/api/cases/{create.json["id"]}/transition'
  self.assertEqual(self.o.post(route,headers=op,json={"action":"propose","recipient":"Demo Pantry B"}).status_code,200)
  self.assertEqual(self.o.post(route,headers=approver,json={"action":"approve","human_approved":True}).status_code,200)
  self.assertEqual(self.o.post(route,headers=approver,json={"action":"dispatch","human_approved":True,"recipient":"Demo Pantry B","transport":"Demo Driver"}).status_code,200)
  self.assertEqual(self.o.post(route,headers=approver,json={"action":"confirm_delivery","human_approved":True}).status_code,400)
  done=self.o.post(route,headers=approver,json={"action":"confirm_delivery","human_approved":True,"delivery_evidence":{"synthetic":True,"type":"simulated_receipt","reference":"demo-proof-001"}})
  self.assertEqual(done.status_code,200)
  self.assertEqual(done.json["status"],"delivered")
  self.assertTrue(any("demo-proof-001" in e["payload"] for e in self.o.get("/api/events",headers=op).json["events"]))
  self.assertEqual(self.o.post("/api/notify",headers=op).status_code,503)
  self.assertFalse(self.t.get("/api/training/readiness").json["customer_ready"])
if __name__=="__main__":unittest.main()
