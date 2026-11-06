import os
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from software_access import AccessStore


class AccessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.temp.name, 'access.sqlite')
        self.store = AccessStore(self.path)

    def tearDown(self):
        self.store.db.close()
        self.temp.cleanup()

    def test_hour_and_exact_boundary(self):
        self.assertEqual(self.store.start_trial('alice', 100)['expires_at'], 3700)
        self.assertTrue(self.store.status('alice', 3699)['allowed'])
        self.assertFalse(self.store.status('alice', 3700)['allowed'])
        with self.assertRaises(PermissionError):
            self.store.require_access('alice', 3700)

    def test_restart_cannot_renew_trial(self):
        self.store.start_trial('alice', 100)
        other = AccessStore(self.path)
        try:
            self.assertEqual(other.start_trial('alice', 4000)['expires_at'], 3700)
            self.assertFalse(other.status('alice', 4000)['allowed'])
        finally:
            other.db.close()

    def test_concurrent_start_has_one_expiry(self):
        def start(now):
            store = AccessStore(self.path)
            try:
                return store.start_trial('alice', now)['expires_at']
            finally:
                store.db.close()
        with ThreadPoolExecutor(max_workers=8) as pool:
            values = list(pool.map(start, range(100, 120)))
        self.assertEqual(len(set(values)), 1)

    def test_payment_bound_to_customer_and_expiry(self):
        self.store.grant_verified_order('alice', 100, order_id='order1', access_until=5000)
        self.assertEqual(self.store.require_access('alice', 4000)['reason'], 'paid')
        self.assertFalse(self.store.status('bob', 4000)['allowed'])
        self.assertFalse(self.store.status('alice', 5000)['allowed'])

    def test_duplicate_payment_does_not_extend(self):
        for _ in range(2):
            self.store.grant_verified_order('alice', 100, order_id='order1', access_until=5000)
        with self.assertRaises(ValueError):
            self.store.grant_verified_order('alice', 200, order_id='order1', access_until=5100)
        with self.assertRaises(ValueError):
            self.store.grant_verified_order('bob', 200, order_id='order1', access_until=5000)
        self.assertEqual(self.store.status('alice', 200)['expires_at'], 5000)

    def test_refund_before_payment_cannot_resurrect_order(self):
        self.store.revoke_verified_order('order1')
        self.store.grant_verified_order('alice', 100, order_id='order1', access_until=5000)
        self.assertFalse(self.store.status('alice', 100)['allowed'])

    def test_refund_after_payment_and_replay(self):
        self.store.grant_verified_order('alice', 100, order_id='order1', access_until=5000)
        self.store.revoke_verified_order('order1')
        self.store.grant_verified_order('alice', 100, order_id='order1', access_until=5000)
        self.assertFalse(self.store.status('alice', 100)['allowed'])

    def test_invalid_identity_clock_and_terms(self):
        for subject, now in [('',100), ('alice',True), ('alice',-1), (None,100)]:
            with self.assertRaises(ValueError):
                self.store.start_trial(subject, now)
        for expiry in [100,99,True,None]:
            with self.assertRaises(ValueError):
                self.store.grant_verified_order('alice',100,order_id='order1',access_until=expiry)

    def test_missing_identity_is_denied_and_clock_before_start(self):
        self.assertFalse(self.store.status('unknown',100)['allowed'])
        self.store.start_trial('alice',100)
        self.assertFalse(self.store.status('alice',99)['allowed'])

    def test_suspension_overrides_paid_access(self):
        self.store.start_trial('alice',100)
        self.store.grant_verified_order('alice',100,order_id='order1',access_until=5000)
        self.store.db.execute('UPDATE accounts SET suspended=1 WHERE subject=?',('alice',))
        self.assertEqual(self.store.status('alice',200)['reason'],'suspended')


if __name__ == '__main__':
    unittest.main()
