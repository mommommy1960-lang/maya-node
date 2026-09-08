"""Deterministic, simulation-only Aurora vessel runtime.

This module deliberately has no hardware, network, RF, acoustic, or actuator I/O.
It turns the Aurora Mini-Vessel Blue Book safety envelope into a replayable test
surface for mission logic, consent gating, telemetry, and fail-closed behavior.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json
from typing import Dict, List


@dataclass(frozen=True)
class SafetyLimits:
    max_temperature_c: float = 55.0
    hard_reset_temperature_c: float = 65.0
    max_rf_dbm: float = 10.0
    max_acoustic_duty: float = 0.35
    max_rf_duty: float = 0.20


@dataclass(frozen=True)
class VesselState:
    tick: int = 0
    mode: str = "SAFE"
    acoustic_duty: float = 0.0
    rf_duty: float = 0.0
    rf_dbm: float = -100.0
    temperature_c: float = 22.0
    consent_valid: bool = False
    rail_powered: bool = False
    emergency_stop: bool = False
    last_reason: str = "boot"


class AuroraVesselSim:
    """Safe state machine for Aurora's simulation-only bring-up."""

    def __init__(self, limits: SafetyLimits | None = None) -> None:
        self.limits = limits or SafetyLimits()
        self.state = VesselState()
        self.telemetry: List[Dict[str, object]] = []
        self._previous_hash = "0" * 64
        self._record("boot")

    def _record(self, reason: str) -> None:
        event = {
            "tick": self.state.tick,
            "reason": reason,
            "state": asdict(self.state),
            "previous_hash": self._previous_hash,
        }
        digest = hashlib.sha256(
            json.dumps(event, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        event["hash"] = digest
        self.telemetry.append(event)
        self._previous_hash = digest

    def _fail_safe(self, reason: str) -> None:
        s = self.state
        self.state = VesselState(
            tick=s.tick,
            temperature_c=s.temperature_c,
            consent_valid=s.consent_valid,
            emergency_stop=reason == "emergency_stop",
            last_reason=reason,
        )
        self._record(reason)

    def grant_consent(self, token: str) -> bool:
        valid = token == "AURORA_SIM_CONSENT_V1"
        self.state = VesselState(
            **{**asdict(self.state), "consent_valid": valid, "last_reason": "consent_granted" if valid else "consent_denied"}
        )
        self._record(self.state.last_reason)
        return valid

    def arm(self) -> bool:
        if self.state.emergency_stop:
            self._fail_safe("latched_emergency_stop")
            return False
        if not self.state.consent_valid:
            self._fail_safe("consent_required")
            return False
        self.state = VesselState(**{**asdict(self.state), "mode": "ARMED", "last_reason": "armed"})
        self._record("armed")
        return True

    def set_command(self, acoustic_duty: float, rf_duty: float, rf_dbm: float) -> bool:
        if self.state.mode != "ARMED" or self.state.emergency_stop:
            self._fail_safe("command_rejected_not_armed")
            return False
        values = (acoustic_duty, rf_duty, rf_dbm)
        if not all(isinstance(v, (int, float)) for v in values):
            self._fail_safe("command_rejected_non_numeric")
            return False
        if not 0 <= acoustic_duty <= self.limits.max_acoustic_duty:
            self._fail_safe("acoustic_limit")
            return False
        if not 0 <= rf_duty <= self.limits.max_rf_duty:
            self._fail_safe("rf_duty_limit")
            return False
        if rf_dbm > self.limits.max_rf_dbm:
            self._fail_safe("rf_power_limit")
            return False
        self.state = VesselState(**{
            **asdict(self.state),
            "acoustic_duty": float(acoustic_duty),
            "rf_duty": float(rf_duty),
            "rf_dbm": float(rf_dbm),
            "rail_powered": acoustic_duty > 0 or rf_duty > 0,
            "last_reason": "command_accepted",
        })
        self._record("command_accepted")
        return True

    def step(self, temperature_delta_c: float = 0.0) -> VesselState:
        next_temp = self.state.temperature_c + float(temperature_delta_c)
        self.state = VesselState(**{**asdict(self.state), "tick": self.state.tick + 1, "temperature_c": next_temp})
        if next_temp > self.limits.hard_reset_temperature_c:
            self._fail_safe("hard_temperature_reset")
        elif next_temp > self.limits.max_temperature_c:
            self._fail_safe("thermal_trip")
        else:
            self._record("step")
        return self.state

    def emergency_stop_now(self) -> None:
        self._fail_safe("emergency_stop")

    def reset(self) -> bool:
        # Emergency stop is a deliberate latch; only a fresh process/operator
        # reset may clear it after the physical safety condition is reviewed.
        if self.state.emergency_stop or self.state.temperature_c > self.limits.max_temperature_c:
            return False
        self.state = VesselState(tick=self.state.tick, temperature_c=self.state.temperature_c, last_reason="reset")
        self._record("reset")
        return True

    def verify_telemetry_chain(self) -> bool:
        previous = "0" * 64
        for event in self.telemetry:
            unsigned = {k: v for k, v in event.items() if k != "hash"}
            if event["previous_hash"] != previous:
                return False
            expected = hashlib.sha256(
                json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()
            if event["hash"] != expected:
                return False
            previous = event["hash"]
        return True

    def snapshot(self) -> Dict[str, object]:
        return {"state": asdict(self.state), "telemetry": list(self.telemetry)}
