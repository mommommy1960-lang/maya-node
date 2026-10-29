# Bruce-to-Bruce continuation — October 29, 2026 (Pacific)

## Founder priority
Get Maya Node moving toward a real, narrow business pilot. Avoid another redesign or repeating already-passed tests. Separate the public demo, protected Cloudflare Worker, payment work, and operational readiness; they are not the same deployment.

## What is verified in repository records
- Existing Maya Node Site v18 was documented as deployed successfully on October 28, source `e6831dd5012fe6ce0e0ec8c81677631cc174e033`, deployment `appgdep_6ae25787a8f081919864b7eae59f3c15`.
- 87 automated tests, local workerd/D1 integration, targeted synthetic acceptance tests, TypeScript and production build were reported passing. These are not a fresh hosted end-to-end customer test.
- Scheduled cleanup was verified with persisted run ID `5c4451cc-e7c4-44ee-a9d5-3af85b03e6f8`; it removed 0/0/0/0 records and had zero pending expired requests.
- The customer-facing demo remains synthetic-only. No real customer records, payment activation, or consequential customer launch.
- Public GitHub readiness issue #76 was updated on October 29 with the deployment blocker and safe next step.

## Current blocker: Cloudflare build
Cloudflare Preview builds for commits `c7ab778` and `772be90` failed on October 29. Authenticated Cloudflare build logs could not be fetched from the available session (`login_required`), so the exact cause is not yet confirmed. The repository contains `deploy/cloudflare/wrangler.jsonc`.

Likely setting to verify in the existing **Worker** build configuration: root directory `deploy/cloudflare` relative to the repository root, without a leading slash. If the build is configured to run from repository root instead, use the Wrangler config path `deploy/cloudflare/wrangler.jsonc`; inspect the current build command before selecting. Do not change the separate frontend Pages settings to fix the Worker. Keep controller-token authentication and `SEND_ENABLED=false`. Do not make a production deployment, secret, DNS, D1, or checkout change without verified settings and authorization.

Separate frontend Pages configuration documented in `docs/FRONTEND_RECOVERY_AND_DEPLOYMENT.md`: production branch `main`, root directory `frontend`, build command `npm run build`, output directory `dist` (relative to frontend). Do not conflate that frontend with the protected Worker.

## External/operational gates still open
1. Obtain authenticated access to Cloudflare settings and exact failed-build logs; correct the configuration only after confirming which build target is being configured.
2. Re-run preview build and inspect the result; do not call it fixed until a successful build/deployment is observed.
3. Re-check the customer-facing demo signed out and at mobile width after the relevant deployment.
4. Hosted real-session and deletion verification; hosting backup/log retention and isolated recovery (Support case 17489131); actual tablet alert delivery; safe founder coverage/escalation plan.
5. Written permission and an agreed scope for one supervised synthetic-data-only business pilot, then record actual participant feedback.
6. Keep business registration/licensing, payment authorization and end-to-end billing rehearsal separate; no real payment activation until those are verified.

## Outreach state
- Juan Garcia was emailed a progress update/invitation on October 29; do not duplicate it. No confirmed meeting is recorded.
- Austin Irvan pilot invitation remains drafted, not sent. User authorized drafting/invitation but no verified LinkedIn send channel was available in the latest checks. Do not claim it was sent.
- OpenAI Support case 17489131 has no substantive recovery/configuration answer in the latest review. Do not duplicate the support request.
- Gmail connector is administrator-disabled in the current session; user expects Gmail correspondence, not Outlook. Do not claim any email sent without verified send result.
- Do not contact Dr. Thomas until the existing hold is reviewed.

## Immediate next actions
- Secure working authenticated Cloudflare dashboard access without requesting or sharing credentials in chat.
- Inspect Worker build command/root setting and exact failed logs; make only the smallest verified config correction.
- Continue synthetic-only customer discovery in parallel; keep the demo accurately labelled and do not promise live automation, savings, compliance, or launch readiness.
- Update this log and issue #76 with evidence, not assumptions.

## Safety and change boundary
No production setting, deployment, secret, DNS, D1 data, payment configuration, or checkout was changed as part of this October 29 continuation. The Cloudflare root-directory explanation remains a hypothesis until the authenticated build logs/settings confirm it.
