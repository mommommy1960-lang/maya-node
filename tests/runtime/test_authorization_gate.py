from dataclasses import replace
import pytest

from src.sovereign.authorization_gate import (
    AuthorizationDenied, AuthorizationGate, bind_capability,
)


ATTESTATION = {"status": "verified", "measurement": "known-good"}
KEY = b"k" * 32


def capability():
    return bind_capability(
        "t1", "operator", ["network.connect"], 200, ATTESTATION, KEY
    )


def args(**changes):
    values = dict(
        actor="operator", operation="network.connect", capability=capability(),
        issuer_key=KEY, platform_attestation=ATTESTATION,
        approvers=["a", "b"], now=100,
    )
    values.update(changes)
    return values


def test_consequential_action_requires_every_control():
    gate = AuthorizationGate()
    gate.authorize(**args())
    assert gate.audit_log[-1]["permitted"] is True
    assert gate.verify_audit() is True


@pytest.mark.parametrize("changes", [
    {"approvers": ["a"]},
    {"operation": "firmware.bypass"},
    {"platform_attestation": {"status": "unverified"}},
    {"now": 200},
    {"issuer_key": b"z" * 32},
])
def test_gate_fails_closed(changes):
    with pytest.raises(AuthorizationDenied):
        AuthorizationGate().authorize(**args(**changes))


def test_capability_field_forgery_breaks_signature():
    forged = replace(capability(), operations=frozenset({"firmware.bypass"}))
    with pytest.raises(AuthorizationDenied, match="signature"):
        AuthorizationGate().authorize(**args(
            operation="firmware.bypass", capability=forged
        ))


def test_revocation_is_external_and_immediate():
    gate = AuthorizationGate()
    gate.revoke("t1")
    with pytest.raises(AuthorizationDenied, match="revoked"):
        gate.authorize(**args())
    assert gate.verify_audit() is True


def test_emergency_freeze_is_independent_and_audited():
    gate = AuthorizationGate()
    gate.emergency_freeze("safety-officer", "test")
    with pytest.raises(AuthorizationDenied):
        gate.authorize(**args())
    assert gate.audit_log[0]["operation"] == "emergency_freeze"
    assert gate.audit_log[-1]["reason"] == "system is independently frozen"
    assert gate.verify_audit() is True


def test_audit_tampering_is_detected():
    gate = AuthorizationGate()
    gate.authorize(**args())
    gate.audit_log[0]["permitted"] = False
    assert gate.verify_audit() is False
