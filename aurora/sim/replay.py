"""Deterministic replay helpers for Aurora simulation traces."""
from __future__ import annotations

from typing import Iterable, Mapping

from .vessel_sim import AuroraVesselSim


def replay_commands(commands: Iterable[Mapping[str, object]]) -> dict:
    """Replay a command sequence without hardware or network side effects."""
    vessel = AuroraVesselSim()
    for command in commands:
        action = command.get("action", "command")
        if action == "consent":
            vessel.grant_consent(str(command.get("token", "")))
        elif action == "arm":
            vessel.arm()
        elif action == "emergency_stop":
            vessel.emergency_stop_now()
        elif action == "step":
            vessel.step(float(command.get("temperature_delta_c", 0.0)))
        elif action == "command":
            vessel.set_command(
                float(command.get("acoustic_duty", 0.0)),
                float(command.get("rf_duty", 0.0)),
                float(command.get("rf_dbm", -100.0)),
            )
        else:
            vessel._fail_safe("unknown_replay_action")
    return vessel.snapshot()
