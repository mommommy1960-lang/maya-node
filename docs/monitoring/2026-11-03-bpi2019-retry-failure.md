# BPI 2019 retry failure — 2026-11-03

## Verified evidence
- Workflow: https://github.com/mommommy1960-lang/maya-node/actions/runs/41630046511
- Retry job ID: `125907901227`.
- Fixture tests passed again.
- Authentic dataset download failed again: six `curl (28)` connection timeouts at 30 seconds each, final exit code 28.
- Full analysis and artifact upload were skipped. No full-dataset result exists from this retry.
- Current download URL in workflow: `https://data.4tu.nl/file/35ed7122-966a-484e-a0e1-749b64e3366d/864493d1-3a58-47f6-ad6f-27f95f995828`.

## Interpretation
The repeated failure is connectivity/retrieval, not evidence of an analyzer result. Exact underlying cause (network, remote host, URL, or redirect) is NOT verified. Do not substitute a synthetic file or claim full-source execution.

## Next safe actions
1. Verify authoritative BPI 2019 dataset metadata and reachable download endpoint, including redirect and HTTP status.
2. Modify isolated workflow only after validating the endpoint, with content validation and checksum recorded.
3. Rerun and verify generated report artifact before considering staging analytics.
4. Independently obtain Cloudflare build logs; Wrangler validation as root cause is not confirmed.

Production, payments, and real customer data remain untouched and unauthorized.
