# SPDX-License-Identifier: CERL-1.0
"""1000-case defensive contingency campaign.

The first 100 cases are the established adaptive red-team suite. Cases 101-1000
are deterministic malicious mutations generated across consent-token and ledger
trust boundaries. This is regression/stress evidence, not a claim of universal
security or 1000 unique vulnerability classes.
"""
import copy
import unittest

from src.sovereign.consent_tokens import ConsentTokenManager, ConsentScope
from src.services.ledger.ledger import ImmutableLedger
from tests.security.test_adaptive_redteam_100 import TestAdaptiveRedTeam100


class TestContingencyCampaign900(unittest.TestCase):
    """Nine hundred additional deterministic adversarial mutations."""

    def _manager(self):
        return ConsentTokenManager(secret_key="contingency-campaign-key")

    def _token(self, manager):
        return manager.generate_token(
            user_id="alice", operation="op.read",
            scope=ConsentScope.SINGLE_OPERATION, ttl_seconds=300,
            metadata={"purpose": "campaign", "level": 1},
        )

    def _ledger(self):
        ledger = ImmutableLedger()
        for i in range(8):
            ledger.append(f"op.{i}", {"value": i, "owner": "alice"})
        return ledger


def _token_case(n):
    def test(self):
        m = self._manager()
        t = self._token(m)
        mode = n % 12
        marker = f"attack-{n}"
        if mode == 0: t.user_id = marker
        elif mode == 1: t.operation = marker
        elif mode == 2: t.signature = marker
        elif mode == 3: t.expires_at += n
        elif mode == 4: t.timestamp -= n
        elif mode == 5: t.metadata[marker] = True
        elif mode == 6: t.metadata["level"] = n
        elif mode == 7: t.token_id = marker
        elif mode == 8: t.scope = ConsentScope.SESSION
        elif mode == 9: t.signature = t.signature[::-1]
        elif mode == 10: t.metadata["purpose"] = marker
        else: t.operation = "*"
        self.assertFalse(m.verify_token(t), f"mutation {n} was accepted")
    return test


def _ledger_case(n):
    def test(self):
        l = self._ledger()
        idx = 1 + (n % (len(l.entries) - 1))
        e = l.entries[idx]
        mode = n % 10
        if mode == 0: e.data["value"] = -n
        elif mode == 1: e.operation = f"evil.{n}"
        elif mode == 2: e.timestamp += n
        elif mode == 3: e.index += n
        elif mode == 4: e.previous_hash = "0" * 64
        elif mode == 5: e.entry_hash = "f" * 64
        elif mode == 6: l.entries.pop(idx)
        elif mode == 7:
            e.data["owner"] = "mallory"
            e.entry_hash = l._compute_hash(e)
        elif mode == 8: l.entries.insert(idx, copy.deepcopy(e))
        else: l.entries[0].data[f"forged-{n}"] = True
        self.assertFalse(l.verify_integrity(), f"ledger mutation {n} was accepted")
    return test


# 450 token mutations + 450 ledger mutations = 900 additional cases.
for i in range(101, 551):
    setattr(TestContingencyCampaign900, f"test_{i:04d}_token_mutation", _token_case(i))
for i in range(551, 1001):
    setattr(TestContingencyCampaign900, f"test_{i:04d}_ledger_mutation", _ledger_case(i))

# Keep the established first 100 discoverable in this campaign module as well.
EstablishedAdaptiveRedTeam100 = TestAdaptiveRedTeam100
