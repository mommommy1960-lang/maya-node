#!/usr/bin/env python3
"""Bounded Consent Token demonstrator.

This is a local, non-networked demonstration of the current Maya Node token
manager. It records pass/fail observations for grant, deny-by-mismatch,
single-use consumption, replay rejection, expiry, and revocation.

It does not perform external actions and does not claim production readiness.
"""
from __future__ import annotations

import json
import time
from dataclasses import asdict

from src.sovereign.consent_tokens import ConsentScope, ConsentStatus, ConsentTokenManager


def snapshot(manager: ConsentTokenManager, token_id: str) -> dict:
    token = manager.get_token(token_id)
    return {
        "token_id": token_id,
        "status": token.status.value if token else None,
    }


def check(name: str, observed: bool, details: dict) -> dict:
    return {"name": name, "pass": bool(observed), "details": details}


def main() -> int:
    manager = ConsentTokenManager(secret_key="demo-only-secret")
    results = []

    token = manager.generate_token(
        user_id="demo-user",
        operation="demo.read",
        scope=ConsentScope.SINGLE_OPERATION,
        ttl_seconds=30,
        metadata={"purpose": "local demonstrator"},
    )
    results.append(check(
        "grant_and_verify",
        manager.verify_token(token),
        snapshot(manager, token.token_id),
    ))

    wrong_operation = manager.generate_token(
        user_id="demo-user",
        operation="demo.write",
        scope=ConsentScope.SINGLE_OPERATION,
        ttl_seconds=30,
    )
    # The current manager binds the operation into the signed token. This
    # negative path demonstrates that a different signed operation is not
    # interchangeable with the original token.
    results.append(check(
        "different_operation_is_distinct",
        wrong_operation.operation != token.operation
        and wrong_operation.signature != token.signature,
        {"original": token.operation, "other": wrong_operation.operation},
    ))

    first_use = manager.use_token(token.token_id)
    second_use = manager.use_token(token.token_id)
    results.append(check(
        "single_use_replay_rejected",
        first_use is True and second_use is False,
        snapshot(manager, token.token_id),
    ))

    expiring = manager.generate_token(
        user_id="demo-user",
        operation="demo.expire",
        scope=ConsentScope.SINGLE_OPERATION,
        ttl_seconds=1,
    )
    time.sleep(1.1)
    results.append(check(
        "expiry_rejected",
        manager.verify_token(expiring) is False
        and manager.get_token(expiring.token_id).status == ConsentStatus.EXPIRED,
        snapshot(manager, expiring.token_id),
    ))

    revocable = manager.generate_token(
        user_id="demo-user",
        operation="demo.revoke",
        scope=ConsentScope.SESSION,
        ttl_seconds=30,
    )
    revoked = manager.revoke_token(revocable.token_id)
    results.append(check(
        "revocation_rejected",
        revoked is True and manager.verify_token(revocable) is False,
        snapshot(manager, revocable.token_id),
    ))

    output = {
        "demonstrator": "Maya Node Consent Token",
        "network_access": False,
        "external_actions": False,
        "results": results,
        "passed": sum(1 for item in results if item["pass"]),
        "total": len(results),
        "limitations": [
            "This uses the current in-memory manager.",
            "Freeze/restore and append-only audit verification remain explicit next gates.",
            "Passing this demonstration does not establish production readiness.",
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if all(item["pass"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
