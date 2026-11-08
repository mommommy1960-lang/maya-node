# BPI Challenge 2019 first-pass analyzer

This folder contains a standard-library, streaming XES analyzer. It does not bundle the source dataset.

## Source

Boudewijn van Dongen (2019), *BPI Challenge 2019*, 4TU.ResearchData:
- DOI: https://doi.org/10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1
- Dataset record: https://research.tue.nl/p/en/datasets/bpi-challenge-2019
- Original XES download: https://data.4tu.nl/file/35ed7122-966a-484e-a0e1-749b64e3366d/864493d1-3a58-47f6-ad6f-27f95f995828

Review the source record's current license and attribution requirements before redistributing source or derived data. Do not commit the 700+ MB source file to this repository.

## Run

```bash
python analyze_xes.py /path/to/BPI_Challenge_2019.xes --output bpi2019_analysis.json
python -m unittest -v
```

The analyzer streams one trace at a time and reports case/event counts, count comparison to published figures, item categories, activity frequencies, top ordered variants, timestamp coverage, cautious first-event interval diagnostics, and attribute-presence summaries.

## Important interpretation limits

- BPI 2019 is purchase-to-pay event evidence, not a four-feed WMS/carrier/support/finance package.
- The first-event interval calculations are diagnostics, not invoice-to-receipt matching.
- The dataset does not provide independent ground-truth dispositions for every case.
- Timezone-less timestamps are treated as unparseable; no local timezone is guessed.
- Event deviations are not automatically violations, losses, fraud, causation, or recoverable value.
- This analyzer is an initial structural pass, not the complete preregistered Whole Story scoring engine.
