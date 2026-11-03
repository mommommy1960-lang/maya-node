# Independent BPI source reachability checkpoint — 2026-11-03

PR: https://github.com/mommommy1960-lang/maya-node/pull/98

Attempted an independent web retrieval of the canonical 4TU DOI `https://doi.org/10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1` and the exact dataset download URL in `.github/workflows/bpi2019-full-data.yml`. The DOI retrieval timed out; the direct 4TU file URL could not be accessed through the independent web retrieval service. This does **not** establish that the official file is down for all networks, that the URL is invalid, or that DNS/TLS/proxy is specifically at fault.

GitHub Actions run https://github.com/mommommy1960-lang/maya-node/actions/runs/41639854367 failed with curl exit 28; the diagnostic artifact contains an empty response-header file and timeout stderr. Full authentic analysis remains unexecuted.

Next: validate official 4TU landing-page metadata and download URL through a reachable network, then collect bounded DNS/connect/TLS/HTTP-stage diagnostics on a GitHub runner. Do not change the dataset source to an unverified mirror, substitute fixtures, or repeatedly rerun an identical download. Verify dataset provenance, bytes, and checksum before declaring a full analysis.

Cloudflare Workers Build remains a separate unresolved investigation. PR #98 unmerged; synthetic-only testing; no real customer data, production deployment, or live billing.
