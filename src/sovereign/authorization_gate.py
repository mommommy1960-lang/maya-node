"""Fail-closed authorization gate for consequential Maya Node operations."""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Iterable


class AuthorizationDenied(PermissionError):
    pass


@dataclass(frozen=True)
class Capability:
    token_id: str
    actor: str
    operations: frozenset[str]
    expires_at: float
    attestation_hash: str
    revoked: bool = False


@dataclass
class AuthorizationGate:
    required_approvals: int = 2
    frozen: bool = False
    audit_log: list[dict] = field(default_factory=list)

    def emergency_freeze(self, actor: str, reason: str) -> None:
        self.frozen = True
        self._record(actor, "emergency_freeze", False, reason)

    def authorize(
        self,
        *,
        actor: str,
        operation: str,
        capability: Capability | None,
        platform_attestation: dict,
        approvers: Iterable[str] = (),
        now: float | None = None,
    ) -> None:
        current = time.time() if now is None else now
        reason = ""
        if self.frozen:
            reason = "system is independently frozen"
        elif capability is None:
            reason = "missing capability"
        elif capability.revoked:
            reason = "capability revoked"
        elif capability.actor != actor:
            reason = "actor mismatch"
        elif current >= capability.expires_at:
            reason = "capability expired"
        elif operation not in capability.operations:
            reason = "operation outside capability scope"
        elif platform_attestation.get("status") != "verified":
            reason = "platform attestation is not verified"
        elif _attestation_hash(platform_attestation) != capability.attestation_hash:
            reason = "platform attestation does not match capability"
        elif len({item for item in approvers if item}) < self.required_approvals:
            reason = "insufficient independent approvals"

        if reason:
            self._record(actor, operation, False, reason)
            raise AuthorizationDenied(reason)
        self._record(actor, operation, True, "all authorization conditions satisfied")

    def _record(self, actor: str, operation: str, permitted: bool, reason: str) -> None:
        previous = self.audit_log[-1]["hash"] if self.audit_log else "0" * 64
        entry = {
            "timestamp": time.time(), "actor": actor, "operation": operation,
            "permitted": permitted, "reason": reason, "previous_hash": previous,
        }
        entry["hash"] = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode("utf-8")
        ).hexdigest()
        self.audit_log.append(entry)


def _attestation_hash(report: dict) -> str:
    return hashlib.sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def bind_capability(
    token_id: str,
    actor: str,
    operations: Iterable[str],
    expires_at: float,
    attestation: dict,
) -> Capability:
    return Capability(
        token_id, actor, frozenset(operations), expires_at,
        _attestation_hash(attestation),
    )
