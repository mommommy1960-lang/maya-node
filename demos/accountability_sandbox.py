"""Local synthetic sandbox. No network server, identity provider or live transport."""
import hashlib
import hmac
import json
import secrets
import sqlite3
from demos.accountability_demo import Demo, Grant


class Sandbox:
    def __init__(self, path, integrity_key):
        if not isinstance(integrity_key, bytes) or len(integrity_key) < 32:
            raise ValueError("External integrity key of at least 32 bytes required")
        self.key = integrity_key
        self.db = sqlite3.connect(path)
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS state(id INTEGER PRIMARY KEY, body TEXT, mac TEXT);
        CREATE TABLE IF NOT EXISTS sessions(digest TEXT PRIMARY KEY, actor TEXT, expires INTEGER);
        CREATE TABLE IF NOT EXISTS outbox(id INTEGER PRIMARY KEY, case_id TEXT,
            recipient TEXT, status TEXT, attempts INTEGER DEFAULT 0,
            UNIQUE(case_id, recipient));
        ''')
        self.model = Demo()
        row = self.db.execute("SELECT body,mac FROM state WHERE id=1").fetchone()
        if row:
            if not hmac.compare_digest(self.sign(row[0]), row[1]):
                self.db.close()
                raise ValueError("State integrity failure")
            state = json.loads(row[0])
            self.model.__dict__.update(state)
            self.model.grants = [Grant(**g) for g in state["grants"]]

    def sign(self, body):
        return hmac.new(self.key, body.encode(), hashlib.sha256).hexdigest()

    def _save(self):
        state = dict(self.model.__dict__)
        state["grants"] = [dict(g.__dict__) for g in self.model.grants]
        body = json.dumps(state, sort_keys=True, separators=(",", ":"))
        self.db.execute("INSERT OR REPLACE INTO state VALUES(1,?,?)", (body, self.sign(body)))

    def provision(self, actor, expires):
        """Trusted local operator provisions a demo credential, never an API endpoint."""
        if not actor or type(expires) is not int or expires <= 0:
            raise ValueError("Actor and positive expiry required")
        token = secrets.token_urlsafe(32)
        with self.db:
            self.db.execute("INSERT INTO sessions VALUES(?,?,?)",
                            (hashlib.sha256(token.encode()).hexdigest(), actor, expires))
        return token

    def authenticate(self, token, now):
        if not isinstance(token, str) or type(now) is not int or now < 0:
            raise PermissionError("Invalid credential or time")
        row = self.db.execute("SELECT actor,expires FROM sessions WHERE digest=?",
                              (hashlib.sha256(token.encode()).hexdigest(),)).fetchone()
        if not row or now >= row[1]:
            raise PermissionError("Invalid or expired session")
        return row[0]

    def revoke_session(self, token):
        with self.db:
            self.db.execute("DELETE FROM sessions WHERE digest=?",
                            (hashlib.sha256(token.encode()).hexdigest(),))

    def configure_fixture(self, grants, away=False, handoff=None):
        """Trusted local operator setup, not customer-facing mutation."""
        self.model.grants = grants
        self.model.away = away
        if handoff:
            self.model.accept_handoff(self.model.backup, *handoff)
        with self.db:
            self._save()

    def request(self, token, operation, now, **args):
        actor = self.authenticate(token, now)
        # Never accept a caller-supplied actor/subject as an authenticated identity.
        if "actor" in args or "subject" in args:
            raise PermissionError("Identity comes from session")
        if operation == "view":
            return self.model.view(args["case_id"], actor, now)
        if operation == "export":
            return self.model.export_case(args["case_id"], actor, now)
        before = json.dumps(self.model.__dict__, default=lambda g: g.__dict__)
        try:
            with self.db:
                if operation == "attempt":
                    result = self.model.attempt(actor, args["action"], args["resource"], now)
                    if not result["allowed"]:
                        cid = result["case_id"]
                        self.db.execute("INSERT OR IGNORE INTO outbox(case_id,recipient,status) VALUES(?,?,?)",
                                        (cid, self.model.cases[cid]["owner"], "pending"))
                elif operation == "acknowledge":
                    result = self.model.acknowledge(args["case_id"], actor, now)
                    self.db.execute("UPDATE outbox SET status='acknowledged' WHERE case_id=? AND recipient=?",
                                    (args["case_id"], actor))
                elif operation == "grant_advocate":
                    if args["expires"] <= now:
                        raise ValueError("Future access expiry required")
                    result = self.model.grant_advocate(args["case_id"], actor, args["advocate"], args["expires"])
                    self.db.execute("INSERT OR IGNORE INTO outbox(case_id,recipient,status) VALUES(?,?,?)",
                                    (args["case_id"], args["advocate"], "pending"))
                elif operation == "revoke_advocate":
                    cid = args["case_id"]
                    old = self.model.cases[cid]["advocate"]
                    result = self.model.revoke_advocate(cid, actor)
                    self.db.execute("UPDATE outbox SET status='canceled' WHERE case_id=? AND recipient=?",
                                    (cid, old))
                else:
                    raise PermissionError("Unsupported operation")
                self._save()
            return result
        except Exception:
            state = json.loads(before)
            self.model.__dict__.update(state)
            self.model.grants = [Grant(**g) for g in state["grants"]]
            raise

    def deliver_test_queue(self, adapter, now):
        """Trusted test worker. Adapter receives only an opaque case ID and recipient.

        External adapter must deduplicate by delivery_id. Exactly-once delivery is
        not promised: a crash after external acceptance may cause retry.
        """
        rows = self.db.execute("SELECT id,case_id,recipient FROM outbox WHERE status IN ('pending','failed') ORDER BY id").fetchall()
        for delivery_id, cid, recipient in rows:
            c = self.model.cases[cid]
            permitted = recipient == c["owner"] or (recipient == c["advocate"] and now < c.get("advocate_expires", 0))
            status = "canceled"
            if permitted:
                try:
                    status = "delivered" if adapter(delivery_id, cid, recipient) else "failed"
                except Exception:
                    status = "failed"
            with self.db:
                self.db.execute("UPDATE outbox SET status=?,attempts=attempts+1 WHERE id=?",
                                (status, delivery_id))
        return self.db.execute("SELECT id,status,attempts FROM outbox ORDER BY id").fetchall()

    def close(self):
        self.db.close()
