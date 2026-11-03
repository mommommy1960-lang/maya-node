# Whole Story Challenge — Competitive Benchmark Protocol

**Date:** 2026-11-03  
**Status:** Research baseline and proposed test protocol; not a completed benchmark  
**Owner:** Civic Continuum  
**Purpose:** Test whether Civic Continuum adds measurable value beyond existing operational systems and credible commercial alternatives.

## 1. The rule: compare evidence, not marketing

Civic Continuum will not claim it is better, more accurate, cheaper, or more profitable than another product until a fair, reproducible test supports that statement.

This document separates three kinds of information:

1. **Published capability:** what a vendor publicly says its product does.
2. **Observed test result:** what the product actually does when given the same authorized evidence, configuration time, and ground truth.
3. **Unverified question:** what we still need to test or obtain from the vendor.

Vendor product pages are useful for identifying credible alternatives. They are not independent proof of performance.

## 2. Credible alternatives identified

The first market is warehouse, fulfillment, and logistics. The alternatives are not all direct substitutes; they occupy overlapping layers of the customer's current stack.

| Alternative | Category | Publicly documented overlap | What must be tested; not assumed |
|---|---|---|---|
| **Existing WMS + carrier portal + support/finance systems + manual review** | Customer's status quo | The systems already record warehouse events, shipment scans, complaints, and credits/refunds. A trained analyst can reconcile exports manually. | How accurately and quickly the current team can reconstruct the same five-order story; analyst time; missing findings; false positives; repeatability. |
| **Celonis Platform** | Enterprise process intelligence | Celonis describes extracting data from multiple systems, a system-agnostic Context Model, process analysis, root-cause analysis, predictions, recommendations, simulations, and ongoing monitoring. | Can it ingest these four source files with reasonable mapping effort, surface the three ground-truth cases, show source-level evidence, and distinguish associated credits from proven causation? |
| **SAP Signavio Process Intelligence** | Process mining and transformation | SAP describes analysis across SAP and non-SAP systems, event-log reconstruction, process deviations, root-cause analysis, improvement recommendations, and value tracking. | Same frozen dataset, ground truth, configuration effort, evidence traceability, exception precision/recall, and financial-causation discipline. |
| **UiPath Process Mining** | Process mining and automation | UiPath describes connecting to business applications, discovering end-to-end processes, identifying bottlenecks and discrepancies, monitoring KPIs, and linking insights to automation. | Can the product model the cross-system order journey from these records and reproduce the independent reference without excessive custom work? |
| **Microsoft Power Automate Process Mining** | Process and task mining | Microsoft documents process discovery from event-log files, process maps and metrics, finding mistakes, comparing processes, and understanding where problems occur. | Whether its import, transformation, and analysis workflow handles the same data and exposes the same source-backed discrepancies; total setup and analyst time. |
| **Salesforce Apromore** | Process intelligence / mining | Apromore documents event-log ingestion, process discovery, filtering, conformance checking, root-cause analysis, simulation, predictive monitoring, and data pipelines. Salesforce describes cross-system process visibility and continuous monitoring. | Can the same event evidence be modeled and tested against ground truth? Compare usability, effort, findings, and reproducibility. |
| **project44** | Supply-chain visibility and transportation intelligence | project44 describes carrier/facility connectivity, shipment and SKU visibility, predictive ETAs, exception management, data-quality diagnostics, analytics, and integration into existing TMS/ERP workflows. | Which evidence is available for this parcel/warehouse scenario, whether it can use the customer's own WMS/support/finance records, and whether it identifies post-event financial consequences. Do not assume it is a general-purpose audit platform. |
| **FourKites** | Supply-chain control tower and visibility | FourKites describes connected order, shipment, inventory, and facility data, digital twins, exception workflows, and AI-supported orchestration. | Whether it can independently reconcile the customer's own support and finance records against WMS/carrier events, and how findings are evidenced and scored. |
| **Blue Yonder** | WMS and end-to-end supply-chain execution | Blue Yonder describes warehouse operations, real-time orchestration, returns, labor, yard and transportation capabilities, and analytics across digital touchpoints. | Compare the customer's native operational view and analytics with the same frozen evidence. Determine whether cross-vendor records and independent financial consequence analysis require additional integration. |
| **Manhattan Active WM** | Warehouse management | Manhattan describes inbound-to-outbound inventory visibility, facility performance, actionable insights, and real-time resource/task visibility. | Can its native records and analytics explain discrepancies outside the warehouse boundary, including carrier, support, and finance records? Test rather than infer. |

### Public source register

Sources checked 2026-11-03. These are vendor-published descriptions and should be treated as claims to investigate, not independent proof.

- Celonis Platform: https://www.celonis.com/platform
- SAP Signavio Process Intelligence: https://www.signavio.com/products/process-intelligence/
- UiPath Process Mining: https://www.uipath.com/product/process-mining
- Microsoft Power Automate process mining overview: https://learn.microsoft.com/en-us/power-automate/process-advisor-overview
- Apromore product overview: https://apromore.com/product
- Salesforce overview of Apromore (published 2026-10-26): https://help.salesforce.com/s/articleView?id=005317703&language=en_US&type=1
- project44 Visibility: https://www.project44.com/Platform/Visibility/
- FourKites platform: https://www.fourkites.ai/platform
- Blue Yonder Warehouse Management: https://blueyonder.com/solutions/warehouse-management
- Manhattan Active Warehouse Management: https://www.manh.com/solutions/supply-chain-management-software/warehouse-management

