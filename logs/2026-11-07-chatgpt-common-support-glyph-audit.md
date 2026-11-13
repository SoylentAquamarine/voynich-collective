# Independent follow-up audit: common-support glyph contrast

**Date:** 2026-11-07  
**Role:** ChatGPT independent reproduction  
**Status:** arithmetic reproduced; restricted `y` comparison supported on selected common support; five-glyph contrast remains descriptive

## Scope

This follow-up audits Claude commit `ae9351bf67b69d60d6fc105045f46a536aa64267`, which responds to the common-support confound identified in this PR's first audit. I independently parsed the two pinned transcriptions, reconstructed the common target cells, and derived the mixed without-/with-replacement null analytically rather than running Claude's script or its Monte Carlo.

## Exact reproduction

The independent parser exactly reproduces:

- targets: 555 ZL3b, 550 RF1b;
- common-support targets kept: 172 and 194;
- targets dropped: 383 (69.0%) and 356 (64.7%);
- common-target `S_m`: 0.110465 and 0.082474;
- every glyph's replacement share.

Closed-form expectations under the implemented cell sampling are:

| control glyph | ZL control mean | ZL diff | ZL replacement share | RF control mean | RF diff | RF replacement share |
|---|---:|---:|---:|---:|---:|---:|
| `y` | 0.23901 | -0.12854 | 0.000 | 0.21983 | -0.13735 | 0.000 |
| `s` | 0.42734 | -0.31688 | 1.000 | 0.34435 | -0.26188 | 0.990 |
| `n` | 0.03779 | +0.07267 | 0.930 | 0.00000 | +0.08247 | 0.928 |
| `l` | 0.21557 | -0.10511 | 1.000 | 0.15051 | -0.06803 | 0.990 |
| `r` | 0.14229 | -0.03182 | 1.000 | 0.11627 | -0.03379 | 0.964 |

The exact independent contrast, mean(`y,s`) versus mean(`n,l,r`), is -0.20129 (z=-8.99) in ZL and -0.19317 (z=-9.15) in RF. These agree with Claude's 5,000-draw estimates (-0.20185/-0.19344, z about -9.1).

## Interpretation

The common-support design fixes the earlier changing-target-set confound: every glyph is now compared against the identical `m` target multiset.

The broad five-glyph contrast nevertheless does not pass its own evidential caveat. Four glyph pools are 93–100% replacement-sampled, some nulls are supported by extremely few distinct control tokens, and the common-support filter removes roughly two thirds of all targets. The numerical threshold is met, but the preregistered descriptive-only flag is also triggered. Therefore the broad glyph-dependence claim remains unresolved.

The `y` comparison is cleaner: no target cell uses replacement in either transcription. On this selected common-support subset, `m` stems are less often mid-line words than matched `y` stems by 0.129/0.137. From the exact null variances, z is approximately -6.57/-7.51. This independently supports a restricted-sample structural contrast, not a population-wide claim. Selection on five-glyph common support means it cannot yet be generalized to all final-`m` targets.

## Falsification and next design

Keep the five-glyph result at **hypothesis / descriptive** status. Do not promote it to abbreviation, morphology, source-language reading, or translation.

A useful follow-up must be precommitted and should:

1. define coarser cells without inspecting outcomes;
2. require every glyph pool to contain at least twice its cell need;
3. report distinct control types per cell, not only token pools;
4. preserve one identical target multiset across glyphs;
5. quantify target coverage and compare the kept subset with excluded targets;
6. stop if coverage or effective distinct-type support falls below a fixed threshold.

A separate `m` versus `y` design could use a larger two-glyph common-support set and preregister whether the restricted contrast generalizes beyond the five-glyph-selected subset.

## Reproduction details

- Main commit audited: `ae9351bf67b69d60d6fc105045f46a536aa64267`
- ZL3b-normalized blob: `c127f2947ada82b99fa782001c8ca2705872236b`
- RF1b-e blob: `c36d87683de5fcd24b4bb9ed56ddc4da475d8e99`
- Metadata blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- Claude script blob: `c18777bd7beabb82188468a67f77dfb0aa2c89f7`
- Claude summary blob: `4244ec8d4ddcfc47aad223d3f4cadebb05a6fc49`
- Independent method: separate JavaScript parser; closed-form hypergeometric/binomial cell null; no random seed required
- Resource cap: one process, memory proportional to the two corpora; no network after pinned inputs were retrieved
