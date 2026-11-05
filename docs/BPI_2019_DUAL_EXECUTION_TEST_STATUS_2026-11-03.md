# BPI Challenge 2019 — Dual Execution Test Status

**Date:** 2026-11-03  
**Status:** Analyzer scaffold and fixture tests completed; full-dataset analytics and authenticated Maya execution remain pending  
**Owner:** Civic Continuum / Maya Node

## Decision

Run two distinct executions against the same authorized BPI Challenge 2019 source evidence:

1. **Standalone analytics:** the Civic Continuum / Whole Story analysis code runs against the original BPI event log.
2. **Maya Node execution:** the same frozen input and analysis version are submitted to an authenticated, isolated Maya Node analytics capability; outputs, evidence references, timing, and errors are captured.

These are separate tests. A local Python result is not evidence that Maya Node executed the analysis.

## Authoritative dataset

- Creator: Boudewijn van Dongen (2019), *BPI Challenge 2019*.
- DOI: https://doi.org/10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1
- Dataset record: https://research.tue.nl/p/en/datasets/bpi-challenge-2019
- Original XES file reference: https://data.4tu.nl/file/35ed7122-966a-484e-a0e1-749b64e3366d/864493d1-3a58-47f6-ad6f-27f95f995828
- Published source description: 76,349 purchase documents, 251,734 line-item cases, 1,595,923 events, 42 activities, and 627 users (including human and batch users).
- Dataset purpose: investigate purchase-order handling, goods receipt, invoice receipt, invoice clearing/payment, matching rules, process throughput, and deviations.
- License/attribution must be verified against the source record before redistribution of data or derived files.

## Dataset fit and limitations

This is real, anonymized purchase-to-pay process evidence. It is suitable for examining purchase-order / goods-receipt / invoice activity and matching rules. It does **not** supply the four distinct systems in the synthetic Whole Story Challenge (WMS, carrier, customer support, and finance) as separate source feeds. It does not provide independent ground-truth dispositions for every exception. Results must therefore be described as purchase-to-pay event-log analysis, not as a full warehouse/carrier/support/finance reconciliation.

The source record explains that some purchase items require three-way matching, some two-way matching, and some consignment handling. Rules must be stratified by item type; a simplistic requirement that every case contain all event types would create false positives.

## Test A — Standalone analytics

**Status: Not yet executed against the original full dataset.**

The original file is approximately 728 MB. The current execution environment could not retrieve it from the 4TU file endpoint, and outbound DNS/network access from the local execution container is unavailable. No full-data metrics, exception counts, or performance claims are reported in this record.

Required run:
1. Retrieve the original source file from 4TU ResearchData, without changing or transforming the source.
2. Record file size, SHA-256, source URL, retrieval date, and license/attribution.
3. Parse the XES event log in a streaming manner.
4. Validate counts against the published figures before analysis.
5. Segment by the four purchase-item flow categories / applicable matching flags.
6. Calculate process variants, event ordering, throughput intervals, missing/late/duplicate or contradictory records where supported, and monetary reconciliation where source fields permit.
7. Export a machine-readable report with row-level evidence references and explicit indeterminate classifications.
8. Re-run the same input and code version to verify reproducibility.

No financial recovery, avoidable loss, fraud, causation, ROI, or savings claim may be inferred solely from an event-log deviation or an anonymized monetary value.

## Test B — Maya Node

**Status: Read-only reachability test completed; authenticated analytics execution not yet possible.**

A read-only GET was performed against:

`https://maya-recovery-staging.mommommy1960.workers.dev/health`

Observed result:
- HTTP 401 Unauthorized.
- Response indicated that a bearer token is required.
- The service is reachable and the protected health route is enforcing authentication.
- No token was supplied or requested; no data was submitted and no state was changed.

Repository inspection of `deploy/cloudflare/worker.mjs` on `main` found handlers for:
- `GET /health`
- `GET /status`
- `POST /enqueue`
- `POST /approve`
- `POST /cancel`
- `POST /stripe/webhook`

The inspected Worker is a bounded email/payment handoff service. It does not currently expose a BPI/XES ingestion or Whole Story analytics route. The staging URL is documented as the separate `maya-recovery-staging` Worker; it must not be confused with a verified production Maya Node analytics service.

Therefore, the live test has so far verified reachability and authentication only—not analytics ingestion, execution, result correctness, or performance.

## Required isolated implementation before Test B can pass

Create an independently testable analytics module and a dedicated authenticated staging route, separate from Stripe, payment, D1 mail queues, and outbound email. The route must:
- accept only a bounded, documented input format;
- validate schema, file size, encoding, and event limits;
- calculate a SHA-256 input fingerprint and identify the analysis version;
- invoke the same analysis logic/version as Test A;
- return findings with source event/case references, confidence/uncertainty, and execution metadata;
- never send email, create charges, change entitlements, or mutate business records;
- use an isolated staging deployment and preserve the existing production Worker, secrets, bindings, DNS, and payment behavior.

The route cannot be considered live until deployed to the intended staging environment and exercised with the exact same frozen dataset. An unauthenticated 401 is an expected security result, not a failed service test.

## Comparison protocol

Both runs must use:
- the same source file SHA-256;
- the same data dictionary and matching-rule specification;
- the same timezone and timestamp interpretation;
- the same analysis version and output schema;
- the same case population and exclusions.

Compare:
- cases/events processed and rejected;
- process variants and throughput calculations;
- supported exception counts by category;
- false positives only where an independently adjudicated reference label exists;
- evidence traceability and reproducibility;
- wall-clock runtime, memory/resource use, and operational cost;
- indeterminate/unsupported cases.

A baseline manual or established process-mining implementation must be run on the same frozen data before claiming an advantage. Public vendor documentation is not a substitute for a measured competitor run.

## Current conclusion

The dual-test work has begun and is tracked in PR #98: https://github.com/mommommy1960-lang/maya-node/pull/98. The streaming analyzer and fixture tests are committed on the branch; the original full BPI dataset has not yet been processed. The live staging Worker is reachable and protected, but the inspected implementation does not yet contain the required analytics capability. No superiority, ROI, recovery, or customer-readiness claim is established.
