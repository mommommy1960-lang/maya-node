"""Synthetic-only staff training assessment API tests. No real learner identities."""
import importlib.util, tempfile, unittest, base64, json, hmac, hashlib, time, sqlite3
from pathlib import Path
spec=importlib.util.spec_from_file_location("academy",Path(__file__).with_name("aao_academy.py"))
academy=importlib.util.module_from_spec(spec); spec.loader.exec_module(academy)
class AcademyTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory()
  academy.DB=str(Path(self.temp.name)/"academy.sqlite")
  academy.OPERATOR_TOKEN="operator-token-long-for-training"
  academy.INSTRUCTOR_TOKEN="separate-instructor-secret-long"
  academy.INSTRUCTOR_ID="demo-instructor-01"
  academy.STAFF_SIGNING_KEY="synthetic-staff-signing-secret-at-least-32"
  academy.SUPERVISOR_TOKEN="synthetic-supervisor-secret-long"
  academy.SUPERVISOR_ID="demo-supervisor-01"
  self.client=academy.app.test_client()
  self.auth={"Authorization":"Bearer operator-token-long-for-training"}
  payload=base64.urlsafe_b64encode(json.dumps({"sub":"demo-01","exp":int(time.time())+600}).encode()).decode().rstrip("=")
  sig=hmac.new(academy.STAFF_SIGNING_KEY.encode(),payload.encode(),hashlib.sha256).hexdigest()
  self.staff_auth={**self.auth,"X-Maya-Staff-Identity":payload+"."+sig}
 def tearDown(self): self.temp.cleanup()
 def test_readiness_fails_closed_for_real_customers(self):
  result=self.client.get("/api/training/readiness")
  self.assertEqual(result.status_code,200)
  self.assertEqual(result.json["mode"],"synthetic_only")
  self.assertIs(result.json["customer_ready"],False)
  self.assertIs(result.json["live_billing"],False)
  self.assertIs(result.json["checks"]["production_staff_identity"],False)
  self.assertIs(result.json["checks"]["end_to_end_staging_verified"],False)
 def test_academy_page(self):
  response=self.client.get("/academy")
  self.assertEqual(response.status_code,200)
  self.assertIn(b"Operational Competence Academy",response.data)
 def test_completion_persists_after_reopening_database(self):
  payload={"learner_id":"demo-01","role":"coordinator","answers":["no","no","escalate","no","no"],"practical_passed":True}
  response=self.client.post("/api/training/complete",headers=self.staff_auth,json=payload)
  self.assertEqual(response.status_code,201)
  with academy.connect() as conn:
   persisted=conn.execute("SELECT id,learner_id,passed FROM completions WHERE id=?",(response.json["id"],)).fetchone()
  self.assertIsNotNone(persisted)
  self.assertEqual(persisted["learner_id"],"demo-01")
  self.assertEqual(persisted["passed"],0)
 def test_sqlite_backup_restore_recovers_completion_and_audit(self):
  data={"learner_id":"demo-01","role":"coordinator","answers":["no","no","escalate","no","no"],"practical_passed":True}
  response=self.client.post("/api/training/complete",headers={**self.staff_auth,"X-Maya-Instructor-Token":"separate-instructor-secret-long"},json=data)
  self.assertEqual(response.status_code,201)
  supervisor={**self.auth,"X-Maya-Supervisor-Token":"synthetic-supervisor-secret-long"}
  self.assertEqual(self.client.get("/api/training/supervisor-records",headers=supervisor).status_code,200)
  backup=str(Path(self.temp.name)/"backup.sqlite")
  with sqlite3.connect(academy.DB) as source,sqlite3.connect(backup) as dest:
   source.backup(dest)
  with sqlite3.connect(academy.DB) as original:
   original.execute("DELETE FROM completions")
   original.execute("DELETE FROM access_audit")
  with sqlite3.connect(backup) as source,sqlite3.connect(academy.DB) as dest:
   source.backup(dest)
  with sqlite3.connect(academy.DB) as restored:
   self.assertEqual(restored.execute("SELECT count(*) FROM completions").fetchone()[0],1)
   self.assertEqual(restored.execute("SELECT count(*) FROM access_audit").fetchone()[0],1)
  self.assertEqual(self.client.get("/api/training/records",headers=self.staff_auth).json["records"][0]["id"],response.json["id"])
 def test_reject_forged_and_expired_staff_identity(self):
  data={"learner_id":"demo-01","role":"coordinator","answers":["no","no","escalate","no","no"],"practical_passed":True}
  forged={**self.staff_auth,"X-Maya-Staff-Identity":self.staff_auth["X-Maya-Staff-Identity"][:-1]+"x"}
  self.assertEqual(self.client.post("/api/training/complete",headers=forged,json=data).status_code,403)
  payload=base64.urlsafe_b64encode(json.dumps({"sub":"demo-01","exp":int(time.time())-60}).encode()).decode().rstrip("=")
  sig=hmac.new(academy.STAFF_SIGNING_KEY.encode(),payload.encode(),hashlib.sha256).hexdigest()
  expired={**self.auth,"X-Maya-Staff-Identity":payload+"."+sig}
  self.assertEqual(self.client.post("/api/training/complete",headers=expired,json=data).status_code,403)
  mismatch={**self.staff_auth}
  self.assertEqual(self.client.post("/api/training/complete",headers=mismatch,json={**data,"learner_id":"demo-02"}).status_code,403)
 def test_training_completion(self):
  self.assertEqual(self.client.post("/api/training/complete",json={}).status_code,401)
  bad=self.client.post("/api/training/complete",headers=self.staff_auth,json={"learner_id":"demo-01","role":"coordinator","answers":[0,0,0,0,0]})
  self.assertEqual(bad.status_code,400)
  good=self.client.post("/api/training/complete",headers=self.staff_auth,json={"learner_id":"demo-01","role":"coordinator","answers":["no","no","escalate","no","no"],"practical_passed":True})
  self.assertEqual(self.client.post("/api/training/complete",headers=self.auth,json={"learner_id":"demo-01","role":"coordinator","answers":["no","no","escalate","no","no"]}).status_code,403)
  self.assertEqual(good.status_code,201)
  self.assertFalse(good.json["passed"])
  approved=self.client.post("/api/training/complete",headers={**self.staff_auth,"X-Maya-Instructor-Token":"separate-instructor-secret-long"},json={"learner_id":"demo-01","role":"coordinator","answers":["no","no","escalate","no","no"],"practical_passed":True})
  self.assertEqual(approved.status_code,201)
  self.assertTrue(approved.json["passed"])
  records=self.client.get("/api/training/records",headers=self.staff_auth).json["records"]
  self.assertEqual(self.client.get("/api/training/records",headers=self.auth).status_code,403)
  self.assertEqual(self.client.get("/api/training/supervisor-records",headers=self.auth).status_code,403)
  supervisor={**self.auth,"X-Maya-Supervisor-Token":"synthetic-supervisor-secret-long"}
  self.assertEqual(self.client.get("/api/training/supervisor-records",headers=supervisor).status_code,200)
  with academy.connect() as conn:
   audit=conn.execute("SELECT actor_id,action FROM access_audit").fetchall()
  self.assertEqual(len(audit),1)
  self.assertEqual(audit[0]["actor_id"],"demo-supervisor-01")
  self.assertEqual(self.client.post("/api/training/retention-cleanup",headers=self.auth).status_code,403)
  with academy.connect() as conn:
   conn.execute("UPDATE completions SET at=? WHERE learner_id=?",("2020-01-01T00:00:00+00:00","demo-01"))
  cleanup=self.client.post("/api/training/retention-cleanup",headers=supervisor)
  self.assertEqual(cleanup.status_code,200)
  self.assertEqual(cleanup.json["deleted"],2)
  self.assertEqual(self.client.get("/api/training/records",headers=self.staff_auth).json["records"],[])
  self.assertEqual(records[0]["instructor_id"],"demo-instructor-01")
  self.assertIsNone(records[1]["instructor_id"])
  self.assertEqual(self.client.get("/api/training/records",headers=self.auth).status_code,403)
  with academy.connect() as conn:
   cleanup_audit=conn.execute("SELECT action FROM access_audit WHERE action LIKE ?",("retention_cleanup_deleted_%",)).fetchall()
  self.assertEqual(len(cleanup_audit),1)
  self.assertEqual(cleanup_audit[0]["action"],"retention_cleanup_deleted_2")
if __name__=="__main__":unittest.main()
