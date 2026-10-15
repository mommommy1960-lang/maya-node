import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEMO = ROOT / "demos" / "database_browser_demo.html"


class DatabaseBrowserDemoContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = DEMO.read_text(encoding="utf-8")
        match = re.search(r"<script>(.*?)</script>", cls.html, re.DOTALL)
        if not match:
            raise AssertionError("Demo must contain its inline JavaScript")
        cls.js = match.group(1)

    def test_all_four_customer_workflows_are_present(self):
        for sector in ("school", "bank", "nonprofit", "support"):
            with self.subTest(sector=sector):
                self.assertRegex(self.js, rf"(?m)^\s*{sector}:\s*\{{")
                self.assertIn(f'id="{sector}"', self.html)

    def test_demo_discloses_synthetic_data_and_no_live_integration(self):
        self.assertIn("invented records", self.html)
        self.assertIn("do not connect to a real organization", self.html)
        self.assertIn("Notifications and acknowledgment are simulated.", self.html)
        self.assertIn("No personal information is requested or transmitted.", self.html)

    def test_permission_gate_does_not_treat_ai_approval_as_authority(self):
        self.assertIn("const allowed=action==='read_summary'&&!state.revoked", self.js)
        self.assertIn("ai_approval:true", self.js)
        self.assertIn("AI approval is present, but human permission is absent", self.js)

    def test_excessive_export_is_not_an_allowed_action(self):
        self.assertIn("el('scope').onclick=()=>run('bulk_export')", self.js)
        self.assertIn("action==='read_summary'", self.js)

    def test_revocation_and_correction_review_are_distinct_steps(self):
        self.assertIn("function revoke(state)", self.js)
        self.assertIn("state.revoked=true", self.js)
        self.assertIn("function correct(state)", self.js)
        self.assertIn("DEMO-SEPARATE-REVIEWER", self.js)
        self.assertIn("correction.reviewed", self.js)

    def test_controls_have_status_feedback_and_keyboard_focus(self):
        self.assertIn('role="status" aria-live="polite"', self.html)
        self.assertIn("button:focus-visible,a:focus-visible", self.html)
        for control in ("allowed", "scope", "revoked", "correct", "reset"):
            self.assertIn(f'id="{control}"', self.html)

    def test_reset_reinitializes_the_selected_sector(self):
        self.assertIn("function reset(sector=state.sector)", self.js)
        self.assertIn("el('reset').onclick=()=>reset()", self.js)


if __name__ == "__main__":
    unittest.main(verbosity=2)
