# SPDX-License-Identifier: CERL-1.0
"""Single-process consent gate for real, create-only UTF-8 files.

Only writes through this adapter are governed. It is not an OS sandbox.
Tokens are process-local; receipts are persisted and fsynced before execution.
"""
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import re
import threading
from src.sovereign.consent_tokens import ConsentScope, ConsentTokenManager
from src.services.ledger.ledger import ImmutableLedger


class FileWriteGate:
    MAX_BYTES = 65536

    def __init__(self, directory):
        self.root = Path(directory).absolute()
        # Refuse existing directories so old files and symlinks cannot be adopted.
        self.root.mkdir(mode=0o700)
        self.output = self.root / 'files'
        self.output.mkdir(mode=0o700)
        self._dir = os.open(self.output, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        self._audit = os.open(self.root / 'receipts.jsonl', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        self._lock = threading.RLock()
        self.tokens = ConsentTokenManager()
        self.ledger = ImmutableLedger()
        self._broken = False
        self._persist(self.ledger.entries[0])

    def close(self):
        with self._lock:
            if self._dir is not None:
                os.close(self._dir)
                os.close(self._audit)
                self._dir = None

    def _persist(self, entry):
        data = (json.dumps(asdict(entry), sort_keys=True) + '\n').encode('utf-8')
        try:
            while data:
                count = os.write(self._audit, data)
                if count <= 0:
                    raise OSError('Incomplete audit write')
                data = data[count:]
            os.fsync(self._audit)
        except OSError:
            self._broken = True
            raise

    def _record(self, operation, data):
        if self._broken or self._dir is None or not self.ledger.verify_integrity():
            raise RuntimeError('Gate unavailable: audit state is invalid or closed')
        entry = self.ledger.append(operation, data)
        self._persist(entry)
        return dict(data, receipt_index=entry.index, receipt_hash=entry.entry_hash)

    def _request(self, actor, filename, text):
        if not isinstance(actor, str) or not actor.strip() or len(actor) > 200:
            raise ValueError('A nonempty actor label of at most 200 characters is required')
        if not isinstance(filename, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,119}', filename):
            raise ValueError('Use a plain filename, not a path')
        if not isinstance(text, str):
            raise ValueError('Content must be text')
        if len(text) > self.MAX_BYTES:
            raise ValueError('Content exceeds 64 KiB')
        content = text.encode('utf-8')
        if len(content) > self.MAX_BYTES:
            raise ValueError('Content exceeds 64 KiB')
        request = {'actor': actor, 'filename': filename,
                   'content_sha256': hashlib.sha256(content).hexdigest(), 'bytes': len(content)}
        canonical = json.dumps(request, sort_keys=True, separators=(',', ':')).encode()
        return request, content, 'file.create:' + hashlib.sha256(canonical).hexdigest()

    def authorize(self, actor, filename, text, ttl_seconds=300):
        with self._lock:
            request, _, operation = self._request(actor, filename, text)
            token = self.tokens.generate_token(actor, operation, ConsentScope.SINGLE_OPERATION, ttl_seconds)
            self._record('permission.granted', dict(request, token_id=token.token_id, expires_at=token.expires_at))
            return token.token_id

    def revoke(self, token_id):
        with self._lock:
            if self._broken:
                raise RuntimeError('Gate unavailable')
            revoked = self.tokens.revoke_token(token_id)
            return self._record('permission.revoked', {'token_id': token_id, 'revoked': revoked})

    def execute(self, token_id, actor, filename, text):
        with self._lock:
            request, content, operation = self._request(actor, filename, text)
            token = self.tokens.get_token(token_id)
            reason = None
            if token is None:
                reason = 'unknown_permission'
            elif not self.tokens.verify_token(token):
                reason = 'permission_' + token.status.value
            elif token.user_id != actor or token.operation != operation:
                reason = 'request_does_not_match_permission'
            if reason:
                return self._record('action.blocked', dict(request, token_id=token_id, outcome='blocked', reason=reason))
            # Pre-execution durable receipt is mandatory. Any failure stops the write.
            self._record('action.authorized', dict(request, token_id=token_id, outcome='authorized'))
            if not self.tokens.use_token(token_id):
                return self._record('action.blocked', dict(request, token_id=token_id, outcome='blocked', reason='permission_unavailable'))
            fd = None
            try:
                fd = os.open(filename, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=self._dir)
                data = content
                while data:
                    count = os.write(fd, data)
                    if count <= 0:
                        raise OSError('Incomplete file write')
                    data = data[count:]
                os.fsync(fd)
                os.close(fd)
                fd = None
                os.fsync(self._dir)
            except OSError as exc:
                if fd is not None:
                    os.close(fd)
                # A failed/partial file is never retried or overwritten automatically.
                return self._record('action.failed', dict(request, token_id=token_id, outcome='failed', reason='target_exists' if isinstance(exc, FileExistsError) else 'write_error', partial_file_possible=not isinstance(exc, FileExistsError)))
            # Failure here propagates: caller must treat the outcome as uncertain,
            # inspect the filesystem and never blindly retry.
            return self._record('action.completed', dict(request, token_id=token_id, outcome='created', reason='current_exact_permission'))


def verify_receipts(path):
    """Detect structural/hash inconsistency, not malicious whole-log replacement."""
    from src.services.ledger.ledger import LedgerEntry
    try:
        rows = [json.loads(line) for line in Path(path).read_text().splitlines()]
        if not rows:
            return False
        ledger = ImmutableLedger()
        ledger.entries = [LedgerEntry(**row) for row in rows]
        ledger._trusted_head_hash = ledger.entries[-1].entry_hash
        return ledger.verify_integrity()
    except (OSError, TypeError, KeyError, ValueError, AttributeError):
        return False
