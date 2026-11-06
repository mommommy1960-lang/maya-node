"""Synthetic-only staff training assessment API tests. No real learner identities."""
import importlib.util, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("academy",Path(__file__).with_name("aao_academy.py"))
academy=importlib.util.module_from_spec(spec); spec.loader.exec_module(academy)
class AcademyTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory()
  academy.DB=str(Path(self.temp.name)/"academy.sqlite")
  academy.OPERATOR_TOKEN="operator-token-long-for-training"
  academy.INSTRUCTOR_TOKEN="separate-instructor-secret-long"
  self.client=academy.app.test_client()
  self.auth={"Authorization":"Bearer operator-token-long-for-training"}
 def tearDown(self): self.temp.cleanup()
 def test_academy_page(self):
  response=self.client.get("/academy")
  self.assertEqual(response.status_code,200)
  self.assertIn(b"Operational Competence Academy",response.data)
 def test_training_completion(self):
  self.assertEqual(self.client.post("/api/training/complete",json={}).status_code,401)
  bad=self.client.post("/api/training/complete",headers=self.auth,json={"learner_id":"demo-01","role":"coordinator","answers":[0,0,0,0,0]})
  self.assertEqual(bad.status_code,400)
  good=self.client.post("/api/training/complete",headers=self.auth,json={"learner_id":"demo-01","role":"coordinator","answers":["no","no","escalate","no","no"],"practical_passed":True})
  self.assertEqual(good.status_code,201)
  self.assertFalse(good.json["passed"])
  approved=self.client.post("/api/training/complete",headers={**self.auth,"X-Maya-Instructor-Token":"separate-instructor-secret-long"},json={"learner_id":"demo-01","role":"coordinator","answers":["no","no","escalate","no","no"],"practical_passed":True})
  self.assertEqual(approved.status_code,201)
  self.assertTrue(approved.json["passed"])
  self.assertEqual(self.client.get("/api/training/records",headers=self.auth).json["records"][0]["learner_id"],"demo-01")
if __name__=="__main__":unittest.main()
