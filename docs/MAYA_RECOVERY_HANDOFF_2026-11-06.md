# MAYA recovery inventory and handoff — 2026-11-06

Status: RECOVERY IN PROGRESS. This file is evidence inventory, not proof of production readiness.

## Founder-confirmed visual baseline
The founder supplied screenshots of a working Academy on Android: pale sky-blue background, sunflower heading, navy typography and outlines, yellow rounded buttons, cream cards, illustrated pantry worker and delivery truck, fictional food-transfer exercise, five-question knowledge check. The Academy page explicitly says it does not transmit quiz answers or save completion/certification. Preserve this styling and content. A separate illustrated pantry-worker graphic was supplied for survey use. No graphics redesign without request.

## Verified connected resource locations
- Vercel Academy project: `maya-academy-synthetic-preview` / `prj_TB7zX2L71CAdUYBXsCd5uefwN93G`; latest deployment `dpl_98pUpwcPZt9bxv3ijEBfp3kCaifF`; READY; original source tree contains `src/index.html`. Founder screenshot confirms page loaded on tablet. SSO enabled for non-custom domains.
- GitHub development: `mommommy1960-lang/maya-node` PR #106, branch `proposal/operational-competence-survey-2026-11-06`, OPEN DRAFT, UNMERGED. Contains guarded synthetic AAO service, Academy backend, synthetic survey intake (public survey disabled), and reconciliation engine and tests. Do not merge until reviewed.
- Vercel `civic-continuum-checkup-preview` / `prj_mhjXfeBVeQAxsTKSOBZWip0FG46h`: GitHub-connected preview, multiple READY deployments including latest `dpl_HSG9BVZYsQ341X49mviqhQQDh6Lm` at commit `bec75567c38bca84858aa3811c32af6601d6c4a0`. Do not assume it is the correct frontend.
- Separate experimental reconciliation Vercel projects: `maya-reconciliation-synthetic-lab`, `maya-reconciliation-api-staging`, `maya-reconciliation-fullstack-staging`. They are NOT the original Academy or verified customer app; avoid using them as canonical.
- Business card QR image supplied by founder; prior assistant decoded destination as `https://civic-continuum.myqueen1960.chatgpt.site/contact.html`, but this destination has NOT been independently validated. GitHub main docs/JUAN_ANTONIO_GARCIA_BUSINESS_REVIEW.md references older `https://civic-continuum-contact.freshcoin8.chatgpt.site` contact/demo/survey materials. Do not silently treat these as the same deployment.
- Civic Continuum main domain `civiccontinuum.org` must remain unchanged without approval.

## Next recovery checks
1. Identify exact currently working Maya operations UI, Academy, and survey URLs separately, verify HTTP/browser behavior and screenshot parity, inspect deployment source and routes. READY is not HTTP proof.
2. Back up complete Academy HTML and graphics, survey source, and Maya UI to GitHub on proposal branch with verified commit; do not overwrite originals.
3. Map QR destination to its real contact/survey route; verify that scan opens the intended page and consent/privacy gate.
4. Repair one isolated staging site using original illustrated visual design, with guarded synthetic backend. Test GET homepage, Academy, survey, health, reconciliation, and rejection of real data; preserve receipts, auth, and audit controls.
5. Customer production remains NO-GO until identity/tenant isolation, hosted deletion and receipt persistence, backup restore, incident escalation, written pilot permission, external feedback, and Stripe mode are independently verified. No real customer data or live payments.

## Bruce-to-Bruce
Do not start another new-look website. Recover and test original artifacts first. Founder has confirmed the Academy screenshot works. Record verified URL and test evidence, not only Vercel READY. Keep synthetic-only boundaries.
