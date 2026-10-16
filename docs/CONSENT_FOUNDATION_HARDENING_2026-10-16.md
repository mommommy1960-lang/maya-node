# Consent foundation hardening — October16,2026

Eight new regression tests exercised expiry at the deadline, session/batch restoration, expired targets, fresh-token replay, wrong owner, malformed signature and invalid TTL. On the unmodified source: eight test methods ran, with nine failing subcases and two type errors. Three methods already passed.

After the patch:19 runtime tests pass (11 existing +8 regressions), plus4 existing integration/ledger tests pass. The separate offline browser lab previously passed23 Node checks; these are different suites, not a shared production metric.

Patch scope: reject non-positive/non-finite TTL and invalid TTL types; use hmac.compare_digest with malformed-signature rejection; expire at now >= expires_at; require single-operation restore authorization; deny restoration of an expired target before consuming fresh permission.

Still an in-memory, process-local component. Exposes mutable token objects; lacks durable/atomic distributed consumption, verified identity, complete resource-bound authorization and integration enforcement. No security audit, production deployment, external certification or competitor superiority claimed.

Python primary documentation: https://docs.python.org/3/library/hmac.html .
