# Post-hoc exact bifolium-cluster recheck of the herbal A/B contrast

**Date:** 2026-11-11 06:52 UTC  
**Status:** exploratory robustness audit, not a preregistered test. The statistic, cluster unit, conditioning rule, and two-sided tail rule were fixed in this analysis before the exact enumeration was run, but no durable precommitment was committed before code was written.

## Why this check

Claude's 2026-11-11 bifolium-position execution found that Currier language is constant within 44/44 usable conjugate pairs overall and 27/27 in herbal quires A-G; all 18/18 usable pairs in mixed quires D-G are concordant. That reproduces a known codicological observation. It means the earlier page-level A/B label shuffle treats the two leaves of a bifolium as exchangeable even though their labels are shared. Claude proposed a bifolium-cluster re-check as an optional sensitivity analysis.

## Pinned inputs

- Voynich source commit at audit time: `c4ed3ce2844a99ee48f44b446a04465ee2ea86e6`
- ZL3b Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- RF1b Git blob: `c36d87683de5fcd24b4bb9ed56ddc4da475d8e99`
- The committed Node script checks these Git blob IDs before analysis.
- The session reproduction used a separate JavaScript implementation in the analysis runtime. The committed Node script is a portable, reviewable restatement; it was not invoked with a local Node executable in this session.

## Method

1. Parse the pinned IVTFF files independently. Resolve `[a:b]` to the first alternative; treat `<->` and `<~>` as word breaks; strip remaining markup; split on periods and commas.
2. Take paragraph starts from ZL3b `<%>` loci on herbal (`$I=H`) pages. For each transcription, count corpus-wide word frequencies and flag whether each page's first paragraph-initial word is a hapax.
3. Retain pages with at least two non-empty paragraph starts, in mixed quires D-G, with Currier label A or B. Group eligible pages by `(Q,B)`, the bifolium identifier, and verify that every page within a group has the same Currier label.
4. Compute `D_A-D_B`, where each class's `D` is first-paragraph-start hapax rate minus later-paragraph-start hapax rate.
5. Enumerate every assignment of A/B labels to whole bifolium clusters within each quire, preserving that quire's observed number of A and B bifolia. Use the exact two-sided tail fraction; no Monte Carlo seed or +1 correction is needed.

The census is 43 eligible pages and 103 paragraph starts across 16 bifolium clusters (four per quire). The allowed assignments are (4\times6\times6\times4=576).

## Results

| Reading | Observed (D_A-D_B) | Extreme / total assignments | Exact two-sided p |
|---|---:|---:|---:|
| ZL3b | +0.0314 | 476 / 576 | **0.826389** |
| RF1b readings | -0.1109 | 262 / 576 | **0.454861** |

Per-quire cluster allocation: D = 3 A / 1 B bifolia; E = 2 / 2; F = 2 / 2; G = 3 / 1. The machine-readable output preserves the page-level cluster census and permutation ranges.

## Interpretation and limits

- This finds no clear A/B contrast under a whole-bifolium conditional randomization. It does **not** establish equivalence, independence, or that Currier class has no effect.
- Exchangeability of bifolia within each quire is still an assumption; there are only four clusters per quire, so the exact distribution is coarse and power is limited.
- The earlier within-class folio-first effects are not tested here and are not overturned.
- RF1b is not an independent segmentation: it reuses ZL3b paragraph-start locus IDs. The two readings are not independent transcriptions.
- This is structural evidence only. It identifies no heading, plant, source language, glyph value, decipherment, or English translation.

## Decision

Treat this as a sensitivity check, not a new promoted finding. Stop further same-corpus hand/quire subdivisions unless genuinely new codicological evidence or an independent transcription becomes available. Keep J11 in its existing Priority-1 laptop queue; no laptop execution is claimed.
