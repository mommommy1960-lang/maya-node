# Hosted invoice, pantry journey and recovery checkpoint

November 4, 2026. Live site: https://maya-working-workflow-lab.myqueen1960.chatgpt.site

Separate Sites source revisions: v22 55a7273b9078749e8614da3236d7974c82306b42; current v23 5e900dfe5d94afe13e0bdd8824b5602e3d30e372. These SHAs belong to the Sites source repository, not this GitHub repository.

- Implemented browser-local invoice CSV review, with duplicate/history/approval-amount checks, held rows and clear limits. Sample USD2,550 is fictional invoice face value, not losses or savings. v23 labels that explicitly and shows amount above approval separately.
- Implemented account-scoped pantry journeys with event time versus record time, server account attribution, reported handler/authorizer, location, quantity/value, reason/source references, append-only corrections through the application, hash linkage and portable JSON export.
- Hosted five-event fictional batch reconciled100 received minus60 distributed minus5 waste to35 remaining, with recorded unit valuation2.50. A50-bag allocation was held. Downloaded archive hashes were recomputed outside the site and matched all events/head/sequence.
- Implemented signed account note backups and missing-record restoration. Old active grants reset; expired and intentionally deleted records excluded; existing records never overwritten. The note backup is not a complete product-journey/billing/provider backup.
- Hosted recovery drill reconstructed a fictional completed output and original receipt in separate D1 fixture tables after simulated loss, and reset an exported active grant. Result persisted. Live account tables were not cleared. Full provider disaster recovery and provider backup/log retention remain unverified.
- MCP initialization instructions and maya_get_user_guide provide current onboarding. Guide tool was discovered and called successfully. No tool can authorize creation.
-122 automated checks passed for v22, with transactional restore, account boundaries, tamper/expiry/deletion/overwrite protection, journey-chain/correction/concurrency and invoice edge cases. v23 six invoice checks and build passed; calculations unchanged.
- Browser file-upload test later hung. Its result is unconfirmed; do not describe that browser import/no-overwrite test as passed. The earlier hosted drill and automated restore tests are separate successful evidence.

No bank/accounting connector, external company AI-agent ingestion, independently verified named approvers, source-document store for journeys, measured customer financial savings or 20-year hosting guarantee is claimed. Hash chains alone do not establish independent operator trust.
