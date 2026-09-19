import unittest

from src.services.ledger.ledger import ImmutableLedger
from src.sovereign.consent_tokens import ConsentScope, ConsentStatus, ConsentTokenManager


class ConsentTokenDemonstratorTests(unittest.TestCase):
    def setUp(self):
        self.manager = ConsentTokenManager(secret_key="test-only-secret")

    def test_single_use_replay_is_rejected(self):
        token = self.manager.generate_token("u", "demo.read")
        self.assertTrue(self.manager.use_token(token.token_id))
        self.assertFalse(self.manager.use_token(token.token_id))
        self.assertEqual(self.manager.get_token(token.token_id).status, ConsentStatus.USED)

    def test_revocation_is_fail_closed(self):
        token = self.manager.generate_token("u", "demo.read", ConsentScope.SESSION)
        self.assertTrue(self.manager.revoke_token(token.token_id))
        self.assertFalse(self.manager.verify_token(token))

    def test_freeze_requires_fresh_restore_authorization(self):
        token = self.manager.generate_token("u", "demo.read", ConsentScope.SESSION)
        self.assertTrue(self.manager.freeze_token(token.token_id))
        self.assertFalse(self.manager.verify_token(token))

        wrong = self.manager.generate_token("u", "other.restore", ConsentScope.SINGLE_OPERATION)
        self.assertFalse(self.manager.restore_token(token.token_id, wrong))

        fresh = self.manager.generate_token(
            "u", f"restore:{token.token_id}", ConsentScope.SINGLE_OPERATION
        )
        self.assertTrue(self.manager.restore_token(token.token_id, fresh))
        self.assertTrue(self.manager.verify_token(token))

    def test_append_only_ledger_integrity(self):
        ledger = ImmutableLedger()
        ledger.append("token.issued", {"token_id": "one"})
        ledger.append("token.revoked", {"token_id": "one"})
        self.assertTrue(ledger.verify_integrity())

        ledger.entries[1].data["token_id"] = "tampered"
        self.assertFalse(ledger.verify_integrity())


if __name__ == "__main__":
    unittest.main()
