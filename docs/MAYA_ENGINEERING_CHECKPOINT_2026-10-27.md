# Maya engineering checkpoint — October 27, 2026 (Pacific)

## Scope and evidence
Continue the existing Maya Accountable Actions Sites project. No replacement site, payment, email delivery, AI inference, DNS change or security certification is included.

The prior release (v15) added dispatch-owned sign-out/switch-account links and showed the signed-in email. In this conversation the founder used two consenting accounts: account B began empty, prepared a synthetic file, authorized/created it, downloaded/opened the exact bytes, and account A's subsequent listing did not include that file. This is a founder-operated two-account test, not third-party customer validation. A third account is not needed for the basic separation check.

## Implemented in this checkpoint
- Additive schema migration: nullable receipt metadata, nullable retention deadlines, minimal account-scoped service notices. Existing records, output bytes and receipts are preserved; existing deadlines remain NULL.
- Persist action type, source (website or connected ChatGPT tool), correlation ID and authorization-event reference for new action receipts. Server export adds output reference, byte count and SHA-256.
- Server-generated v2 JSON export uses a D1 transaction snapshot, not the browser's latest-200 cache. All currently retained action events and service notices are exported up to 5,000 each. Larger histories produce an explicit error, never a silently partial file. Payload text and email addresses are omitted. Legacy receipt metadata is marked partial rather than fabricated.
- Record minimal access-denial/human-review notices. Foreign/missing target IDs and payloads are not copied into denial notices. A review reference is not a sent email, staffed ticket or promise of a response.
- Storage uncertainty returns a correlation reference and attempts to persist a handoff notice after rollback. Total database outage explicitly reports when no notice could be saved; no success is claimed.
- New records expire after 30 days. Active request/output/linked receipt cleanup is atomic and account-scoped, on the next authenticated access. Legacy records remain until owner deletion. Standalone minimal service notices expire after 30 days on account access.

## Verification completed before publication
- 77 automated tests passed: existing cases plus targeted deletion, access, export, outage, retention and migration-preservation cases.
- 1 isolated local workerd/D1 integration test passed, covering actual D1 migration and snapshot export, foreign download/delete denial, injected deletion rollback, successful deletion/re-query, preservation of another owner's record and expiry.
- TypeScript check passed.
- Production build passed; Sites version 16 deployed successfully to https://maya-working-workflow-lab.myqueen1960.chatgpt.site. Source commit: `685c5c5b429ec15a2fb01e8def34d28b4435adba`. Deployment: `appgdep_6ae165f223508191a916ef8915a5f638`.
- Forced failures used isolated databases only. No production failure injection or deletion of the founder's saved records.

## Matrix disposition
| Cases | Evidence | Remaining limit |
| --- | --- | --- |
| DEL-01/02/06/08 | Earlier hosted draft/completed deletion and founder reload/list evidence; fresh isolated SQL and local D1 deletion/preservation checks | No claim that a normal owner-scoped listing proves physical backup erasure |
| DEL-03 | Fresh isolated SQL and local D1 foreign download/delete denial with safe notice; real two-account listing separation | Direct destructive probing of a real production target is not performed |
| DEL-04/05 | Repeat-delete denial and forced-failure atomic rollback pass in isolation | Fault injection is deliberately not performed against production |
| DEL-07 | New-record expiry/access cleanup implemented and tested; legacy behavior disclosed | Hosting backup/log expiry, unattended purge and restoration drill remain unverified |
| REC-01..05 | Persisted metadata, permission/grant linkage, exact bytes/hash, revocation/expiry/missing/replay denials tested | Historical receipts remain explicitly partial |
| REC-06/07 | Output/receipt failures roll back, handoff notice saved when possible; complete outage reports missing receipt | No untested claim of successful recovery during a production outage |
| REC-08 | Durable human-review reference with no execution or automatic message | Human notification/contact monitoring remains operational work |
| REC-09 | SQL/local D1 isolation and founder-operated two-account listings | Live direct download evidence recorded separately |
| REC-10 | Snapshot export vs stored events/output checked; >200 events and explicit overflow tested | Live export verification recorded separately |

## Existing prerequisites not satisfied by this code
- Hosting backup and infrastructure-log retention/expiry are not exposed by the available Sites tools. Obtain actual operator settings and verify them; do not infer purge guarantees.
- No unattended scheduled purge is installed. An account that never returns can retain expired physical rows; the service denies access and cleans them on its next authenticated request. This does not satisfy an unconditional physical-purge deadline.
- No backup restoration drill against hosted data has been performed. Use a separate staging database, synthetic records and explicit operator access for that drill.
- contact@civiccontinuum.org is displayed, but mailbox monitoring/delivery and acknowledgement coverage are not verified by these tests. No test email is sent.
- Founder remains primary owner; backup person/contact is unassigned. Record support hours and acknowledgement expectations before a business pilot.
- Written scope/permission is needed when a participating business starts a pilot. Do not invent a participant or demand a third account to finish the two-account engineering check.

## Incident and recovery procedure prepared for operator use
1. Pause affected creation; preserve minimal correlation references and avoid copying payloads into tickets or logs.
2. Check stored state and receipts before retrying an uncertain operation. A handoff is not proof that the action failed or completed.
3. Primary owner contacts the affected participant through the agreed channel. Backup contact, monitoring and support window must be filled before launch.
4. Test recovery using an isolated copy and synthetic fixture; reconcile request, output, permission and receipt together. Do not restore a deleted/expired record to live access without reviewing its retention deadline and authority.
5. Record containment, correction, data impact, recovery evidence and the owner's decision before reopening the workflow.

## Post-deployment verification
- The connected owner account still lists the same 10 requests and 28 action events; all 10 original retention deadlines remain NULL.
- All five original completed outputs read back successfully with their hashes matching the pre-release request listing.
- Using account A's real connected identity to request account B's synthetic output returned File not found and a correlation reference, without output contents. A minimal account-A denial notice was saved. No cross-account deletion was attempted on a real saved file.
- Signed into the existing owner account in the browser and verified the production workspace: existing records, real auth links, new receipt download and service-notice section are present.
- Clicked the production Download receipts link and parsed the actual downloaded JSON privately: v2 format, 10 requests, 28 action events, 1 service notice. All five created events have grant and output references. Payload bodies are omitted; the foreign target ID is absent. All 28 old action receipts remain labelled legacy_partial.
- No production fixture was created/authorized/deleted in this checkpoint. No fault injection occurred in production. Existing action history and original output contents remain preserved; only the expected minimal denial notice was added.

## Next assistant: continue without repeating the founder's account-switch exercise
The source/editor access blocker and the v15 sign-out task are resolved. Source is in the existing Sites-managed repository, not the public repository's bootstrap UI. The DEL/REC test cases above now have fresh isolated SQL/local D1 evidence. Do not describe them as unexecuted or make the founder redo them.
The remaining technical dependencies are actual hosting backup/log settings, an authorized isolated hosted restore drill, and an unattended purge mechanism if an unconditional physical-deletion deadline is required. Available Sites tools expose source, deployments and Worker logs, but no backup/restore configuration. Incident mailbox delivery/monitoring, backup person and business-pilot permission remain separate operational prerequisites. Never invent them or claim all paid-service readiness is complete.
