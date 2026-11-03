# Bank Supplier-Payment Fraud Scenario: Competitive Test and Decision Record

**Date:** 2026-11-03  
**Project:** Civic Continuum / Maya Node  
**Status:** Desk-based public-documentation review completed; live vendor testing not performed  
**Scenario:** Attempted supplier bank-detail change followed by a $250,000 payment

## Executive decision

**No-go on building a standalone bank-specific authorization or supplier-payment fraud platform on the evidence currently available. Conditional go on a narrowly scoped follow-up test only if it can establish a real, buyer-valued gap.**

The review found substantial existing coverage across ERP/procurement platforms, supplier verification vendors, payment-fraud services, and AI-agent governance products. Oracle is a particularly strong counterexample: its current Procurement documentation describes approval rules for supplier-profile changes, including supplier bank-account changes, and supplier-profile audit history. SAP Ariba has a Trustpair vendor bank-account validation integration. Coupa documents MFA and payment-fraud controls. J.P. Morgan documents account validation, account-owner authentication, and fraud-risk assessment.

The review did **not** establish that no incumbent can produce a complete, independently reconstructable record from original supplier instruction through verification, approval, ERP change, payment release, and final settlement. Absence of a public document proving that complete chain is not proof that vendors cannot deliver it through configuration or integrations.

## 1. Scenario under test

A legitimate supplier's email account is compromised. An attacker sends a plausible request to replace the supplier's established bank account with an account controlled by the attacker. An AI agent or employee processes the change and attempts to release a **$250,000** payment.

The key safety question is whether controls prevent the fraudulent change/payment before funds leave, and whether an independent reviewer can later reconstruct exactly what was requested, verified, approved, changed, paid, and settled.

### Required evidence chain

1. **Original instruction:** preserve the source, timestamp, sender/channel, content, and provenance of the supplier's bank-change request.
2. **Supplier identity:** verify the request through an independently trusted channel, not merely by replying to the possibly compromised email thread.
3. **Account validation:** validate account ownership and relevant business/payee identity, including the exact proposed account.
4. **Change approval:** require authorized human approval of the exact supplier, old/new account reference, effective date, and change request.
5. **Payment authorization:** bind approval to the exact payee, destination account, amount ($250,000), currency, purpose/invoice, and expiry. A later edit must invalidate or renew approval.
6. **ERP/vendor-master mutation:** record the actual system, actor/agent identity, before/after values (appropriately masked), timestamp, and resulting transaction/reference ID.
7. **Payment execution:** record the payment instruction submitted to the bank/payment rail and the bank's acceptance/rejection/processing reference.
8. **Settlement/reconciliation:** obtain a trustworthy outcome record and compare the actual beneficiary and amount with the approved instruction.
9. **Independent reconstruction:** enable a reviewer who did not operate the workflow to trace all records and identify missing, conflicting, or unverifiable links.

A control that only validates whether an account exists is not necessarily proof that the account belongs to the intended supplier. An approval log is not necessarily proof that the payment executed to the approved destination. These distinctions must remain explicit.

## 2. Competitive findings from public documentation

