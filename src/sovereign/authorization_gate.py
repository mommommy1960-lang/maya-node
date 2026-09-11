"""Fail-closed authorization gate for consequential Maya Node operations."""
from __future__ import annotations

import hashlib
import hmac
import json
import time
from dataclasses import dataclass, field, replace
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
    signature: str


def _capability_bytes(capability: Capability) -> bytes:
    payload = {
        "token_id": capability.token_id,
        "actor": capability.actor,
        "operations": sorted(capability.operations),
        "expires_at": capability.expires_at,
        "attestation_hash": capability.attestation_hash,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sign(capability: Capability, issuer_key: bytes) -> str:
    if len(issuer_key) < 32:
        raise ValueError("issuer key must contain at least 32 bytes")
    return hmac.new(issuer_key, _capability_bytes(capability), hashlib.sha256).hexdigest()


@dataclass
class AuthorizationGate:
    required_approvals: int = 2
    frozen: bool = False
    audit_log: list[dict] = field(default_factory=list)
    revoked_token_ids: set[str] = field(default_factory=set)

    def emergency_freeze(self, actor: str, reason: str) -> None:
        self.frozen = True
        self._record(actor, "emergency_freeze", False, reason)

    def revoke(self, token_id: str, actor: str = "security") -> None:
        self.revoked_token_ids.add(token_id)
        self._record(actor, "capability_revoke", False, token_id)

    def authorize(
        self,
        *,
        actor: str,
        operation: str,
        capability: Capability | None,
        issuer_key: bytes,
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
        elif len(issuer_key) < 32:
            reason = "issuer key is invalid"
        elif not hmac.compare_digest(capability.signature, _sign(capability, issuer_key)):
            reason = "capability signature is invalid"
        elif capability.token_id in self.revoked_token_ids:
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
            "sequence": len(self.audit_log), "timestamp": time.time(),
            "actor": actor, "operation": operation, "permitted": permitted,
            "reason": reason, "previous_hash": previous,
        }
        entry["hash"] = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode("utf-8")
        ).hexdigest()
        self.audit_log.append(entry)

    def verify_audit(self) -> bool:
        previous = "0" * 64
        for sequence, stored in enumerate(self.audit_log):
            entry = dict(stored)
            digest = entry.pop("hash", "")
            if entry.get("sequence") != sequence or entry.get("previous_hash") != previous:
                return False
            expected = hashlib.sha256(
                json.dumps(entry, sort_keys=True).encode("utf-8")
            ).hexdigest()
            if not hmac.compare_digest(digest, expected):
                return False
            previous = digest
        return True


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
    issuer_key: bytes,
) -> Capability:
    if not token_id or not actor:
        raise ValueError("token_id and actor are required")
    operation_set = frozenset(operations)
    if not operation_set:
        raise ValueError("at least one operation is required")
    unsigned = Capability(
        token_id, actor, operation_set, expires_at, _attestation_hash(attestation), ""
    )
    return replace(unsigned, signature=_sign(unsigned, issuer_key))
