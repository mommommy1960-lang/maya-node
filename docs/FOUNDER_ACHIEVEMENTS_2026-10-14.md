# Mya P. Brown — achievements, learning and project evidence
Updated October 14, 2026. Founder, author and socio-technical systems accountability engineer.

## Start with the proof

- [Training completions and seven Kaggle badges — inspected source notes](FOUNDER_TRAINING_EVIDENCE_2026-10-14.md)
- [All 13 verified public repositories](PUBLIC_REPOSITORY_INDEX_2026-10-14.md)
- [School and banking customer pitches](https://civic-continuum-contact.freshcoin8.chatgpt.site/pitches.html)
- [Interactive school and banking demos](https://civic-continuum-contact.freshcoin8.chatgpt.site/demo.html)
- [Contact and digital business card](https://civic-continuum-contact.freshcoin8.chatgpt.site)

## Completed learning and activity

| Achievement | Evidence type | Click to inspect |
|---|---|---|
| Ethics of AI — MOOC.fi / University of Helsinki course | October 5, 2026 issuer completion notice; certificate access described; university credits separately unverified | [Source note](FOUNDER_TRAINING_EVIDENCE_2026-10-14.md#ethics-of-ai) |
| Introducing SAP Ariba Intake Management | October 3, 2026 issuer course-completion and badge notice | [Source note](FOUNDER_TRAINING_EVIDENCE_2026-10-14.md#sap-ariba-intake-management) |
| Introduction to Generative AI - Art of the Possible — AWS | March 12, 2026 course completion; not an AWS exam certification | [Source note](FOUNDER_TRAINING_EVIDENCE_2026-10-14.md#aws-generative-ai) |
| Google / Kaggle 5-day AI Agents Intensive | November 14, 2025 completion notice; capstone follow-up December 3; issued certificate not yet recovered | [Source note](FOUNDER_TRAINING_EVIDENCE_2026-10-14.md#google-and-kaggle-ai-agents-intensive) |
| Washington SBDC SOS program | October 9, 2026 adviser acknowledgment | [Source note](FOUNDER_TRAINING_EVIDENCE_2026-10-14.md#washington-sbdc-sos) |
| Seven Kaggle community/activity badges | Code Forker, Utility Scripter, Dataset Creator, Code Tagger, Python Coder, Vampire, Kaggle Community Member | [Badge list and dates](FOUNDER_TRAINING_EVIDENCE_2026-10-14.md#kaggle-community-and-activity-badges) |

These are accomplishments backed by the inspected completion/badge records. Links above open public evidence summaries, not the original certificate PDFs. Individual awarded certificate files and publicly verifiable badge URLs remain to be recovered; no certificate image has been fabricated. [Hugging Face source-recovery status](FOUNDER_TRAINING_EVIDENCE_2026-10-14.md#hugging-face-certificate-retrieval).

## Software milestones and reproducible results

| Work | Result and scope | Actual artifact |
|---|---|---|
| Accountability model and sandbox | 28 selected checks in the documented October 13 snapshot; 24 newly added checks reproduced October 14 | [Methods and results](ACCOUNTABILITY_PUBLIC_PROGRESS.md) · [Tests](../tests/integration/) |
| Separate seeded decision sweep | 2,256 expected labels matched, 1,128 school and 1,128 billing; synthetic model decisions | [Evaluation](ACCOUNTABILITY_EVALUATION_2026-10-13.md) · [Run code](../demos/evaluate_accountability.py) |
| Runnable accountability demonstrations | Code and tests merged October 14 via PR61; hosted integration run passed 1,113 tests on its proposed merge snapshot | [Merged PR61](https://github.com/mommommy1960-lang/maya-node/pull/61) · [Hosted run](https://github.com/mommommy1960-lang/maya-node/actions/runs/38482781796) |
| Durable dispatch queue and mocked mail adapters | 16 local Python checks passed; 16 Node test entries passed including the health-report test file. No real email sent in these tests | [Merged PR60](https://github.com/mommommy1960-lang/maya-node/pull/60) · [Queue guide](DISPATCH_QUEUE.md) · [Cloudflare test sources](../deploy/cloudflare/) |
| Repaired PR60 hosted validation | All 111 checks passed at commit 53b2ded5722dc749d96f78dd904a64d66bd0920f, including the 100-run validation matrix | [Exact checks](https://github.com/mommommy1960-lang/maya-node/commit/53b2ded5722dc749d96f78dd904a64d66bd0920f/checks) |
| Adversarial signature tests | 100 local cases passed after repairing two mutations that could accidentally leave a signature unchanged | [Tests](../tests/security/test_adaptive_redteam_100.py) |
| Public customer website | Contact Site version5 published with pitches, demos and reviewer routes | [Contact](https://civic-continuum-contact.freshcoin8.chatgpt.site) |

Counts refer to different suites/snapshots and are not added into one unique-test total. One hundred repeated CI runs are not one hundred independently designed experiments. A passing mocked or synthetic check establishes its specific behavior, not certification, physical validation or field reliability.

## Authorship and wider work

[Recovered Zenodo publication catalog](https://github.com/mommommy1960-lang/commons-sentience-sandbox/blob/main/docs/portfolio/zenodo/README.md) · [Public invention inventory](https://github.com/mommommy1960-lang/commons-sentience-sandbox/blob/main/docs/civic-continuum/portfolio/complete-invention-portfolio-inventory.md) · [Blue Book registry](https://github.com/mommommy1960-lang/commons-sentience-sandbox/blob/main/docs/civic-continuum/blue-books/civic-continuum-complete-invention-blue-book-registry.md).

These routes include governance papers, books, research records, curricula and invention concepts beyond the initial customer service. The inventories overlap and are not summed as a unique invention count. DOI publication is an authorship/provenance milestone, not a scientific award or peer-review finding.

## Corrections preserved

The publication work fixed a missing CERL header, shell examples mistakenly appended as executable Python, absent test-dependency installation and incomplete test discovery in the portfolio workflow. The signature-prefix/suffix tests previously wrote a fixed zero byte: sometimes the original byte was already zero. They now flip a bit so the tamper test actually changes the signature. Earlier failed runs remain visible. No test was removed or acceptance threshold relaxed. Email sending remains disabled in the published configuration under the outbound hold.

## Continuing gates

Registration, insurance, actual customer validation and live integrations remain open. Protected research implementation remains private; public summaries are linked from the repository index. No endorsement by Juan Garcia, Dr. Thomas Ainsworth, course providers or a regulator is claimed.
