import copy
import unittest

from aurora.sim.replay import replay_commands


TRACE = [
    {"action": "consent", "token": "AURORA_SIM_CONSENT_V1"},
    {"action": "arm"},
    {"action": "command", "acoustic_duty": 0.10, "rf_duty": 0.05, "rf_dbm": -3.0},
    {"action": "step", "temperature_delta_c": 1.0},
    {"action": "step", "temperature_delta_c": 2.0},
]


class AuroraReplayTests(unittest.TestCase):
    def test_same_trace_produces_identical_snapshot(self):
        first = replay_commands(TRACE)
        second = replay_commands(TRACE)
        self.assertEqual(first, second)
        self.assertTrue(first["telemetry"])

    def test_replay_is_fail_closed_on_limit_violation(self):
        trace = TRACE + [
            {"action": "command", "acoustic_duty": 0.40, "rf_duty": 0.0, "rf_dbm": -3.0}
        ]
        result = replay_commands(trace)
        self.assertEqual(result["state"]["mode"], "SAFE")
        self.assertFalse(result["state"]["rail_powered"])

    def test_tamper_is_detected_by_hash_chain(self):
        result = replay_commands(TRACE)
        tampered = copy.deepcopy(result)
        tampered["telemetry"][2]["state"]["temperature_c"] = 999.0

        # Rebuild a verifier-only object without performing any physical action.
        from aurora.vessel_sim import AuroraVesselSim
        vessel = AuroraVesselSim()
        vessel.telemetry = tampered["telemetry"]
        self.assertFalse(vessel.verify_telemetry_chain())


if __name__ == "__main__":
    unittest.main()