Amazon note: Amazon's internal fulfillment and warehouse technology is not a publicly accessible software product that Civic Continuum can independently install and benchmark. Amazon may be an operator, logistics provider, or customer environment depending on the use case, but claims about its private internal systems require authorized access and a defined test. We will not invent or infer their internal capabilities.

## 3. What the first synthetic case can and cannot test

The current Whole Story Challenge contains five fictional orders and four record sets:

- WMS: 5 rows
- Carrier: 4 rows
- Customer support: 3 rows
- Finance: 3 rows
- Independent ground truth: 5 order classifications

Expected ground-truth findings are ORD-100, ORD-101, and ORD-102. ORD-103 and ORD-104 are non-exception controls under the five-minute timestamp tolerance.

This is a useful smoke test for import, joining, timestamp comparison, missing-record handling, evidence traceability, and uncertainty labeling. It is **too small** to establish general accuracy, scalability, predictive performance, real-world financial recovery, or superiority over enterprise software.

The current $137.00 is the sum of documented refunds/credits associated with flagged order IDs. The dataset establishes no causal amount and no recovered value.

## 4. Fair test design

### A. Freeze one common evidence package

For every participant, including Civic Continuum:

- use the same source files, field definitions, timezone declarations, and data dictionary;
- preserve the original files and record cryptographic hashes;
- document missing rows and known limitations;
- provide the same written business question and the same independent ground truth;
- do not let any participant see the answer key before submitting its results.

Use a larger, separately prepared dataset for the real benchmark. Keep the current five-order case as a public teaching example only.

### B. Use two baselines

1. **Current-state baseline:** the operator's existing WMS/carrier/support/finance workflow and a trained analyst following the operator's normal procedure.
2. **Commercial-tool baseline:** at least one credible process-mining platform and one logistics-visibility or WMS platform selected with the pilot operator.

Civic Continuum receives the same evidence and equivalent time for configuration. Any extra custom engineering or manual analyst intervention must be recorded for every participant, including ours.

### C. Pre-register the scorecard

| Measure | Definition |
|---|---|
| Material finding recall | Ground-truth material findings correctly identified / all ground-truth material findings |
| Finding precision | Correct material findings / all findings reported |
| False-positive rate | Non-findings incorrectly presented as material exceptions |
| Unsupported-claim rate | Conclusions stated more strongly than the source evidence permits |
| Evidence traceability | Findings with source IDs and reproducible supporting calculations |
| Ground-truth agreement | Agreement with the independent reference, including uncertainty labels |
| Setup effort | Analyst and engineer hours, connectors, mappings, and custom code |
| Time to defensible result | Elapsed time from receipt of frozen evidence to review-ready report |
| Reproducibility | Independent reviewer can reproduce the same result from the same evidence and rules |
| Financial accuracy | Correctly classified documented transactions, with causation and uncertainty kept separate |
| Total cost | License, implementation, integration, compute, and labor cost for the tested scope |
| Customer value | Verified improvement after intervention, measured against a pre-agreed baseline |

No single score should hide trade-offs. Report raw counts, denominators, configuration details, and confidence/limitations.

### D. Protect test integrity

- Select a neutral ground-truth reviewer before the test.
- Publish the test plan and scoring rules before results are known.
- Use synthetic data first; use customer records only with written authorization and appropriate privacy/security terms.
- Give vendors a fair opportunity to configure their product within the same declared limits.
- Record version, license tier, enabled modules, connectors, configuration, and date.
- Separate vendor-assisted setup from self-service performance.
- Do not exclude difficult cases after seeing results.
- Have a second reviewer reproduce the scoring.
- Obtain permission before publishing any vendor or customer-specific result.

## 5. Immediate benchmark sequence

1. Keep the current synthetic challenge as a transparent demo and smoke test.
2. Expand the synthetic dataset to a meaningful, independently labeled set with normal cases, edge cases, duplicate events, clock skew, missing events, late-arriving scans, reversals, and ambiguous causation.
3. Ask a willing warehouse/fulfillment operator which WMS, carrier, support, and finance products they actually use.
4. Select one process-mining competitor and one logistics/WMS competitor relevant to that operator's stack.
5. Ask for trial, evaluation, or documented import requirements; do not imply access or cooperation that has not been granted.
6. Run the pre-registered blind comparison and publish the full scorecard, including cases where Civic Continuum loses.
7. Only then decide whether the differentiator is real, needs narrowing, or is not supported.

## 6. Claims policy

Until a controlled comparison is complete, approved public wording is:

> Civic Continuum is developing an independent way to reconcile operational evidence across existing systems, identify material gaps and contradictions, and trace documented consequences. The Whole Story Challenge demonstrates the method on fictional data. We are testing whether this approach adds measurable value alongside the tools organizations already use.

Do not say that Civic Continuum is the world's first, beats Amazon, outperforms Celonis, guarantees recovery, finds hidden fraud, or produces a particular ROI unless a properly designed test establishes that exact claim.

## 7. Decision gate

Proceed with the market position only if the first authorized pilot shows a meaningful, repeatable advantage on a customer-valued measure—such as finding material exceptions missed by the current workflow, improving evidence traceability, reducing analyst effort, or verifying corrective value—at a total cost the customer will pay.

If the test does not show that advantage, revise the product or positioning. The goal is not to win a slogan contest; it is to produce independently verifiable customer value.
