# Maya Node: isolated synthetic HTTP byte-boundary verification

**Date:** November 8, 2026, America/Los_Angeles. **Scope:** Draft PR #109, loopback-only fictional pantry workflow. No production deployment or live customer integration.

## Defect corrected

The local demo JSON reader previously used JavaScript string length instead of UTF-8 payload bytes and destroyed the HTTP socket upon limit violation. Multi-byte text could pass the nominal 2,048-byte request boundary, and socket termination could prevent callers from receiving a useful rejection response.

The synthetic HTTP reader now counts actual incoming Buffer bytes, bounds retained request memory to 2,048 bytes, rejects and drains over-limit input without destroying the socket, and returns HTTP **413** with a machine-readable `request_too_large` error. Exact-boundary valid JSON remains accepted. Existing test-only tenant permission ordering is preserved: denied principals receive 403 before the body is parsed.

Implementation: [source commit 8595062aab11b56e21ae6c5f40a64161a93c8baa](https://github.com/mommommy1960-lang/maya-node/commit/8595062aab11b56e21ae6c5f40a64161a93c8baa). Four new byte, Unicode, boundary, denied-principal and legacy-route regression cases: [test commit bb024e6fb0dfca5760d8de0fed6cfc1db9b36cec](https://github.com/mommommy1960-lang/maya-node/commit/bb024e6fb0dfca5760d8de0fed6cfc1db9b36cec).

## Independently inspected CI at exact source/test commit bb024e6

- [Pantry watchtower synthetic tests: run 42513455123](https://github.com/mommommy1960-lang/maya-node/actions/runs/42513455123), job **128831265251**: **182 tests passed, 0 failed, 0 skipped**, verified against the decoded job's TAP summary.
- [Pantry fictional order browser integration: run 42513455128](https://github.com/mommommy1960-lang/maya-node/actions/runs/42513455128), job **128831265410**: **two PASS** messages for actual Chromium → local HTTP → SQLite full and partial fictional journeys. **These browser paths remain the deliberately unguarded demo; they do NOT verify hosted or authenticated customer access.**
- [Security & Ethics Checks: run 42513455163](https://github.com/mommommy1960-lang/maya-node/actions/runs/42513455163): all **five** jobs succeeded, including core runtime, security scanning, ethics constraints, adaptive red-team and Nightwatch. Passing scans do not amount to independent production security approval.

## Remaining risk and next priorities

This is bounded-resource and predictable-response hardening only, not a genuine login system. Header-derived principals are spoofable local test doubles. A protected browser journey with authentic revocable hosted sessions is still missing, as are provider-delivered Stripe TEST webhook-to-order verification, hosted record deletion/isolated recovery and retention proof, staffed incident backup, written donor/receiver/transporter permissions, and independent legal and food-safety approval.

**Readiness:** Verified synthetic CI checkpoint for November 8 **met**; hosted browser goal for November 10–14 **open**; November 21–December 19 is only a conditional evidence-based limited-pilot decision period. Real customer records, real dispatch, outbound messages, partner integrations, live billing and production launch remain **NO-GO**. PR #109 remains draft/unmerged; no Site or production deployment was made. Do not mistake more passing tests for a completed release gate.
