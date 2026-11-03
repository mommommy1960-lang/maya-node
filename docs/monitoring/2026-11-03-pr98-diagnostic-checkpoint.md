# Maya Node PR #98 diagnostic checkpoint — 2026-11-03

Source: GitHub Actions run https://github.com/mommommy1960-lang/maya-node/actions/runs/41630046511

- Head commit: `5d69ef3c558c713f4e8b6bdeee2444bca1d32ca4` (PR #98, unmerged).
- BPI analyzer fixture tests: passed.
- Security & Ethics Checks: passed.
- Full-dataset workflow: failed at `Download original BPI Challenge 2019 XES`.
- GitHub job logs show `curl: (28) Connection timed out after 30002 milliseconds`, repeated, then exit code 28. Analysis and report upload skipped.
- Workflow downloads from `https://data.4tu.nl/file/35ed7122-966a-484e-a0e1-749b64e3366d/864493d1-3a58-47f6-ad6f-27f95f995828`; source reachability, HTTP headers, and integrity are NOT independently verified.
- Cloudflare PR preview build failed for commit `5d69ef3`; precise Cloudflare log cause NOT independently verified.
- Staging Whole Story analytics execution NOT verified. Hosted deletion/receipt durability, backup recovery, incident escalation, written business permission, external pilot feedback, and live payment readiness NOT verified.
- Customer data and live billing remain NOT AUTHORIZED. Do not merge or deploy to production.

Safest next step: test 4TU URL accessibility, HTTP response and redirect chain without substituting data; fix only the isolated download workflow after evidence; rerun with checksum and artifact verification. Obtain exact Cloudflare build logs before changing Wrangler bindings.

This record reflects verified GitHub evidence and explicitly labels unverified claims. No secrets or customer data included.
