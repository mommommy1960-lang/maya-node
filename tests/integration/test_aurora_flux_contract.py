import unittest

from aurora.integration.flux_drive_bridge import (
    AuroraCommand,
    AuroraFluxBridge,
    FluxDriveStatus,
)


class AuroraFluxContractTests(unittest.TestCase):
    def setUp(self):
        self.bridge = AuroraFluxBridge()
        self.safe = FluxDriveStatus(mode="SAFE", audit_status="PASS")

    def test_approved_command_is_accepted_for_simulation_only(self):
        decision = self.bridge.evaluate(
            AuroraCommand(1, 0.10, 0.05, -3.0, human_approved=True),
            self.safe,
        )
        self.assertTrue(decision.accepted)
        self.assertTrue(decision.command["simulation_only"])

    def test_unapproved_command_is_rejected(self):
        decision = self.bridge.evaluate(
            AuroraCommand(1, 0.10, 0.05, -3.0),
            self.safe,
        )
        self.assertFalse(decision.accepted)
        self.assertEqual(decision.reason, "human_approval_required")

    def test_flux_trip_blocks_command(self):
        status = FluxDriveStatus(mode="SAFE", safety_trip=True)
        decision = self.bridge.evaluate(
            AuroraCommand(1, 0.10, 0.05, -3.0, human_approved=True),
            status,
        )
        self.assertFalse(decision.accepted)
        self.assertEqual(decision.reason, "flux_drive_not_safe")

    def test_limits_block_command(self):
        decision = self.bridge.evaluate(
            AuroraCommand(1, 0.40, 0.05, -3.0, human_approved=True),
            self.safe,
        )
        self.assertFalse(decision.accepted)
        self.assertEqual(decision.reason, "acoustic_limit")


if __name__ == "__main__":
    unittest.main()
