import pytest

from src.sovereign.authorization_gate import (
    AuthorizationDenied, AuthorizationGate, bind_capability,
)


ATTESTATION = {"status": "verified", "measurement": "known-good"}


def capability():
    return bind_capability("t1", "operator", ["network.connect"], 200, ATTESTATION)


def test_consequential_action_requires_every_control():
    gate = AuthorizationGate()
    gate.authorize(
        actor="operator", operation="network.connect", capability=capability(),
        platform_attestation=ATTESTATION, approvers=["a", "b"], now=100,
    )
    assert gate.audit_log[-1]["permitted"] is True


@pytest.mark.parametrize("changes", [
    {"approvers": ["a"]},
    {"operation": "firmware.bypass"},
    {"platform_attestation": {"status": "unverified"}},
    {"now": 200},
])
def test_gate_fails_closed(changes):
    args = dict(
        actor="operator", operation="network.connect", capability=capability(),
        platform_attestation=ATTESTATION, approvers=["a", "b"], now=100,
    )
    args.update(changes)
    with pytest.raises(AuthorizationDenied):
        AuthorizationGate().authorize(**args)


def test_emergency_freeze_is_independent_and_audited():
    gate = AuthorizationGate()
    gate.emergency_freeze("safety-officer", "test")
    with pytest.raises(AuthorizationDenied):
        gate.authorize(
            actor="operator", operation="network.connect", capability=capability(),
            platform_attestation=ATTESTATION, approvers=["a", "b"], now=100,
        )
    assert gate.audit_log[0]["operation"] == "emergency_freeze"
    assert gate.audit_log[-1]["reason"] == "system is independently frozen"
