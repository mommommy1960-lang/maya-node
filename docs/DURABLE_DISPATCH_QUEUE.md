
## Host worker package (not activated)

`src.sovereign.mail_worker` uses authenticated SMTP over verified TLS and processes only previously approved queue jobs. SMTP acceptance is not proof of inbox delivery. Authentication or ambiguous send failures stay blocked by the queue. No credentials are committed.

Install the repository at `/opt/maya-node` on a persistent Linux systemd host. Create a dedicated `maya-mail` service account and root-owned `/etc/maya-mail/config` containing `MAYA_SMTP_HOST`, `MAYA_SMTP_USER`, and optionally `MAYA_SMTP_PORT` (465 by default). Store the provider-issued SMTP credential in root-owned mode-0600 `/etc/maya-mail/smtp_password`. systemd supplies it through LoadCredential. Do not use or copy a ChatGPT Gmail connector token; connector authorization does not supply daemon credentials.

Install both units from `deploy/systemd/` into `/etc/systemd/system/`, run `systemctl daemon-reload`, then `systemctl enable --now maya-mail.timer`. The persistent database is `/var/lib/maya-mail/queue.db`. The trusted controller must use that same database and explicitly approve each immutable payload with recipient, subject, and body. Restrict controller and database access to trusted operators.

Check `systemctl status maya-mail.timer maya-mail.service` and `journalctl -u maya-mail.service`. Structured alerts go to the journal and make the worker exit unsuccessfully; external alert delivery and monitoring still need configuration. A five-minute worker limit may conservatively leave interrupted jobs dispatch_committed; reconcile them without blind retries. Before rollout, verify a canceled job never sends, an approved test arrives, and receipts survive host restart. Host installation, real credentials, external monitoring and end-to-end daemon delivery have not been verified in this workspace.

Validation: 13 queue tests and 3 adapter tests passed. Adapter tests mock SMTP; they verify authentication precedes sending and failed authentication never calls send.
