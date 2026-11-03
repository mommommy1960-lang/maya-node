import unittest
from src.sovereign.approval_gate import ApprovalGate, ApprovalStatus

class Clock:
    def __init__(self): self.now=100.0
    def __call__(self): return self.now

class ApprovalGateTests(unittest.TestCase):
    def setUp(self):
        self.clock=Clock()
        self.gate=ApprovalGate(lambda actor, req: actor=="human-reviewer",
                               clock=self.clock)
    def test_fails_closed_without_authorizer(self):
        gate=ApprovalGate(clock=self.clock)
        req=gate.request("release",{}, "critical")
        with self.assertRaises(PermissionError): gate.approve(req.request_id,"reviewer")
        self.assertEqual(gate.pending_requests()[0].status,ApprovalStatus.PENDING)
    def test_authorized_approval(self):
        req=self.gate.request("release",{}, "critical")
        self.assertTrue(self.gate.approve(req.request_id,"human-reviewer","reviewed"))
        self.assertEqual(self.gate.history_snapshot()[-1]["status"],"approved")
    def test_wrong_approver_rejected(self):
        req=self.gate.request("release",{})
        with self.assertRaises(PermissionError): self.gate.approve(req.request_id,"agent")
    def test_expiry_blocks_late_approval(self):
        req=self.gate.request("release",{},ttl=5)
        self.clock.now=105
        self.assertFalse(self.gate.approve(req.request_id,"human-reviewer"))
        self.assertEqual(self.gate.history_snapshot()[-1]["event"],"timeout")
    def test_override_cancels_and_blocks_new_requests(self):
        req=self.gate.request("release",{})
        self.gate.override("operator","safety stop")
        self.assertTrue(self.gate.halted)
        self.assertEqual(self.gate.pending_requests(),[])
        blocked=self.gate.request("other",{})
        self.assertEqual(blocked.status,ApprovalStatus.CANCELLED)
        with self.assertRaises(PermissionError): self.gate.resume("operator")
        self.gate.resume("human-reviewer",authorized=True)
        self.assertFalse(self.gate.halted)
    def test_rejection_requires_reason(self):
        req=self.gate.request("release",{})
        with self.assertRaises(ValueError): self.gate.reject(req.request_id,"human-reviewer","")
        self.assertTrue(self.gate.reject(req.request_id,"human-reviewer","policy mismatch"))

if __name__=="__main__": unittest.main()
