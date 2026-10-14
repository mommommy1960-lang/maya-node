"""Synthetic fixtures inspired by official records; not historical replays."""
import unittest
from demos.accountability_demo import Demo, Grant


class PublicRecordScenarios(unittest.TestCase):
    def test_addon_needs_its_own_authority(self):
        # FTC ABCmouse complaint: base/add-on cancellation confusion.
        d = Demo()
        d.grants.append(Grant("CUSTOMER", "charge", "BASE", 100, True))
        self.assertFalse(d.attempt("CUSTOMER", "charge", "ADDON", 1)["allowed"])
        # Separately valid authority must not be silently equated to the base grant.
        d.grants.append(Grant("CUSTOMER", "charge", "ADDON", 100))
        self.assertTrue(d.attempt("CUSTOMER", "charge", "ADDON", 2)["allowed"])

    def test_resubmitted_revoked_charge_stays_blocked(self):
        # CFPB 1005.10 official interpretation: resubmitted debit after stop.
        d = Demo(); d.grants.append(Grant("CUSTOMER", "charge", "PAYEE", 100, True))
        for now in (1, 2, 3):
            self.assertFalse(d.attempt("CUSTOMER", "charge", "PAYEE", now)["allowed"])
        self.assertEqual(len(d.cases), 3)  # Deduplicated incident grouping remains a gap.

    def test_educational_scope_does_not_authorize_advertising(self):
        # FTC Edmodo record: consent/authorization purpose boundary.
        d = Demo(); d.grants.append(Grant("PROVIDER", "education", "SYNTHETIC-DATA", 100))
        self.assertTrue(d.attempt("PROVIDER", "education", "SYNTHETIC-DATA", 1)["allowed"])
        self.assertFalse(d.attempt("PROVIDER", "advertising", "SYNTHETIC-DATA", 2)["allowed"])

    def test_known_incident_stays_open_until_independent_review(self):
        d = Demo(); cid = d.attempt("CUSTOMER", "charge", "ADDON", 1)["case_id"]
        d.correct(cid, d.primary, "Synthetic cancellation evidence")
        self.assertNotEqual(d.cases[cid]["status"], "resolved")
        d.verify(cid, d.lead, False)
        self.assertEqual(d.cases[cid]["status"], "review_required")


if __name__ == "__main__": unittest.main()
