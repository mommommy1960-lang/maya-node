# Maya Node: 50-step customer-readiness implementation backlog
Date: 2026-11-07
Status: authorized for synthetic-only development. No live customer data, real dispatch, external messages, or billing without separate evidence and founder approval.

Each item is a **proposed acceptance task**, not a completed milestone. Mark done only with commit, CI/test evidence, responsible reviewer and dated result.

## Reservation correctness
- [ ] 1. Run latest GitHub CI and inspect actual failing tests
- [ ] 2. Fix SQLite runtime compatibility and migration initialization
- [ ] 3. Enable SQLite foreign keys and WAL where appropriate
- [ ] 4. Make offer, freezer and truck reservation one atomic transaction
- [ ] 5. Add resource time windows and per-unit quantities
- [ ] 6. Implement deterministic idempotency keys for retries
- [ ] 7. Handle simultaneous reservation requests across processes
- [ ] 8. Make reservation expiry atomic and repeat-safe
- [ ] 9. Release holds on cancellation and timeout
- [ ] 10. Verify crash/restart recovery with file-backed database

## Order and evidence
- [ ] 11. Connect reservations to order lifecycle transitions
- [ ] 12. Persist order state and append-only audit events
- [ ] 13. Validate actor permissions for each transition
- [ ] 14. Require donor approval with evidence
- [ ] 15. Require receiving pantry approval with evidence
- [ ] 16. Require transporter confirmation with evidence
- [ ] 17. Block pickup until all approvals and capacity checks pass
- [ ] 18. Implement signed pickup manifest and quantity checks
- [ ] 19. Implement partial receipt and discrepancy review
- [ ] 20. Test duplicate, missing, contradictory and backdated evidence

## Safety and reliability
- [ ] 21. Define resource ownership and tenant isolation
- [ ] 22. Implement authentication and least-privilege authorization
- [ ] 23. Threat-model cross-tenant data exposure and abuse
- [ ] 24. Add input validation and bounded resource consumption
- [ ] 25. Add replay protection for all event/webhook handlers
- [ ] 26. Build structured logs with redaction and trace IDs
- [ ] 27. Define retention and deletion rules per data class
- [ ] 28. Prove hosted deletion including downstream copies
- [ ] 29. Prove backup restore and measure recovery objectives
- [ ] 30. Assign named human incident escalation and rollback owners

## Customer experience and finance
- [ ] 31. Browser-test demo module loading and interactions
- [ ] 32. Build accessible Android-first pantry dashboard
- [ ] 33. Label verified, stale, estimated and unavailable data
- [ ] 34. Add simple consented alert acknowledgment and escalation
- [ ] 35. Provide human-readable quote and service fee disclosure
- [ ] 36. Capture agreement acceptance with versioned terms
- [ ] 37. Rehearse Stripe sandbox authorization only
- [ ] 38. Verify signed sandbox webhooks and duplicate events
- [ ] 39. Rehearse cancellation, refunds and financial reconciliation
- [ ] 40. Test full synthetic customer journey including failures

## Partnership and launch
- [ ] 41. Map MealConnect and Food Rescue Hero integration permissions
- [ ] 42. Document adapters for import/export without unauthorized scraping
- [ ] 43. Review food-safety, privacy, insurance and WA licensing requirements
- [ ] 44. Obtain independent security and legal review
- [ ] 45. Prepare written pilot agreement and data-processing terms
- [ ] 46. Recruit one authorized donor, receiver and transport partner
- [ ] 47. Conduct usability interviews and log observed gaps
- [ ] 48. Measure coordination time, food delivered and exceptions in pilot
- [ ] 49. Conduct founder go/no-go review with evidence for every gate
- [ ] 50. Scale in measured stages only after successful approved pilot

## Current verified baseline
GitHub CI on earlier PR #109 head reported 30 synthetic tests passed, 0 failed; subsequent order-lifecycle and SQLite reservation changes require fresh verification.

## Release gates
Real customer data: NO-GO. Live billing: NO-GO. Real dispatch: NO-GO. External pilot: NO-GO until written permission, hosted controls, counsel review and founder sign-off.

## Next action
Execute CI for latest head; fix failures before proceeding to atomic multi-resource reservations. Link evidence to Bruce-to-Bruce ledger and this checklist.