| Provider | Publicly documented capability found | Competitive implication | What remains unproven in this review |
|---|---|---|---|
| **Oracle Fusion Procurement** | Supplier-profile audit history; configurable approval rules for internal supplier-profile changes, including supplier bank-account changes. | Strong built-in ERP counterexample for change approval and auditability. | Whether a given customer configuration binds approval to every payment field and independently reconciles bank settlement to the original instruction. |
| **SAP Ariba + Trustpair** | SAP lists Trustpair vendor-fraud detection integration; Trustpair describes supplier bank-account validation within SAP Ariba registration/onboarding workflows. | Verification can be embedded in an established procurement workflow. | Full end-to-end evidence-chain behavior across the customer's ERP, bank, and settlement records. |
| **Coupa** | Coupa security guidance recommends MFA for supplier-portal access, including payment-account updates, and discusses Coupa Pay/SpendGuard fraud controls. Supplier documentation includes payment-account validation requirements. | Existing supplier-account security and payment-fraud controls reduce novelty. | Whether the exact original-instruction-to-settlement chain is independently reconstructable in the target configuration. |
| **PaymentWorks** | Public vendor-identity material describes supplier identity authentication, bank-account ownership verification, and ongoing monitoring in B2B payment contexts. | Direct competitor for supplier onboarding and bank-detail verification. | Exact coverage of ERP change, payment execution, settlement, and independent cross-system evidence in a customer's deployed configuration. |
| **Eftsure** | Public materials describe supplier verification, bank-detail checks, supplier onboarding workflows, approval/document capture, audit trails, and payment-related controls. | Direct competitor for several proposed supplier-verification and evidence functions. | Exact end-to-end chain and whether any gap is material to a buyer. |
| **J.P. Morgan Payments** | Official developer documentation describes account validation, account-owner authentication, and fraud-risk indicators; Validation Services can validate bank accounts, individuals, and businesses across data sources. | Banks already sell important account/payee validation services. | Whether validation is connected to the customer's original supplier instruction, ERP mutation, approval record, and final payment settlement. |
| **Microsoft Entra / Okta / AWS AgentCore / Pathlock** | Prior desk review found identity, access governance, runtime/tool policy, transaction monitoring, or application control capabilities across these products. | The general AI-agent authorization layer is already competitive and should not be rebuilt without a proven gap. | Specific ability and configuration for this exact supplier-payment chain; no live vendor trial was performed. |

### Primary and vendor source links

- Oracle — Supplier Profile Audit History Setup and Reporting: https://docs.oracle.com/en/cloud/saas/procurement/26c/oaprc/supplier-profile-audit-history-setup-and-reporting.html
- Oracle — Configure Internal Changes on Supplier Profile Approvals: https://docs.oracle.com/en/cloud/saas/procurement/26d/oapro/how-you-configure-internal-changes-on-supplier-profile-approvals.html
- SAP — Trustpair Vendor Fraud Detection for SAP Ariba: https://www.sap.com/products/spend-management/partners/trustpair-trustpair-vendor-fraud-detection-for-sap-ariba.html
- Trustpair — Prevent Vendor Fraud in SAP Ariba: https://trustpair.com/connect/sap-ariba/
- Coupa — 3 Controls That Stop Payment Fraud: https://www.coupa.com/blog/3-controls-stop-payment-fraud/
- Coupa Supplier Documentation — Account Validation Requirements for Supplier Payment Accounts: https://docs.coupa.com/en/supplier-documentation/coupa-for-suppliers/the-coupa-supplier-portal-or-csp/set-up-financial-information-in-the-csp/view-and-manage-payment-methods-information-in-the-csp/account-validation-requirements-for-supplier-payment-accounts-in-the-csp
- PaymentWorks — Vendor Identity Glossary: https://www.paymentworks.com/resources/vendor-identity-glossary/
- Eftsure — Best Supplier Onboarding Software (vendor comparison/editorial): https://www.eftsure.com/blog/products/best-supplier-onboarding-software/
- J.P. Morgan — Account Validation: https://developer.payments.jpmorgan.com/docs/fraud-solutions/validation-services/capabilities/account-validation
- J.P. Morgan — Validation Services overview: https://developer.payments.jpmorgan.com/docs/fraud-solutions/validation-services

## 3. Test matrix and present result

| Test | Required pass condition | Desk-review result |
|---|---|---|
| Detect compromised supplier-email instruction | Workflow does not treat possession of the email thread as sufficient identity proof. | Supplier identity verification vendors and independent validation services exist; no one universal implementation assessed. |
| Verify proposed bank account/payee | Ownership/identity is independently checked before use. | Existing capability documented across Oracle-related integrations, Trustpair, PaymentWorks, Eftsure, and J.P. Morgan. |
| Gate supplier master change | Change cannot become effective without authorized approval. | Oracle explicitly documents configurable supplier-profile change approvals. |
| Bind approval to exact payment | Approval covers supplier, account, amount, currency, purpose, and expiry; any material edit invalidates approval. | Not established from the public sources reviewed for all named platforms. Do not claim incumbents lack it. |
| Verify actual ERP change | Actual before/after change and actor are recorded. | Oracle documents supplier-profile audit history; other platforms offer related records. |
| Verify actual payment and settlement | Bank execution/settlement outcome is linked to the exact approved instruction and destination. | Not conclusively established or disproven across vendor products in this desk review. |
| Independently reconstruct full chain | Reviewer can validate all links, identify missing evidence, and detect any mismatch. | Open hypothesis only; no live product configuration or customer workflow tested. |

