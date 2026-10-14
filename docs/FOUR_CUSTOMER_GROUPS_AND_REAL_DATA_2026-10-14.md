# Four customer groups, pitches and real public-data comparison
October 14, 2026. Buyer hypotheses for discovery, not four signed customers.

[Live pitches](https://civic-continuum-contact.freshcoin8.chatgpt.site/pitches.html) · [Four interactive workflow demos](https://civic-continuum-contact.freshcoin8.chatgpt.site/demo.html) · [Real-data results](https://civic-continuum-contact.freshcoin8.chatgpt.site/real-data.html).

## Customer groups and buying roles

| Group | First buying role to interview | Bounded problem | Discovery question |
|---|---|---|---|
| School database teams | Student-information / IT operations owner | Purpose-limited student information access | Who approves access changes and corrects an out-of-scope read? |
| Banking database teams | Data operations / AI governance / risk owner | Customer information and transaction-summary scope | What evidence must a vendor supply before a redacted workflow review? |
| Nonprofit donor/member operations | Operations director / fundraising CRM owner | Donor/member purpose, consent freshness and export limits | Where do volunteer, staff and AI permissions become unclear? |
| Customer-support teams | Support operations / platform owner | Customer-record access, escalation and correction review | Which AI-assisted support workflow has the clearest boundary and named reviewer? |

The added groups are recommendations inferred from their workflow fit. Official Salesforce documentation describes donor profiles and permission-set assignment; Zendesk documentation describes role-based record access and customer-data masking. These establish relevant permission needs, not willingness to pay or integration compatibility.
- https://help.salesforce.com/s/articleView?id=sfdo.fundraising_manage_donor_profiles.htm&language=en_US&type=5
- https://help.salesforce.com/s/articleView?id=sfdo.NPC_Nonprofit_Cloud_Permission_Sets.htm&language=en_US&type=5
- https://support.zendesk.com/hc/en-us/articles/6034260247066-Configuring-permissions-to-access-custom-object-records
- https://support.zendesk.com/hc/en-us/articles/7713908123674-About-data-masking-ADPP-add-on

## Four pitches

### School database teams
When AI reads or recommends a use of student information, can your team show which purpose was permitted, who authorized it and who owns correction? Civic Continuum's $25 human review examines one redacted workflow, maps authority and data boundaries, records one bounded adversarial test and returns a written review with next actions. The demo allows a limited attendance read and blocks excessive export and revoked access. No live school system or compliance certification is claimed.

### Banking database teams
When AI uses customer information, can your team show the permitted scope and who reviews a boundary failure? The $25 human review examines one redacted workflow and one bounded test. The demo allows a transaction-count summary and blocks bulk statement export or revoked access. This is not a bank software license, penetration test or regulatory approval.

### Nonprofit donor/member operations
When an AI assistant uses donor or member records, can your team show the permitted purpose, whether consent is current and who owns correction? The $25 human review maps one redacted workflow and one boundary test. The demo allows an aggregate contact-preference summary, blocks donor/member list export and blocks revoked access. It does not connect to a CRM or send fundraising messages.

### Customer-support teams
When AI helps with a customer request, can your team show which records it may read, what it may do and who reviews a failure? The $25 human review examines one redacted support workflow and one boundary test. The demo allows a ticket-count summary and blocks full customer-record export, with separate correction review. It does not issue refunds, message customers or connect to a support platform.

## Real data downloaded and evaluated

| Source | Observed sample | Selection and retained fields |
|---|---|---|
| IRS Washington exempt-organization Business Master File | 100 records selected from 42,812 downloaded rows | First 100 in source order; name, city, state, subsection, status, NTEE code. EIN and addresses omitted. |
| CFPB complaint database | 100 actual complaint records returned by a 2025 query | API source order, not representative; product, issue, response category, timely flag and received date. Narratives, ZIP, complaint IDs and consumer data omitted. |

IRS source: https://www.irs.gov/pub/irs-soi/eo_wa.csv . CFPB exact query: https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/?size=100&date_received_min=2025-01-01&date_received_max=2025-12-31 . CFPB selected received-date range: May 31–December 2, 2025 (UTC). These are observed records, not invented case descriptions.

[Published non-personal source sample](../data/public/source-records-2026-10-14.json) · [Exact result JSON and event records](../data/public/comparison-results-2026-10-14.json) · [Reproduction code](../demos/public_data_comparison.py).

### Observed summaries
IRS subsection code counts: 03=78; 04=8; 05=5; 06=5; 07=3; 08=1. Codes are retained as published and are not inferred donor-consent fields.
CFPB response categories: 91 closed with explanation; 3 closed with monetary relief; 3 closed with non-monetary relief; 3 untimely response. Closure categories are not evidence that an underlying complaint was fixed, and complaints are not verified findings or a representative market sample.

### Comparison with our software
Both 100-record samples had the required selected fields present. The allowed summary returned through the existing permission model exactly matched direct aggregation. An out-of-scope export and a revoked summary read were denied for each dataset: six comparison assertions passed.

The data is real; the operator grant, export restriction, revocation and response-owner labels are injected test conditions. The public records do not supply actual donor consent, live bank permissions, staff identity or a historical incident-response baseline. This test does not establish that our system prevented those original complaints. IRS registry records are not donor/member records. The CFPB corpus supports financial-service customer-response exploration and is not generalized as a random sample of all support industries.

Run from the repository root:
```sh
python -m demos.public_data_comparison data/public/source-records-2026-10-14.json
```
The browser illustrations remain fictional workflow examples, separately labeled. Twenty logic assertions passed across four sectors. Real public-source comparison remains a separate experiment with real records and specified test permissions.

## Next buyer validation
Ask Juan to help prioritize one buyer group. Interview the actual owner, test a redacted workflow with consent, agree evidence and acceptance criteria, and measure human review and delivery. No customer contact, subscription, production deployment or field reliability result was created by this report.
