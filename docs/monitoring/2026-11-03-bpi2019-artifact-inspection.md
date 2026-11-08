# BPI 2019 artifact inspection — 2026-11-03

Source run: https://github.com/mommommy1960-lang/maya-node/actions/runs/41639854367
Diagnostic artifact: https://github.com/mommommy1960-lang/maya-node/actions/runs/41639854367/artifacts/13232286665

Inspected the actual ZIP contents: download_error.txt, download_headers.txt, download_status.txt.

Verified: four curl attempts each timed out after approximately 15,002 milliseconds, exit code 28. No HTTP response headers were recorded (headers file is empty). No dataset was downloaded, and full analysis and report steps were skipped. The diagnostics upload succeeded. This is a connection-establishment timeout, not evidence of an HTTP 403/404 or an analyzer defect. Exact network cause remains unknown.

Next safe action: verify authoritative 4TU download endpoint and redirects from an independent network, inspect DNS/TLS/proxy connectivity from GitHub runner, then change the isolated workflow only with a validated source and integrity verification. Avoid repeated identical retries and do not substitute a sample as a full result. Cloudflare build requires separate exact logs. PR #98 stays unmerged; production, real customer data, and live billing remain blocked.