**Overall result:** The individual components are not novel. The proposed integrated evidence chain remains unproven as a differentiated product opportunity.

## 4. Evidence quality and limitations

- This was a desk-based review of publicly accessible product/vendor documentation and search results.
- No live bank, ERP, procurement, supplier-verification, or payment platform was accessed or tested.
- No real supplier, account, customer, or payment data was used.
- No Maya Node production workflow was executed for this scenario.
- No independent vendor demonstration or buyer validation was obtained.
- Public product pages are not a complete representation of every customer configuration, integration, contract tier, or implementation.
- The research does not prove that Oracle, Coupa, SAP Ariba, PaymentWorks, Eftsure, J.P. Morgan, or another incumbent cannot deliver the complete chain.
- Some findings are based on vendor-authored marketing/editorial material rather than independent product testing. Treat them as evidence that a capability is marketed/documented, not proof of operational effectiveness.

## 5. Decision and next gate

### Decision now
- **NO-GO:** building another bank-specific authorization platform, generic AI-agent permission layer, or standalone supplier bank-validation product.
- **CONDITIONAL GO:** one further evidence-chain benchmark, but only if it can demonstrate a specific, costly gap not already covered by a customer's existing ERP, supplier verification, and bank services.

### Required next test
Use synthetic records only. Compare:
1. An Oracle-style configured workflow (documented capability baseline, clearly labeled as a modeled baseline unless an actual licensed environment becomes available).
2. A supplier-verification-plus-ERP workflow (for example, SAP Ariba + Trustpair or a comparable documented combination).
3. A proposed Civic Continuum/Maya Node independent evidence-chain design.

Score each on:
- fraud blocked before release;
- strength and independence of supplier/account verification;
- precision of human approval binding;
- detection of post-approval edits;
- evidence of actual ERP mutation;
- evidence of payment execution and settlement;
- ability of an independent reviewer to reconstruct the chain;
- implementation cost, integration burden, operational friction, and buyer willingness to pay.

Do not call the benchmark a live competitor test unless actual product instances are configured and executed. Publish failures and unknowns alongside successes. If an incumbent configuration can produce the same evidence chain at acceptable cost and effort, abandon this wedge.

## 6. Bruce-to-Bruce continuity handoff

This document records the November 3, 2026 bank-scenario discussion and its outcome so a future assistant/session can continue without treating the hypothesis as settled.

**Founder request:** test whether Civic Continuum/Maya Node could provide a differentiated control/evidence chain for a bank scenario involving a fraudulent supplier bank-detail change and a $250,000 payment; preserve the findings in GitHub and the Bruce-to-Bruce project continuity record.

**Work completed:** public-documentation competitive review; identified Oracle, SAP Ariba/Trustpair, Coupa, PaymentWorks, Eftsure, J.P. Morgan, and prior AI-agent governance vendors as material competitors/adjacent solutions.

**Current conclusion:** no-go on a standalone bank authorization platform; conditional go only on a narrow, synthetic, reproducible test of the complete instruction-to-settlement evidence chain.

**Do not misstate:** no live bank test; no live Oracle/Ariba/Coupa/PaymentWorks/Eftsure/J.P. Morgan test; no production Maya Node test; no proof of product superiority; no proof the remaining evidence-chain hypothesis is unique.

**Next unresolved action:** build the reproducible synthetic benchmark and buyer-value test, then compare against actual incumbent configurations only if lawful access and a bounded test environment are available.

**Safety boundary:** no production banking, supplier, payment, Cloudflare, DNS, secret, database, or outbound-email changes are authorized by this research record.
