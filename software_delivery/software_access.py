"""Server-only access core. HTTP authentication and Stripe verification are adapters.

Never expose these methods directly to a browser. Subjects must come from verified
identity; timestamps must come from the server. This module neither charges cards
nor connects Maya to customer systems.
"""
import sqlite3

TRIAL_SECONDS = 3600


class AccessStore:
    def __init__(self, path):
        self.db = sqlite3.connect(path, timeout=10, isolation_level=None)
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS accounts(
          subject TEXT PRIMARY KEY, trial_start INTEGER NOT NULL,
          trial_end INTEGER NOT NULL, suspended INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS orders(
          order_id TEXT PRIMARY KEY, subject TEXT NOT NULL,
          access_until INTEGER NOT NULL, revoked INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS revocations(order_id TEXT PRIMARY KEY);
        """)

    @staticmethod
    def validate(subject, now):
        if not isinstance(subject, str) or not 1 <= len(subject) <= 200:
            raise ValueError('Verified identity required')
        if type(now) is not int or now < 0:
            raise ValueError('Server timestamp required')

    def start_trial(self, subject, now):
        self.validate(subject, now)
        self.db.execute('INSERT INTO accounts(subject,trial_start,trial_end) '
                        'VALUES(?,?,?) ON CONFLICT(subject) DO NOTHING',
                        (subject, now, now + TRIAL_SECONDS))
        return self.status(subject, now)

    def status(self, subject, now):
        self.validate(subject, now)
        row = self.db.execute('SELECT trial_start,trial_end,suspended FROM accounts '
                              'WHERE subject=?', (subject,)).fetchone()
        if row and row[2]:
            return {'allowed': False, 'reason': 'suspended', 'expires_at': None}
        paid = self.db.execute('SELECT MAX(access_until) FROM orders '
                               'WHERE subject=? AND revoked=0', (subject,)).fetchone()[0]
        if paid is not None and now < paid:
            return {'allowed': True, 'reason': 'paid', 'expires_at': paid}
        if row and row[0] <= now < row[1]:
            return {'allowed': True, 'reason': 'trial', 'expires_at': row[1]}
        return {'allowed': False, 'reason': 'expired' if row else 'not_started',
                'expires_at': row[1] if row else None}

    def grant_verified_order(self, subject, now, *, order_id, access_until):
        """Call ONLY after raw webhook signature + exact configured price/product,
        currency, paid status, account and server-created subject mapping validate.
        A success-page redirect or a user-supplied checkout ID is never sufficient.
        Access duration is an explicit product term, not assumed to be monthly.
        """
        self.validate(subject, now)
        if not isinstance(order_id, str) or not 1 <= len(order_id) <= 200:
            raise ValueError('Verified order required')
        if type(access_until) is not int or access_until <= now:
            raise ValueError('Explicit future expiry required')
        self.db.execute('BEGIN IMMEDIATE')
        try:
            old = self.db.execute('SELECT subject,access_until FROM orders WHERE order_id=?',
                                  (order_id,)).fetchone()
            if old and old != (subject, access_until):
                raise ValueError('Order conflict')
            revoked = bool(self.db.execute('SELECT 1 FROM revocations WHERE order_id=?',
                                           (order_id,)).fetchone())
            self.db.execute('INSERT INTO orders VALUES(?,?,?,?) ON CONFLICT(order_id) DO NOTHING',
                            (order_id, subject, access_until, int(revoked)))
            self.db.execute('COMMIT')
        except Exception:
            self.db.execute('ROLLBACK')
            raise
        return self.status(subject, now)

    def revoke_verified_order(self, order_id):
        """Authenticated refund/dispute/cancellation adapter; blocks late replay."""
        if not isinstance(order_id, str) or not 1 <= len(order_id) <= 200:
            raise ValueError('Verified order required')
        self.db.execute('BEGIN IMMEDIATE')
        try:
            self.db.execute('INSERT INTO revocations VALUES(?) ON CONFLICT DO NOTHING', (order_id,))
            self.db.execute('UPDATE orders SET revoked=1 WHERE order_id=?', (order_id,))
            self.db.execute('COMMIT')
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def require_access(self, subject, now):
        result = self.status(subject, now)
        if not result['allowed']:
            raise PermissionError(result['reason'])
        return result
