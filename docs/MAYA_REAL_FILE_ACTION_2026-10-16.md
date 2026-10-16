# Maya: real file-action gate

This adapter uses the existing signed ConsentTokenManager and hash-chained ImmutableLedger to control a real filesystem action. It is executable code, not a fictional workflow or model-response stub. No API key, hosting account, payment or Python third-party package is needed. Python3.10+ and a POSIX filesystem are required.

From the repository root:

```bash
python3 -m examples.real_file_gate --output /tmp/maya-proof-new-directory
python3 -m unittest tests.integration.test_real_file_gate -q
```

Use a NEW output directory. The program refuses to adopt an existing directory. It creates:
- files/authorized.txt: actual bytes written after current exact permission.
- receipts.jsonl: durable, fsynced grant, decision, outcome and revocation records.
- verification.json: results checked against the actual file bytes and missing blocked file.
- files/must-not-exist.txt: must NOT be present; permission was revoked before execution.

Permission is signed and bound to actor label, exact filename, byte length and content hash. Tokens are single-use. Changed payloads, unknown/revoked/expired/used permissions, paths outside the allowed plain filename format, existing files and symlinks are rejected. A same-process lock serializes checks, consumption and writes. Durable authorization receipt is required before the side effect. Write failures consume permission and are not automatically retried. A final receipt failure propagates an uncertain outcome: inspect the file before any new action. Mid-write failures may leave a partial file and are reported as such.

## Honest boundary

This is a trusted local caller API and a real adapter, not an OS sandbox, an identity service, external AI integration or a hosted customer product. Actor labels are supplied by the trusted caller; there is no remote authentication. Code with equivalent operating-system access can bypass this adapter, modify its objects or rewrite the entire receipt log. Receipt validation checks structural consistency, not independent authenticity or resistance to whole-log replacement. Tokens and lock are process-local and are not restarted or shared across processes. Existing live Maya remains unresolved. Do not market this component as general protection of all AI actions.

Revocation takes effect before a not-yet-started request acquires the gate lock; it cannot undo a completed write. No email or external customer action is performed by this command.

## Verification

13 focused tests execute real files in temporary directories, including revocation, exact binding, expiry, replay, create-only behavior, symlink rejection, path/size checks, audit-failure blocking, same-process concurrency and modified receipt detection. The separate example creates and reads a real file and verifies that the revoked new write produces no file. Receipts are evidence from this local run, not customer adoption or paid service validation.
