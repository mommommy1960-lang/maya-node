# Bruce-to-Bruce Checkpoint — Business Viability, Maya Tests, and Registration
Date: 2026-10-27
Owner: Civic Continuum founder
Purpose: Preserve exact assessment, avoid duplicate outreach, and resume from verified evidence.

## 1. Preserved business viability assessment
The founder asked that the complete assessment from the prior ChatGPT answer be saved verbatim and retrieved whenever she asks whether Civic Continuum is worth pursuing.
Canonical saved copy:
https://github.com/mommommy1960-lang/maya-node/blob/main/docs/CIVIC_CONTINUUM_BUSINESS_VIABILITY_ASSESSMENT_PRESERVED_2026-10-27.md
Commit: 52895473c95780be74f04e054d2fa79ef4abca9a
Do not replace this assessment with a shorter summary when the founder asks to pull it back out. It can be supplemented by dated evidence, but preserve the original text.

## 2. Austin outreach — avoid redundancy
Repository history already contains the Austin & Team Controlled Test Guide:
https://github.com/mommommy1960-lang/maya-node/blob/main/docs/AUSTIN_TEAM_CONTROLLED_TEST_GUIDE_2026-10-26.md
The guide covers synthetic-data testing, permission, output bytes, receipts, revocation, and safe deletion.
The latest outreach record says Austin Irvan's direct-message thread was last answered by the owner and is awaiting his response; no extra nudge was sent. The Gmail connector was reported DISABLED_BY_ADMIN, and no message was read or sent in that review.
Therefore: do not send Austin another generic invitation or repeat the same instructions. Wait for his response or use an already-authorized channel to share the existing guide only when needed. Do not claim he or his team has begun testing until evidence arrives.

## 3. Maya Node verification — current evidence and gates
- Draft PR #77 expands the inventory and distinguishes the local React/Vite consultation site, offline workflow lab, and separately hosted server-backed Maya Accountable Actions application.
- Issue #76 remains the readiness tracker.
- Historical October 16 evidence describes 17 SQLite service tests and a prior hosted authorized action, revocation block, and receipt persistence/download. Treat this as historical evidence only.
- CI run 40383680850 reportedly passed five configured jobs, but it was documentation-triggered and is not a fresh hosted deletion test.
- The 18-case map covers DEL-01–08 and REC-01–10 provisionally; several cases remain unestablished, including repeat deletion, failure atomicity, preservation of unrelated records, human-handoff receipt, endpoint-specific cross-user behavior, retention/backups, and stored-vs-downloaded receipt comparison.
- The Cloudflare preview build for commit 7ed19e42354d31326f6c616f470bd54e7bfbb028 reported FAILED. Diagnose from build logs before assuming the cause. This alone does not establish production is down.
- The checked-in Cloudflare mail/dispatch worker is an opt-in staging port, not identified as the hosted customer workflow.
- No production code was changed or deployed; no hosted customer records were deleted or modified.

## 4. Required technical next steps
1. Obtain the hosted Maya Accountable Actions application's source repository or source export and identify its build/deployment owner/location.
2. Inspect the actual deletion and receipt implementation and map each of the 18 cases to real functions and tests.
3. Run fresh targeted tests in an available authorized environment; record exact command, commit, test result, and limitations.
4. Use a verified disposable hosted account and synthetic data for authorized end-to-end deletion/receipt checks.
5. Verify current retention/backup behavior, multi-user isolation, incident contact/escalation, and written partner permission before any live customer data or pilot.
6. Keep issue #76 open until the evidence gates are met. Do not label untested cases passed or failed.

## 5. Washington business registration — confirmed records and unknowns
- Existing IRS EIN was assigned September 26, 2026 to the founder as a sole proprietor; confirmation is retained privately. Do not apply for another EIN. Do not publish the EIN or confirmation letter.
- Current documented structure is sole proprietorship. No Washington LLC formation is verified as filed or accepted.
- Washington UBI, Civic Continuum trade-name registration, and Seattle business-license/endorsement status remain unverified in the records reviewed.
- Washington DOR official schedule states $50 non-refundable processing fee to open the first location of a new business/UBI or reopen one with no active locations. This is the application processing fee, not a guarantee that the entire checkout total is $50.
- Applicable endorsement/trade-name fees may be added. Prior budget records estimated Civic Continuum trade name $5 if not already registered and Seattle licensing $36.50 or $73 depending on qualifying start date and applicability. These must be checked against the live application and actual location/endorsement rules before payment.
- UBI and DOR tax registration are not separately purchased; the UBI is issued through the process. IRS EIN is free and already obtained.
- A Washington LLC is a separate choice and is not needed merely to apply as a sole proprietor. If forming an LLC later, the state fee is $180 plus online processing fee, with optional expedite fee; do not initiate without explicit founder approval.
- No $50 payment or completed DOR application submission has been verified in this checkpoint. A prior startup budget and SBDC application exist, but they are not proof that the DOR business-license application is ready to submit.

Official sources:
https://dor.wa.gov/open-business/apply-business-license/variable-business-license-processing-fees
https://dor.wa.gov/open-business/apply-business-license
https://dor.wa.gov/manage-business/grow-business/register-trade-names
https://seattle.gov/city-finance/business-taxes-and-licenses/business-licenses
https://www.sos.wa.gov/corporations-charities/business-entities/online-filing-instructions/start-domestic-wa-limited-liability-company-llc-online

## 6. Founder instruction
The founder wants to proceed with Maya Node's five verification actions, avoid redundant Austin outreach, retrieve the full preserved viability assessment whenever she asks whether the business is worth it, and pay the Washington DOR $50 opening application fee if the correct application and final total are verified. Do not make a payment or submit an application without explicit authorization at the actual payment/submission step.
