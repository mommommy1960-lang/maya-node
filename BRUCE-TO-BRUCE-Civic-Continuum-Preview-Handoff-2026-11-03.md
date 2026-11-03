# BRUCE-TO-BRUCE — Civic Continuum Website Preview Handoff
Date: 2026-11-03 (America/Los_Angeles)
Status: PAUSED at founder's request; preserve current state, do not continue testing or deploy until asked.

## Source of truth and scope
- Existing public website: https://civiccontinuum.org — DO NOT change without founder approval.
- GitHub repository: mommommy1960-lang/maya-node
- Development branch: focus/ai-privacy-accuracy-checkup
- Draft PR #101: https://github.com/mommommy1960-lang/maya-node/pull/101 (open, unmerged)
- Separate Vercel project: civic-continuum-checkup-preview (prj_mhjXfeBVeQAxsTKSOBZWip0FG46h)
- Original successful preview deployment: dpl_2tbn2bGrSQXfSCDHmLAm7rBft4XK, commit b0735122ee6550653f39bb6f9aeb256f880c6f28
- SPA routing fix: frontend/vercel.json, commit 85721bd2de22707d42fa8624e3dabd53df55e934
- Corrected deployment: dpl_586nvRvzX8fW39nDByEJtfWdTuDo; URL https://civic-continuum-checkup-preview-ohnooj96h-civic-continuum.vercel.app ; Vercel verified READY for commit 85721bd.
- The corrected deployment is a PREVIEW deployment, not the original business domain. Earlier deployment was target production within the isolated preview project only.

## Confirmed evidence
- Founder personally opened preview on Android tablet and confirmed homepage visible.
- Founder tested Home, AI Checkup, Mission & Research, Contact navigation and reported all work.
- GitHub source review: homepage states prototype only; contact page has mailto:contact@civiccontinuum.org; Services, Pricing, Consultation describe prototype and no paid offering; About distinguishes Maya Node/SAGE/Aurora/Flux R&D.
- Founder confirmed receiving email at contact@civiccontinuum.org (apparently forwarded/linked to another inbox; exact forwarding destination not verified).
- GitHub PR #101 open, draft, unmerged when checked.
- Vercel get_deployment confirmed corrected build READY.
- Vercel project has SSO protection enabled. No public access assurance.

## NOT verified / remaining work
- Independent live-browser deep-link and refresh testing of /contact, /about, /services, /pricing, /consultation; deployment READY alone does not prove those paths load.
- Full accessibility/mobile QA, broken links, browser console, email delivery test independent of founder's report.
- Founder proposed delegating browser QA to Gemini. A detailed handoff was drafted in chat but NOT sent to Gemini. No Gemini report received.
- Vercel list_project_routes returned [] even after config commit; this API does not establish whether deployed vercel.json rewrites work. Attempt to read deployment source file through Vercel returned 404. Do not mark refresh as PASS or FAIL without browser evidence.

## Explicit safety boundaries
- Do not change civiccontinuum.org, merge PR #101, publish primary site, enable billing/payments, spend money, or accept real/confidential customer data without explicit founder approval.
- Maya Node is NOT cleared for real customer data or live billing.
- Checkup $250 was a research hypothesis, not an established price or live offer.
- Keep existing preview intact. Avoid redundant deploys.

## Founder instruction at pause
Founder said the spoken discussion was not appearing on screen and requested: STOP; save all current work in GitHub and in a Bruce-to-Bruce handoff so another model can resume without losing context.
This file is the durable handoff. Next assistant should resume from this state only when requested, not assume Gemini has been contacted.

## November 4 adviser Zoom preparation — founder-requested addition (2026-11-03)
Founder requests that whenever she says **“I need to be prepared for the Zoom call”**, the briefing must include the following commercial update for Juan's Wednesday November 4, 2026, 10:30–11:30 a.m. Pacific meeting (verify meeting details before relying on them):
- Founder approved **$150 per client for the first three founding clients** for a human-led Civic Continuum AI Privacy & Accuracy Checkup.
- Scope: review up to three public or fictional AI examples; concise findings and 30-day action checklist; 20-minute findings discussion. No confidential data or production Maya Node.
- This is a proposed first-revenue path, **not** a booked sale; no customers or payments confirmed.
- Ask Juan for feedback on positioning, customer fit, licensing and business terms, and whether warm introductions may be appropriate **during the Zoom conversation**, not in a new email now.
- Juan was recently sent a substantial adviser packet. **Do not send another sales email to Juan** before the call; do not resend the packet automatically.
- Source of offer and terms: BRUCE-TO-BRUCE-Founding-Client-Price-Approval-2026-11-03.md and BRUCE-TO-BRUCE-Founding-Client-Sales-Kit-2026-11-03.md.
- This is an internal preparation addendum; it does not revise or resend an already delivered email packet.
