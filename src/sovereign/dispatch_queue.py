# SPDX-License-Identifier: CERL-1.0
"""Durable dispatch gate. Call only from a trusted, authenticated controller."""
import json
import sqlite3
import uuid
from contextlib import contextmanager


class DispatchQueue:
    def __init__(self, path):
        self.path = str(path)
        with self._transaction() as db:
            db.execute('CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, payload TEXT NOT NULL, state TEXT NOT NULL, attempt TEXT, receipt TEXT)')
            db.execute('CREATE TABLE IF NOT EXISTS events (sequence INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL, event TEXT NOT NULL)')

    @contextmanager
    def _transaction(self):
        db = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        try:
            db.execute('PRAGMA synchronous=FULL')
            db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def _event(self, db, job_id, event):
        db.execute('INSERT INTO events(job_id,event) VALUES (?,?)', (job_id, event))

    def enqueue(self, job_id, payload):
        """Idempotent submission; changing an existing payload is rejected."""
        encoded = json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False)
        with self._transaction() as db:
            row = db.execute('SELECT payload FROM jobs WHERE id=?', (job_id,)).fetchone()
            if row:
                if row[0] != encoded:
                    raise ValueError('Changed payload requires a new job and new approval')
                return
            db.execute('INSERT INTO jobs VALUES (?,?,?,NULL,NULL)', (job_id, encoded, 'pending'))
            self._event(db, job_id, 'enqueued')

    def approve(self, job_id):
        """Trusted controller confirms approval for this exact immutable payload."""
        with self._transaction() as db:
            changed = db.execute("UPDATE jobs SET state='queued' WHERE id=? AND state='pending'", (job_id,)).rowcount
            if changed:
                self._event(db, job_id, 'approved')
            return bool(changed)

    def cancel(self, job_id):
        with self._transaction() as db:
            row = db.execute('SELECT state FROM jobs WHERE id=?', (job_id,)).fetchone()
            if not row:
                raise KeyError(job_id)
            if row[0] == 'canceled':
                return 'canceled'
            if row[0] not in ('pending', 'queued'):
                self._event(db, job_id, 'cancel_too_late')
                return 'too_late'
            db.execute("UPDATE jobs SET state='canceled' WHERE id=?", (job_id,))
            self._event(db, job_id, 'canceled')
            return 'canceled'

    def claim(self, job_id):
        """Commit dispatch once. Cancellation after this point is too late.

        No automatic reclaim: a crashed/timeout worker may have sent already.
        """
        with self._transaction() as db:
            row = db.execute('SELECT payload,state FROM jobs WHERE id=?', (job_id,)).fetchone()
            if not row:
                raise KeyError(job_id)
            if row[1] != 'queued':
                return None
            attempt = str(uuid.uuid4())
            db.execute("UPDATE jobs SET state='dispatch_committed',attempt=? WHERE id=?", (attempt, job_id))
            self._event(db, job_id, 'dispatch_committed')
            return attempt, json.loads(row[0])

    def complete(self, job_id, attempt, receipt=None, error=False):
        # Unknown outcomes stay blocked until a human reconciles provider state.
        state = 'unknown' if error else 'sent'
        encoded = json.dumps(receipt, sort_keys=True, allow_nan=False)
        with self._transaction() as db:
            changed = db.execute("UPDATE jobs SET state=?,receipt=? WHERE id=? AND attempt=? AND state='dispatch_committed'", (state, encoded, job_id, attempt)).rowcount
            if not changed:
                raise ValueError('Invalid or already completed attempt')
            self._event(db, job_id, state)

    def dispatch(self, job_id, sender):
        claim = self.claim(job_id)
        if claim is None:
            return 'blocked'
        attempt, payload = claim
        try:
            receipt = sender(payload)
        except Exception:
            self.complete(job_id, attempt, error=True)
            raise
        self.complete(job_id, attempt, receipt)
        return 'sent'

    def status(self, job_id):
        with self._transaction() as db:
            row = db.execute('SELECT state FROM jobs WHERE id=?', (job_id,)).fetchone()
            if not row:
                raise KeyError(job_id)
            return row[0]
