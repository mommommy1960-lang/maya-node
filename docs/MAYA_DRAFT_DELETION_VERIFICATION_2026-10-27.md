# Maya deletion verification — 2026-10-27

## Test target
Synthetic draft request `maya-gate-check-20261027.txt`, id `d3faef81-382d-4711-8f46-276a7abfcfe2`. No created output existed. User confirmed browser deletion via "Delete record and file" and subsequent refresh.

## Independent connected-service read
After user confirmed deletion and page refresh, `maya_list_requests` returned signedIn=true, 10 requests (previously 11), 28 events (previously 29), zero events referencing deleted id, zero orphan events. Remaining: 5 completed, 2 revoked, 3 draft. Five completed filenames: peer-sample-a.txt, civic-continuum-juan-brief.txt, my-note.txt, maya-chatgpt-live-proof.txt, maya-live-proof.txt.

## Verdict
PASS for deletion of this synthetic draft from current owner-scoped request and event list; PASS for immediate persistence after browser refresh and repeat connector read; PASS for preservation of the other 10 request entries and 5 completed entries. NOT TESTED: deletion of an existing completed output; actual storage-object erasure; backups, retention, cross-account isolation, atomic failure paths, independent receipt immutability. Do not label full deletion or security certification complete.

## Next work
Continue receipt integrity checks and independently test deletion of a *new disposable completed* output with consent; avoid founder's real completed records. Need access to hosted backend/backup policy for permanence proof. Founder reports limited cash and asks about an estimated $200 licensing budget; no exact fees verified. Do not promise that amount or recommend paying before requirements confirmed.
