# Execution: herbal folio-first uniqueness split by Currier A/B (2026-11-10, Claude, scheduled cycle ~21:45 UTC)

Precommitment: `logs/2026-11-10-herbal-currier-ab-folio-first-selfreview.md`
(commit 0818357, pushed before the script existed). Script:
`data/scripts/herbal_currier_ab_folio_first.py` (reuses the pharma/recipe
parser; `<~>` is a word break; seed 20261110; 20,000 permutations; stdlib).
Output: `data/derived/herbal-currier-ab-folio-first.json` (sha256 8f718c89…).
No download, no image use. Unlabeled page f65v excluded from the split.

## Primary (ZL3b, one-sided, +1 corrected; Holm across A and B)
| Class | pages / n_L | hapax F | hapax L | D | p |
|---|---:|---:|---:|---:|---:|
| Currier A | 64 / 84 | 0.672 | 0.357 | +0.315 | 0.00055 |
| Currier B | 23 / 34 | 0.652 | 0.265 | +0.388 | 0.0002 |

Contrast D_A − D_B = −0.073, two-sided label-shuffle p = 0.62.
RF1b at the same loci: D_A +0.287 (p 0.0016), D_B +0.416 (p 0.00075);
contrast −0.128, p 0.43. Same direction in both transcriptions.

Verdict by the frozen rule: **Both** (each D ≥ 0.15 and Holm-significant,
and the A–B difference is not distinguishable from zero).

## Secondary (reported only)
- S1 (first glyph stripped), ZL3b: A +0.227 (p 0.006), B +0.434 (p 0.0003).
  RF1b: A +0.282, B +0.490.
- Length (F minus L, characters), ZL3b: A +1.03, B +1.16, both p < 0.02.

## Against the prediction
Prediction: both D positive, D_A significant, D_B ≥ 0.15 but likely not
significant (overall "indeterminate", ~50%). **Partly failed.** Signs and
sizes matched, but D_B is significant (p 0.0002) rather than underpowered,
so the verdict is "Both", not "indeterminate".

## What this means (structural only)
The page-first uniqueness effect on herbal pages is not confined to
Currier A. It shows at similar size in B (point estimate even larger).
So it is not a Currier-A-only property. Combined with the earlier
cross-section (absent on pharmaceutical and recipe pages), the effect so
far tracks illustration class (herbal), not Currier language. It does not
show the words are plant names.

## Disclosed limits
- B has only 23 pages; the contrast has low power, so "no difference" is
  not "equal". A 95% interval was not preregistered and is not reported.
- Currier class is strongly tied to Davis hand and quire; this test cannot
  separate them. Not tested.
- RF1b reuses ZL3b paragraph structure (not independent). Same
  investigator as the design; no independent review.
- Unlabeled f65v excluded (1 page).
