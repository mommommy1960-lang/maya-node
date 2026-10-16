import unittest
from unittest.mock import patch
from src.sovereign.consent_tokens import ConsentTokenManager, ConsentScope, ConsentStatus

class ConsentBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.manager = ConsentTokenManager(secret_key='test-only-boundary-key')

    def frozen_pair(self, scope=ConsentScope.SINGLE_OPERATION):
        token = self.manager.generate_token('fixture-user', 'demo.read', ConsentScope.SESSION)
        self.assertTrue(self.manager.freeze_token(token.token_id))
        fresh = self.manager.generate_token('fixture-user', f'restore:{token.token_id}', scope)
        return token, fresh

    def test_expiry_boundary_is_closed(self):
        token = self.manager.generate_token('fixture-user', 'demo.read')
        with patch('src.sovereign.consent_tokens.time.time', return_value=token.expires_at):
            self.assertFalse(self.manager.verify_token(token))

    def test_session_restore_authorization_is_rejected(self):
        token, fresh = self.frozen_pair(ConsentScope.SESSION)
        self.assertFalse(self.manager.restore_token(token.token_id, fresh))
        self.assertEqual(token.status, ConsentStatus.FROZEN)

    def test_batch_restore_authorization_is_rejected(self):
        token, fresh = self.frozen_pair(ConsentScope.BATCH)
        self.assertFalse(self.manager.restore_token(token.token_id, fresh))

    def test_expired_target_cannot_be_reactivated_or_consume_fresh_grant(self):
        token, fresh = self.frozen_pair()
        with patch('src.sovereign.consent_tokens.time.time', return_value=token.expires_at):
            self.assertFalse(self.manager.restore_token(token.token_id, fresh))
        self.assertEqual(fresh.status, ConsentStatus.ACTIVE)

    def test_fresh_restore_is_consumed_and_cannot_be_replayed(self):
        token, fresh = self.frozen_pair()
        self.assertTrue(self.manager.restore_token(token.token_id, fresh))
        self.assertEqual(fresh.status, ConsentStatus.USED)
        self.assertTrue(self.manager.freeze_token(token.token_id))
        self.assertFalse(self.manager.restore_token(token.token_id, fresh))

    def test_wrong_owner_cannot_restore(self):
        token, _ = self.frozen_pair()
        other = self.manager.generate_token('other-user', f'restore:{token.token_id}')
        self.assertFalse(self.manager.restore_token(token.token_id, other))

    def test_malformed_signature_is_denied(self):
        for value in [None, 42, '\N{SNOWMAN}', 'not-a-valid-signature']:
            with self.subTest(value=value):
                token = self.manager.generate_token('fixture-user', 'demo.read')
                token.signature = value
                self.assertFalse(self.manager.verify_token(token))

    def test_invalid_ttl_cannot_create_nonexpiring_or_empty_grants(self):
        for ttl in [0, -1, float('nan'), float('inf'), True, '300', None]:
            with self.subTest(ttl=ttl):
                with self.assertRaises(ValueError):
                    self.manager.generate_token('fixture-user', 'demo.read', ttl_seconds=ttl)

if __name__ == '__main__':
    unittest.main()
