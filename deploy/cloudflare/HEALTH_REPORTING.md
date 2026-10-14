# Maya Node runtime health reporting

The worker records its latest scheduled-run health in D1 runtime_health and logs only sanitized error codes. GET /health requires the existing controller bearer token. Reports exclude credentials, email bodies, and recipients. The latest record is overwritten by each run; this is not a permanent incident history.

For independent error alerts, configure ALERT_WEBHOOK_URL as a secret HTTPS endpoint accepting the JSON health report; optionally configure ALERT_WEBHOOK_TOKEN as its bearer credential. Do not route this endpoint through the same Gmail authentication. A missing route means no proactive external alert. Delivery failures are logged; webhook alerts are not durably queued or retried. Repeated failures can produce one alert per scheduled run.

Tests: node deploy/cloudflare/health-report.test.mjs. Verified locally: OAuth failure classification, secret redaction, persisted report, webhook delivery with mocked receiver, database failure fallback, endpoint authorization, scheduled authentication failure reporting. Production deployment and receipt have not been verified.

Activation: confirm Cloudflare build of the updated branch succeeds, inspect authenticated /health after a scheduled run, configure a controlled independent receiver, and verify a failure report arrives. An external monitor must separately check heartbeat freshness: a stopped worker cannot report its own outage. No external heartbeat monitor is configured by this change.
