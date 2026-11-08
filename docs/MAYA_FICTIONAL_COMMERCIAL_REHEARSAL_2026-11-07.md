# Maya Node fictional commercial rehearsal — November 7, 2026
Status: **DEVELOPER-LOCAL SYNTHETIC ONLY / NOT A STRIPE TEST / NO REAL MONEY**

## Scope and capabilities
The original synthetic order/receipt journey now has a separate persistent local SQLite **commercial simulator**, in `prototypes/pantry-watchtower/synthetic-commercial-rehearsal.mjs`, integrated with the loopback-only browser demo. The purpose is to test ordering and user-visible commercial state machine logic without any payment provider, partner data, or contractual effect.

1. Require all **three fictional order approvals** before preparing the quote.
2. Display a fictional **USD $2.50 sponsor service fee**, **$0.00 receiver fee**, and fixed versioned sample terms `SYN-TERMS-2026-11-07-v1`. These figures are **test fixtures**, not market pricing, tax advice or a commitment to charge.
3. Require fictional sponsor acceptance of the exact sample terms version before attempting mock authorization. Nobody logs in; button clicks do **not** evidence real sponsor consent.
4. Record unique mock authorization attempt IDs; simulate decline/retry; reject contradictory replays, wrong actors, backdated events and unauthorized transitions. Store append-only mock financial events.
5. Block **local demo pickup** until fictional sponsor authorization is recorded. Never mistake this HTTP demonstration guard for a production-grade independent payment/role gate.
6. Permit fake capture only after reconciled fictional delivery, then fake refund, with net simulated amount zero after refund. No real card is touched.
7. In the **same SQLite transaction as order cancellation/expiry**, auto-void any outstanding fake quote/agreement/authorization (before physical pickup) so there is no stale fictional authorization. Transaction persistence and replay tests include restart behavior.
8. Keep the server loopback-only, with restrictive origin/Host checks and no credentials, vendor imports, outbound network, external notifications, real data, dispatch or billing.

## Not done, and critical legal/technical boundaries
- **NO Stripe test-mode authorization, real Stripe API connection, webhook signature validation, provider dispute/refund tests, hosted idempotency, or PCI assessment.** The simulator says `LOCAL_SIMULATOR_ONLY_NOT_STRIPE` in its outputs.
- No authenticated or independently signed donor/receiver/driver/sponsor approval. No verified agreement acceptance by a real person.
- No hosted website integration, independent Android/screen-reader accessibility certification, data-protection/backup/delete evidence, payment/legal/food-safety review, incident owners or written partner permission.
- This demo cannot accept anyone's money; **real customer onboarding, external notifications, dispatch, real data and live billing are all NO-GO**. Do not deploy the simulator as a real checkout.

## Acceptance and planned next work
```
node --test prototypes/pantry-watchtower/*.test.mjs
# same-device loopback demo (Node 22+)
node prototypes/pantry-watchtower/synthetic-local-demo-server.mjs
```
- Test the real Chromium→loopback API→SQLite path in the dedicated GitHub browser workflow, including a local declined authorization and mock capture/refund. Record exact run IDs and TAP counts after independent verification.
- Next **separate** milestone: a permissioned, zero-live-charge Stripe **test-mode** connector with signed webhook event validation/replay controls and restricted secret handling. Sandbox configuration requires owner-controlled account access and approval, and must not be attempted with any live keys.
- Legal/partner/pilot governance remains a separate founder go/no-go: prospective real charge payer, service fee, tax treatment, refund terms and food-recipient no-charge principle need independent review.

## November 7 checkpoint

The [public Maya homepage](https://maya-working-workflow-lab.myqueen1960.chatgpt.site/) is the destination for the corrected Civic Continuum QR card. The demo, survey, and contact links were opened and verified from that homepage.

[Node CI](https://github.com/mommommy1960-lang/maya-node/actions/runs/42445674313/job/128623968229) reported 96 passes. It verified three fictional approval roles, blocked premature pickup, and confirmed that a pre-pickup cancellation releases resources and cannot be restarted or delivered. [Chromium-to-SQLite CI](https://github.com/mommommy1960-lang/maya-node/actions/runs/42445674294/job/128623968199) passed the full and partial receipt journeys.

The existing public v37 demonstration has a verified single-account fictional handoff and withdrawal. Next, use an isolated hosted environment to verify authenticated donor and receiver approvals, driver acknowledgment, and the cancellation drill. A delayed event from the original carrier should leave the order on hold, and a replacement plan should require fresh approvals. Track release gates in [issue #76](https://github.com/mommommy1960-lang/maya-node/issues/76) and [issue #80](https://github.com/mommommy1960-lang/maya-node/issues/80).
