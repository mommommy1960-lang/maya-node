"""Simulation-only Aurora-to-Flux Drive command contract.

This is an interface contract, not a physical actuator driver. It accepts
Aurora command proposals and returns a fail-closed decision based on human
approval, Aurora limits, and Flux Drive safety status.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Dict


@dataclass(frozen=True)
class AuroraCommand:
    sequence: int
    acoustic_duty: float
    rf_duty: float
    rf_dbm: float
    human_approved: bool = False


@dataclass(frozen=True)
class FluxDriveStatus:
    mode: str = "SAFE"
    safety_trip: bool = False
    emergency_stop: bool = False
    audit_status: str = "NO_DATA"
    telemetry_hash: str = ""


@dataclass(frozen=True)
class BridgeDecision:
    accepted: bool
    reason: str
    command: Dict[str, Any]


class AuroraFluxBridge:
    """Connects simulation messages without performing hardware I/O."""

    def __init__(self, max_acoustic_duty: float = 0.35, max_rf_duty: float = 0.20, max_rf_dbm: float = 10.0):
        self.max_acoustic_duty = max_acoustic_duty
        self.max_rf_duty = max_rf_duty
        self.max_rf_dbm = max_rf_dbm

    def evaluate(self, command: AuroraCommand, status: FluxDriveStatus) -> BridgeDecision:
        values = (command.acoustic_duty, command.rf_duty, command.rf_dbm)
        if command.sequence < 0 or not all(math.isfinite(float(v)) for v in values):
            return BridgeDecision(False, "invalid_command", {})
        if not command.human_approved:
            return BridgeDecision(False, "human_approval_required", {})
        if status.safety_trip or status.emergency_stop or status.mode != "SAFE":
            return BridgeDecision(False, "flux_drive_not_safe", {})
        if not 0 <= command.acoustic_duty <= self.max_acoustic_duty:
            return BridgeDecision(False, "acoustic_limit", {})
        if not 0 <= command.rf_duty <= self.max_rf_duty:
            return BridgeDecision(False, "rf_duty_limit", {})
        if command.rf_dbm > self.max_rf_dbm:
            return BridgeDecision(False, "rf_power_limit", {})
        payload = {
            "sequence": command.sequence,
            "acoustic_duty": command.acoustic_duty,
            "rf_duty": command.rf_duty,
            "rf_dbm": command.rf_dbm,
            "simulation_only": True,
        }
        return BridgeDecision(True, "accepted_for_simulation", payload)
