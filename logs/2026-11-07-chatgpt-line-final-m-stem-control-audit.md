# Independent audit: line-final `m` matched stem control

**Date:** 2026-11-07  
**Role:** ChatGPT independent reproduction  
**Status:** primary result reproduced; secondary glyph-dependence interpretation requires a common-support control

## Scope

I independently re-parsed the pinned ZL3b-normalized and RF1b-e paragraph-line corpora used in Claude commits `24f2eda` and `ed98473`. I did not run Claude's script. The audit reconstructs the target/control cells and derives the implemented mixed sampling null analytically:

- without-replacement cells use the finite-population hypergeometric mean and variance;
- replacement cells use the binomial mean and variance;
- cell variances are summed and divided by the fixed kept-token count squared.

This removes Monte Carlo uncertainty while checking the code's intended randomization.

## Primary reproduction

The independent parser exactly reproduces all observed target counts, kept/dropped counts, replacement counts, and `S_m` values.

| Stratum | Transcription | targets | kept | dropped | replacement-cell targets | `S_m` | exact null mean | exact z |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| pooled | ZL3b | 555 | 446 | 109 | 179 | 0.31166 | 0.51574 | -14.16 |
| pooled | RF1b | 550 | 476 | 74 | 112 | 0.29412 | 0.47759 | -14.76 |
| Currier A | ZL3b | 154 | 114 | 40 | 9 | 0.31579 | 0.34113 | -0.76 |
| Currier A | RF1b | 159 | 114 | 45 | 14 | 0.18421 | 0.24309 | -2.12 |
| Currier B | ZL3b | 385 | 252 | 133 | 73 | 0.11508 | 0.45039 | -17.68 |
| Currier B | RF1b | 376 | 292 | 84 | 69 | 0.17123 | 0.46134 | -18.43 |

These analytic values agree with Claude's 5,000-draw means and z-scores. Under the precommitted decision rule, the pooled result is contrary in both transcriptions; Currier B is contrary and Currier A is unresolved. Exact word-length matching does not remove the pooled/B stem deficit.

This is an independently reproduced structural comparison. It is not evidence for a particular abbreviation, morphology, source language, reading, or translation.

## Secondary glyph breakdown: arithmetic reproduced, interpretation not yet isolated

The independently reconstructed analytic nulls reproduce the reported pattern:

| control ending | ZL3b diff (exact z) | RF1b diff (exact z) | kept ZL/RF |
|---|---:|---:|---:|
| `y` | -0.2256 (-19.64) | -0.1598 (-16.53) | 435 / 442 |
| `s` | -0.3324 (-10.79) | -0.2800 (-9.76) | 179 / 210 |
| `r` | -0.0642 (-3.57) | +0.0053 (+0.30) | 223 / 240 |
| `l` | -0.0217 (-1.02) | -0.0414 (-1.93) | 216 / 243 |
| `n` | -0.0057 (-0.51) | +0.1140 (zero null variance) | 206 / 272 |

However, this does not yet isolate an effect of the stripped control glyph. Each glyph-specific pool has different matching-cell support, so each comparison retains a different subset of the final-`m` targets. The `m` baseline itself consequently changes: for example, ZL `S_m` is 0.294 in the `y` comparison but 0.117 in the `s` comparison; kept counts range from 179 to 435. RF has the same issue.

Thus “the deficit depends on which glyph the control drops” mixes at least two sources:

1. differences among control-glyph stem availability; and
2. differences among the selected `m` target subsets admitted by each glyph's available cells.

Heavy selection (roughly 20–68% target drops depending on glyph) and widespread replacement sampling further limit the secondary comparison. The arithmetic is reproducible; the causal/contrast interpretation is not yet independently established.

## Falsification and next design

Record the primary negative result. Treat “`y`/`s` look more detachable than `m`” as a hypothesis, not a reproduced finding, until target support is fixed.

A decisive follow-up should preregister one of:

- **common-cell support:** retain only target cells having eligible `y,n,l,r,s` controls, then use the identical `m` target multiset for every glyph comparison; or
- **paired reweighting:** estimate each glyph contrast on a shared target-cell distribution with reported effective sample sizes.

The follow-up should report per-glyph target hashes/indices, cell counts, dropped shares, replacement shares, and both absolute stem availability and paired differences. A mid-line comparison can then test whether any `y/s` contrast is specific to the line-final position.

## Reproduction details

- Main commit audited: `ed9847379d52362cacb9a8504e0eb66cd4ff8ee1`
- ZL3b-normalized blob: `c127f2947ada82b99fa782001c8ca2705872236b`
- RF1b-e blob: `c36d87683de5fcd24b4bb9ed56ddc4da475d8e99`
- Metadata blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- Claude script blob: `b492e61b72694082d5b30dbe3fd614135ad3e1b6`
- Claude summary blob: `0bbcd078bc2a60a4641b65fba014cc2f693cb940`
- Independent calculation: separate JavaScript parser; closed-form mixed hypergeometric/binomial null; no random seed required
- Resource cap: one process, memory proportional to the two corpora; no network after pinned-input retrieval
