"""Run: python3 -m examples.real_file_gate --output NEW_DIRECTORY"""
import argparse
import hashlib
import json
from pathlib import Path
from src.adapters.file_write_gate import FileWriteGate, verify_receipts


def main():
    parser = argparse.ArgumentParser(description='Maya real file-action verification')
    parser.add_argument('--output', required=True, help='New directory; existing directories are refused')
    args = parser.parse_args()
    gate = FileWriteGate(args.output)
    content = 'Civic Continuum: Maya created this real file after checking exact permission.\n'
    try:
        approved = gate.authorize('local-owner', 'authorized.txt', content)
        created = gate.execute(approved, 'local-owner', 'authorized.txt', content)
        gate.revoke(approved)
        repeat = gate.execute(approved, 'local-owner', 'authorized.txt', content)
        withdrawn = gate.authorize('local-owner', 'must-not-exist.txt', 'This write must be blocked.\n')
        gate.revoke(withdrawn)
        blocked = gate.execute(withdrawn, 'local-owner', 'must-not-exist.txt', 'This write must be blocked.\n')
        path = gate.output / 'authorized.txt'
        assert created['outcome'] == 'created'
        assert path.read_text() == content
        assert hashlib.sha256(path.read_bytes()).hexdigest() == created['content_sha256']
        assert repeat['outcome'] == blocked['outcome'] == 'blocked'
        assert not (gate.output / 'must-not-exist.txt').exists()
        assert verify_receipts(gate.root / 'receipts.jsonl')
        result = {'authorized_file': str(path), 'actual_file_sha256': created['content_sha256'],
                  'created': created, 'revoked_retry': repeat, 'revoked_new_write': blocked,
                  'blocked_file_exists': False, 'receipt_chain_consistent': True,
                  'scope': 'Real local filesystem adapter; single-process, not a hosted service or OS sandbox.'}
        (gate.root / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result, indent=2))
    finally:
        gate.close()


if __name__ == '__main__':
    main()
