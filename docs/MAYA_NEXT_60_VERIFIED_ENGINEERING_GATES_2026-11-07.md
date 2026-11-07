# Maya Node — next 60 verified engineering acceptance gates
2026-11-07. Continuation beyond existing 50-step plan. These are NOT completed tasks. Synthetic development only until independent gates and founder approval.

Every checked item requires test/log/commit evidence and a reviewer. Do not mark complete merely because code exists.

## Concurrency and atomicity
- [ ] 1. Cross-process simultaneous claims on one truck
- [ ] 2. Cross-process simultaneous claims on food quantity
- [ ] 3. Cross-process simultaneous claims on freezer capacity
- [ ] 4. All-or-nothing three-resource hold
- [ ] 5. Repeat request idempotency across workers
- [ ] 6. Rollback on third-resource failure
- [ ] 7. SQLite busy-timeout contention behavior
- [ ] 8. Crash during transaction and restart recovery
- [ ] 9. Reservation expiry race against approval
- [ ] 10. Cancellation race against pickup

## Order integration
- [ ] 11. Persist orders in transactional store
- [ ] 12. Bind order IDs to reservation bundle IDs
- [ ] 13. Reject approval if reservation expired
- [ ] 14. Verify donor identity and approval evidence
- [ ] 15. Verify recipient identity and approval evidence
- [ ] 16. Verify transporter identity and confirmation
- [ ] 17. Enforce pickup-after-approval invariant
- [ ] 18. Prevent duplicate pickup and delivery events
- [ ] 19. Handle partial pickup and partial delivery
- [ ] 20. Release capacity on terminal cancellation

## Data integrity
- [ ] 21. Append-only event provenance
- [ ] 22. Tamper-evident event sequencing
- [ ] 23. Source timestamp validation
- [ ] 24. Timezone-safe deadlines
- [ ] 25. Lot-level handling and allergen flags
- [ ] 26. Cold-chain temperature evidence
- [ ] 27. Storage capacity freshness validation
- [ ] 28. Reconciliation of rejected and damaged units
- [ ] 29. Duplicate receipt and forged signer checks
- [ ] 30. Corrective event without erasing history

## Security and resilience
- [ ] 31. Tenant-isolated authorization tests
- [ ] 32. Least-privilege operator roles
- [ ] 33. Secrets rotation rehearsal
- [ ] 34. Webhook signature and replay protection
- [ ] 35. Hosted deletion proof
- [ ] 36. Retention and backup purge semantics
- [ ] 37. Backup restore drill
- [ ] 38. Disaster recovery measured objectives
- [ ] 39. Incident owner and escalation chain
- [ ] 40. Rollback and emergency pause drill

## Customer experience
- [ ] 41. Real browser module import test
- [ ] 42. Mobile Android layout test
- [ ] 43. Keyboard accessibility test
- [ ] 44. Screen-reader labels test
- [ ] 45. Translation quality review
- [ ] 46. Consent and notification controls
- [ ] 47. Visible blocked-reason explanation
- [ ] 48. Human approval review screen
- [ ] 49. Quote and agreement review screen
- [ ] 50. Cancellation and support flow

## Commercial and pilot
- [ ] 51. Sandbox payment authorization
- [ ] 52. Sandbox payment failure recovery
- [ ] 53. Sandbox refund and reversal
- [ ] 54. Ledger/payment reconciliation
- [ ] 55. Service-fee disclosure
- [ ] 56. Food recipient no-charge invariant
- [ ] 57. Partner integration permission review
- [ ] 58. Written donor receiver transporter pilot permission
- [ ] 59. Food-safety legal and insurance signoff
- [ ] 60. Founder evidence-based go/no-go decision

Release remains NO-GO for real customer data, real dispatch, and live billing.