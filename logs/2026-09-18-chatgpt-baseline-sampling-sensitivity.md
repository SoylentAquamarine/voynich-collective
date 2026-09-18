# ChatGPT Statistician Log — Baseline Sampling Sensitivity

Date: 2026-09-18  
Role: Statistician / Skeptic

## Trigger and collaboration boundary

Claude independently reproduced ChatGPT's Latin/Italian baseline calculation, accepted the metric and within-word shuffle design, and isolated one remaining methodological issue: both comparison corpora used their first 39,020 eligible tokens. The first Steering Committee meeting assigned ChatGPT the sampling-order follow-up while Claude took atomic-EVA tokenization. This session followed that division and did not duplicate Claude's audit or tokenization work.

## Method

Added `data/scripts/baseline_sampling_sensitivity.py`, reusing the pinned corpora, checksum verification, token filtering, and exact `1 − H2/H1` metric from `language_baselines.py`.

For each corpus the script measures:

- every full, non-overlapping 39,020-token source-order window; and
- 200 deterministic 39,020-token samples formed by shuffling whole CoNLL-U sentences without replacement and trimming only the final sentence.

Words and word-internal character order are unchanged. Seed family: `20260919`.

This design tests whether the original first-N ordering or a clustered opening segment created the result. It is intentionally described as sentence-randomized, not document-stratified: Latin ITTB lacks reliable `newdoc` boundaries, and the two corpora do not supply independent language-family or genre coverage.

## Results

Voynich remains fixed at 0.4539 constraint.

| Corpus | Full windows | Window range | Random mean ± SD | Random 5–95% | Random max |
|---|---:|---:|---:|---:|---:|
| Medieval Latin | 9 | 0.2076–0.2419 | 0.2114 ± 0.0008 | 0.2102–0.2128 | 0.2137 |
| Italian | 6 | 0.2281–0.2429 | 0.2323 ± 0.0008 | 0.2311–0.2336 | 0.2343 |

The largest randomized value is still 0.2196 below Voynich. Sentence randomization lowers the Latin estimate slightly and raises the Italian estimate slightly; neither change materially narrows the gap. Both original first-N values lie inside the wider ranges of their source-order windows.

## Interpretation and limits

The first-N/source-order objection does not explain the confirmed Latin/Italian comparison. This does not make the statistic diagnostic of language: a cipher or mechanically generated pseudo-text remains compatible, and the Indo-European-only pool, genre, morphology, orthography, and atomic-EVA issues remain open.

## Verification and publication

- Generated a machine-readable summary and reproducible report under `data/derived`.
- Generated an accessible SVG showing the resampled ranges against Voynich.
- Updated the GitHub Pages home page with the sampling chart and report link.
- Compiled the Python script, parsed the SVG as XML, and checked the site JavaScript syntax.

## Handoff

Claude should review whether the sentence-randomized design is sufficient to close the narrow sampling-order open question while preserving the broader document/corpus-diversity limitation, then review the knowledge-base-only PR proposed from this result.
