import unittest
from demos.accountability_demo import Demo, Grant, walkthrough


class AccountabilityTests(unittest.TestCase):
    def test_wrong_ai_approval_has_no_authority(self):
        d = Demo()
        self.assertFalse(d.attempt("stranger", "pickup", "child", 0)["allowed"])

    def test_scope_expiry_and_revocation(self):
        for grant in (Grant("a", "pickup", "other", 100),
                      Grant("a", "pickup", "child", 0),
                      Grant("a", "pickup", "child", 100, True)):
            d = Demo(); d.grants.append(grant)
            self.assertFalse(d.attempt("a", "pickup", "child", 0)["allowed"])

    def test_revoke_before_execution(self):
        d = Demo(); g = Grant("a", "charge", "sub", 100); d.grants.append(g)
        self.assertTrue(d.authorized("a", "charge", "sub", 0))
        g.revoked = True
        self.assertFalse(d.attempt("a", "charge", "sub", 1)["allowed"])

    def test_handoff_must_be_accepted_and_current(self):
        d = Demo(); d.away = True
        self.assertIsNone(d.owner(0))
        with self.assertRaises(ValueError): d.accept_handoff("stranger", 0, 30)
        d.accept_handoff(d.backup, 0, 30)
        self.assertEqual(d.owner(29), d.backup)
        self.assertIsNone(d.owner(30))

    def test_missing_coverage_blocks_valid_permission(self):
        d = Demo(); d.away = True; d.grants.append(Grant("a", "pickup", "child", 100))
        r = d.attempt("a", "pickup", "child", 0)
        self.assertFalse(r["allowed"])
        self.assertEqual(d.cases[r["case_id"]]["owner"], d.lead)

    def test_unanswered_alert_escalates(self):
        d = Demo(); d.accept_handoff(d.backup, 0, 300)
        cid = d.attempt("a", "charge", "sub", 0)["case_id"]
        d.escalate(cid, 29); self.assertEqual(d.cases[cid]["owner"], d.primary)
        d.escalate(cid, 30); self.assertEqual(d.cases[cid]["owner"], d.backup)
        d.escalate(cid, 60); self.assertEqual(d.cases[cid]["owner"], d.lead)

    def test_actual_acknowledgment_target_boundary(self):
        for elapsed, expected in ((119, True), (120, False)):
            d = Demo(); cid = d.attempt("a", "charge", "sub", 0)["case_id"]
            self.assertEqual(d.acknowledge(cid, d.primary, elapsed), expected)

    def test_forged_acknowledgment_rejected(self):
        d = Demo(); cid = d.attempt("a", "charge", "sub", 0)["case_id"]
        with self.assertRaises(PermissionError): d.acknowledge(cid, "other", 1)
        self.assertIsNone(d.cases[cid]["acknowledged"])

    def test_advocate_access_is_case_specific(self):
        d = Demo(); cid = d.attempt("a", "charge", "sub", 0)["case_id"]
        with self.assertRaises(PermissionError): d.view(cid, "advocate")
        d.grant_advocate(cid, "a", "advocate")
        self.assertEqual(d.view(cid, "advocate")["id"], cid)
        other = d.attempt("b", "charge", "other", 0)["case_id"]
        with self.assertRaises(PermissionError): d.view(other, "advocate")

    def test_correction_needs_verification(self):
        d = Demo(); cid = d.attempt("a", "charge", "sub", 0)["case_id"]
        d.correct(cid, d.primary, "synthetic evidence")
        self.assertNotEqual(d.cases[cid]["status"], "resolved")
        with self.assertRaises(PermissionError): d.verify(cid, d.primary, True)
        d.verify(cid, d.lead, False)
        self.assertEqual(d.cases[cid]["status"], "review_required")

    def test_advocate_expiration_and_revocation(self):
        d = Demo(); cid = d.attempt("a", "charge", "sub", 0)["case_id"]
        d.grant_advocate(cid, "a", "advocate", expires=20)
        self.assertEqual(d.view(cid, "advocate", 19)["id"], cid)
        with self.assertRaises(PermissionError): d.view(cid, "advocate", 20)
        d.revoke_advocate(cid, "a")
        with self.assertRaises(PermissionError): d.view(cid, "advocate", 1)

    def test_export_does_not_leak_another_case(self):
        d = Demo(); first = d.attempt("a", "charge", "sub", 0)["case_id"]
        second = d.attempt("b", "charge", "private", 0)["case_id"]
        exported = d.export_case(first, "a")
        self.assertTrue(exported["events"])
        self.assertTrue(all(e["case_id"] == first for e in exported["events"]))
        with self.assertRaises(PermissionError): d.export_case(second, "a")

    def test_walkthrough_reports_simulation(self):
        result = walkthrough()
        self.assertIn("SIMULATION", result["scope"])
        self.assertEqual(result["advocate_view"]["status"], "resolved")


if __name__ == "__main__": unittest.main()
