# Portable sector workflow lab — October 16, 2026

Open `demos/offline_workflow_lab.html` directly in a browser. No Cloudflare, API key or server is required. Eight fictional scenarios cover housing, food-bank operations, account creation, subscriptions, schools, banking, nonprofit intake and support.

Run `node --test tests/test_workflow_lab.mjs`. Twenty functional checks evaluate the actual inline JavaScript in a simulated DOM. Existing checks remain unchanged: thirteen core-model checks and eight browser-demo contract checks pass. These are bounded prototype checks, not a browser accessibility audit or production security assessment.

Demonstrated: scope and purpose limits, revocation checked at execution, expiry, named owner coverage, separate correction reviewer, and a simulated USD5 one-time payment cap. All data and actions are fictional. Browser state is editable. No actual account, charge, subscription cancellation or notification occurs.

The hosted AI product remains gated by deployment access, provider billing and production identity/payment verification. Changing hosting providers does not resolve those independent gates.

## Business record
Existing business records document an EIN assigned September 26, 2026, to the founder as a sole proprietor. The identifier and tax letter remain private. Washington and Seattle licensing remain unverified. An EIN is not evidence of incorporation, licensing or certification.

## Customer hypotheses
Test subscription operations first; validate housing-service and food-bank workflows alongside it. Banking and schools are longer-term validation prospects. Buyer demand, procurement timelines and budgets remain unverified. Keep all pilot discovery fictional until written data-handling requirements and business readiness are established.
