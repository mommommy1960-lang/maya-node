# Public-record scenario register
October 13, 2026. Primary public records; synthetic fixtures, not real personal data or faithful historical replays. The cited matters do not establish AI involvement.

## Billing: ABCmouse
FTC complaint filed September 1, 2020, paragraphs 39–42 (printed pages 16–18), describes alleged cancellation difficulties, continuing charges and base/add-on subscription confusion. The case record reports a settlement, not a trial verdict on every allegation.
- Complaint: https://www.ftc.gov/system/files/documents/cases/1723086abcmousecomplaint.pdf
- Case record: https://www.ftc.gov/legal-library/browse/cases-proceedings/172-3186-age-learning-inc-abcmouse

Derived synthetic test: base permission revoked; no separate add-on authority supplied; add-on charge blocked. Contrast fixture: distinct current add-on grant supplied; permitted action allowed. A base cancellation must not silently imply either that every other grant is valid or that every separate contract automatically ends. Actual terms and scope require verification.

Gap: a cancellation/account-login trap cannot be detected by the current grant predicate alone. A real pilot must test accessible cancellation, usable receipt, upstream state synchronization and protected alternate dispute intake.

## Schools/data: Edmodo
The FTC case record says it obtained an order concerning collection of children's information without required consent, advertising uses and outsourcing COPPA responsibilities to schools. The complaint describes educational-purpose authorization limits and inadequate notice.
- Case record: https://www.ftc.gov/legal-library/browse/cases-proceedings/202-3129-edmodo-llc-us-v
- Complaint, paragraphs 23–29 and 37–40: https://www.ftc.gov/system/files/ftc_gov/pdf/edmodocomplaintfiled.pdf

Derived synthetic test: an educational-use grant permits only its education action and does not authorize advertising. The code tests action scope, not compliance with consent law, notice sufficiency or age/identity verification.

Gap: organizational incident routing is not a blanket transfer of vendor responsibilities. Buyer personnel can own immediate operational response while provider duties, defect remediation and legal obligations remain separately mapped. Do not claim that Civic Continuum has no possible responsibility simply because it develops the software.

No verified public child-pickup incident was recovered in this search. The pickup scenario remains a founder-defined hypothetical; the Edmodo record concerns data handling, not physical release of a child.

## Payment revocation and resubmission
CFPB Regulation E 1005.10(c) and official interpretations address stop-payment and revoked authorization, including resubmitted debits and confirmation conditions.
Source: https://www.consumerfinance.gov/rules-policy/regulations/1005/10/

Derived fixture assumes valid effective revocation already established, then retries the same payee's charge three times. Each is blocked. This is a scoped software invariant, not a complete legal/payment implementation. Revoking automatic debit authorization does not necessarily cancel the underlying debt or contract.

Observed gap: three attempts create three cases. Stable incident grouping and idempotent case creation need implementation; repeated requests must not fragment response ownership.

## Local result
Run:
```sh
python -m unittest tests.integration.test_public_record_scenarios tests.integration.test_accountability_sandbox tests.integration.test_accountability_demo tests.integration.test_consent_token_demonstrator -v
```
Observed 28 passes: four new public-record-inspired scenario checks plus the prior 24 checks. Separate model sweep: 2,256 synthetic decisions matched expected labels. Do not combine these denominators or call them independent representative field trials.

Another synthetic case verifies that a correction remains open when independent review rejects it. This is our design requirement, not a claim about either historical company's actual incident platform.

## Next proof
Integrate actual authorization sources and cancellation state; add incident deduplication and alternate protected intake; test vendor/buyer responsibility maps and reachable human responders. Obtain a partner's representative workload and measured field outcomes before a 99% reliability claim.
