import os
import sqlite3
import tempfile
import unittest
from demos.accountability_sandbox import Sandbox


class SandboxTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.temp.name, "synthetic.db")
        self.key = b"test-only-key-never-use-for-real!!"
        self.s = Sandbox(self.path, self.key)
        self.customer = self.s.provision("DEMO-CUSTOMER", 300)
        self.owner = self.s.provision("DEMO-STAFF-1", 300)

    def tearDown(self):
        self.s.close(); self.temp.cleanup()

    def case(self):
        return self.s.request(self.customer, "attempt", 0, action="charge", resource="DEMO-SUB")["case_id"]

    def test_invalid_expired_revoked_and_spoofed_identity(self):
        for token, now in (("fake", 0), (self.customer, 300)):
            with self.assertRaises(PermissionError): self.s.request(token, "attempt", now)
        with self.assertRaises(PermissionError):
            self.s.request(self.customer, "attempt", 0, actor="DEMO-STAFF-1")
        self.s.revoke_session(self.customer)
        with self.assertRaises(PermissionError): self.s.authenticate(self.customer, 0)

    def test_restart_preserves_case_session_and_outbox(self):
        cid = self.case(); self.s.close(); self.s = Sandbox(self.path, self.key)
        self.assertEqual(self.s.request(self.customer, "view", 1, case_id=cid)["owner"], "DEMO-STAFF-1")
        rows = self.s.deliver_test_queue(lambda *args: True, 1)
        self.assertEqual(rows[0][1], "delivered")
        self.assertIsNone(self.s.model.cases[cid]["acknowledged"])

    def test_delivery_failure_retry_and_acknowledgment(self):
        cid = self.case()
        self.assertEqual(self.s.deliver_test_queue(lambda *args: False, 1)[0][1], "failed")
        calls = []
        self.s.deliver_test_queue(lambda *args: calls.append(args) or True, 2)
        self.s.deliver_test_queue(lambda *args: calls.append(args) or True, 3)
        self.assertEqual(len(calls), 1)
        self.s.request(self.owner, "acknowledge", 10, case_id=cid)
        self.assertEqual(self.s.deliver_test_queue(lambda *args: True, 11)[0][1], "acknowledged")

    def test_unrelated_session_cannot_read_case(self):
        cid = self.case(); stranger = self.s.provision("STRANGER", 300)
        with self.assertRaises(PermissionError): self.s.request(stranger, "export", 1, case_id=cid)

    def test_revocation_cancels_pending_advocate_delivery(self):
        cid = self.case(); advocate = self.s.provision("ADVOCATE", 300)
        self.s.request(self.customer, "grant_advocate", 1, case_id=cid, advocate="ADVOCATE", expires=20)
        self.s.request(self.customer, "revoke_advocate", 2, case_id=cid)
        calls = []
        self.s.deliver_test_queue(lambda *args: calls.append(args) or True, 3)
        self.assertNotIn("ADVOCATE", [x[2] for x in calls])
        with self.assertRaises(PermissionError): self.s.request(advocate, "view", 3, case_id=cid)

    def test_state_alteration_rejected_on_restart(self):
        self.case(); self.s.close()
        db = sqlite3.connect(self.path)
        db.execute("UPDATE state SET body='{}'"); db.commit(); db.close()
        with self.assertRaises(ValueError): Sandbox(self.path, self.key)
        # Restore a valid open instance for tearDown without accepting corrupted state.
        os.unlink(self.path); self.s = Sandbox(self.path, self.key)

    def test_write_failure_rolls_back_case_and_queue(self):
        original = self.s._save
        def fail(): raise OSError("Injected storage failure")
        self.s._save = fail
        with self.assertRaises(OSError): self.case()
        self.s._save = original
        self.assertEqual(self.s.model.cases, {})
        self.assertEqual(self.s.db.execute("SELECT count(*) FROM outbox").fetchone()[0], 0)


if __name__ == "__main__": unittest.main()
