# Maya Node competitive landscape — 2026-11-07
Research from public product pages. Absence of published detail does not prove a competitor lacks a capability. Maya is a synthetic prototype, not a deployed competitor.

| Organization | Publicly documented capabilities | Maya differentiation hypothesis to validate |
|---|---|---|
| Feeding America MealConnect | Donor posting, agency matching, local food-bank coordination, refrigerated/frozen loads, availability-based pickup, reporting/export | Cross-platform operator for organizations using multiple existing systems; receipt-level reconciliation and explicit approval evidence |
| Food Rescue Hero / 412 Food Rescue | Volunteer dispatch, donor and agency logistics, onboarding, BI, multi-city partner network | Exception-handling and integration layer; avoid competing head-on with its volunteer network |
| Food Rescue US | Volunteer claiming, recurring pickups, cancellations, agency matching, local site operations | Automated exception escalation with documented authority and provenance |
| Goodr | Managed pickups, live tracking, donation impact and tax documentation | Pantry-to-pantry capacity and cold-storage coordination across independent operators |
| Spoiler Alert | AI-assisted surplus inventory listing, pricing, freight, and secondary-market buyers | Nonprofit resource coordination rather than commercial closeout sales |
| Share My Meals STAN | Cold-chain safety, tracking, allocation, navigation, donor/recipient communication, impact reporting | Test whether cross-platform integration and evidence-grade discrepancy resolution are unmet needs; do not claim STAN lacks safety controls |

## Evidence URLs
- https://mealconnect.org/how-it-works
- https://mealconnect.org/receive
- https://foodrescuehero.org/our-product/
- https://412foodrescue.org/programs/
- https://foodrescue.us/our-app/
- https://goodr.co/food-waste-solutions/surplus-food-recovery/
- https://www.spoileralert.com/
- https://sharemymeals.org/technology/

## Product bets, not established advantages
1. **System-of-systems operator**: permissioned integrations with existing donor, pantry, logistics and inventory platforms rather than forcing replacement.
2. **Verifiable operations**: time-stamped evidence, human approvals, no silent override, reconciliation and dispute correction.
3. **Cold-chain capacity orchestration**: capacity freshness and truck/receiving windows across pantries, with durable atomic reservations.
4. **Exception-first workflow**: missing driver, spoiled lot, 20-box discrepancy, unacknowledged request, backup contact.
5. **Accessible affordability**: clear organization-paid coordination fee, no recipient charge; test willingness-to-pay with consented partners.

## Critical corrections
MealConnect already supports availability-based matching and reporting; Food Rescue Hero already offers end-to-end volunteer dispatch and analytics; Share My Meals already documents cold-chain controls. These are **not** novel Maya features. We must win on interoperability, evidence quality, and measurable reduction in coordinator workload, and verify that those gaps exist through partner interviews and demos.

## Competitive validation plan
For each competitor, request demos and review published pricing, integrations/API, offline workflow, SLA, exception handling, data export, proof of delivery, and privacy. Use a common scripted fictional rescue (donor offer, freezer full, truck conflict, 200 loaded/180 received, cancellation). Score only observed evidence and record unknowns. No scraping private accounts or accessing customer records.

## Maya's verified stage
Draft PR #109 synthetic GitHub workflow reported success on 2026-11-07. This does not establish customer readiness, performance under actual load, durable reservation behavior, or superiority over these established products. No real data, messages, dispatch, or billing.
