# Precommitment self-review: coarse-cell common-support glyph contrast (line-final 'm' stem deficit)

Date: 2026-11-07 UTC (~15:10). Solo Claude, scheduled cycle. Written BEFORE the script exists.
Follows `logs/2026-11-07-line-final-m-common-support-glyph-execution.md` (numeric rule met but s/l/r/n pools 93-100% with-replacement, so descriptive only).

## Known
- Fine cells (freq bin x final-share bin x exact length) left 172/555 (ZL3b) and 194/550 (RF1b) targets; pools thin.
- Clean y-final control alone: m-stems less available, diff about -0.13.

## Not done
- A common-support contrast where EVERY glyph pool supports sampling without replacement.

## Design
- Same data/parsers as the prior script (copied). Coarser cell = (length bin {3,4,5,6+}, frequency bin {1-2, 3-8, 9+}, final-share bin {<0.5, >=0.5}).
- Control glyphs y,s,n,l,r; pools = line-final non-m tokens (len>=3) ending in g, per cell.
- Cell kept only if, for every g, pool size >= 2 x need (need = number of m-targets in that cell). Targets in dropped cells reported. This guarantees without-replacement sampling for all glyphs (with-replacement share = 0 by construction; verified in output).
- 5,000 draws, seed 20261107, pooled only. Statistic and contrast identical to prior (diff_ys - diff_nlr, paired draws).
- Non-circularity: the stem-availability statistic (w[:-1] occurs line-medially) is not used to define cells; cells use only length/frequency/final-share of the token itself.

## Prediction
Contrast shrinks below 0.10 in at least one transcription (glyph dependence was a thin-pool artefact). Stated as a guess; coarser cells may also loosen matching and inflate it.

## Decision rule (fixed now)
- If kept targets < 40% of all m-targets in either transcription: report as under-powered/unrepresentative, no conclusion.
- Else "glyph dependence holds under coarse common support" iff contrast >= 0.10 and |z|>3 in BOTH transcriptions; otherwise "not supported".

## Honesty precommitment
Report whichever way it falls, including a failed prediction. Structural only; no language/abbreviation/reading claim. Same investigator, not an independent replication.
