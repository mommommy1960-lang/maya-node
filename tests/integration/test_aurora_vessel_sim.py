import unittest

from aurora.vessel_sim import AuroraVesselSim


class AuroraVesselSimTests(unittest.TestCase):
    def test_consent_is_required_before_arm(self):
        vessel = AuroraVesselSim()
        self.assertFalse(vessel.arm())
        self.assertEqual(vessel.state.mode, "SAFE")

    def test_valid_consent_and_safe_command(self):
        vessel = AuroraVesselSim()
        self.assertTrue(vessel.grant_consent("AURORA_SIM_CONSENT_V1"))
        self.assertTrue(vessel.arm())
        self.assertTrue(vessel.set_command(0.10, 0.05, -3.0))
        self.assertTrue(vessel.state.rail_powered)

    def test_limits_fail_closed(self):
        vessel = AuroraVesselSim()
        vessel.grant_consent("AURORA_SIM_CONSENT_V1")
        vessel.arm()
        self.assertFalse(vessel.set_command(0.40, 0.05, -3.0))
        self.assertEqual(vessel.state.mode, "SAFE")
        self.assertFalse(vessel.state.rail_powered)

    def test_thermal_trip_cuts_rails(self):
        vessel = AuroraVesselSim()
        vessel.grant_consent("AURORA_SIM_CONSENT_V1")
        vessel.arm()
        vessel.set_command(0.10, 0.05, -3.0)
        vessel.step(34.0)
        self.assertEqual(vessel.state.mode, "SAFE")
        self.assertFalse(vessel.state.rail_powered)

    def test_emergency_stop_latches_until_reset(self):
        vessel = AuroraVesselSim()
        vessel.grant_consent("AURORA_SIM_CONSENT_V1")
        vessel.arm()
        vessel.emergency_stop_now()
        self.assertTrue(vessel.state.emergency_stop)
        self.assertFalse(vessel.arm())
        self.assertFalse(vessel.reset())

    def test_telemetry_hash_chain_is_replayable(self):
        vessel = AuroraVesselSim()
        vessel.grant_consent("AURORA_SIM_CONSENT_V1")
        vessel.arm()
        vessel.set_command(0.10, 0.05, -3.0)
        vessel.step(1.0)
        self.assertTrue(vessel.verify_telemetry_chain())


if __name__ == "__main__":
    unittest.main()
