# Execution: line-final 'm' type overlap vs controls matched on type frequency x final share

Date: 2026-11-07 UTC (~06:50). Solo Claude. Precommitment: `logs/2026-11-07-line-final-m-share-matched-selfreview.md` (pushed as 608e992 before the script existed). Script `data/scripts/line_final_m_share_matched.py`; output `data/derived/line-final-m-share-matched-summary.json`. Seed 20261108, 2,000 draws. One addition not in the precommit: z is reported as NaN when the control SD is 0 (see caveat).

## Results (ZL3b / RF1b; tokens whose matching cell had a control pool; 57 / 84 of 634 / 629 dropped for empty cells)

| stratum | tx | kept | O_m | O_ctrl | S_m | S_ctrl | S z |
|---|---|---:|---:|---:|---:|---:|---:|
| all | ZL3b | 577 | 0.532 | 0.586 | 0.378 | 0.596 | -12.7 |
| all | RF1b | 545 | 0.448 | 0.491 | 0.255 | 0.507 | -13.8 |
| A | ZL3b | 135 | 0.467 | 0.467 | 0.354 | 0.338 | +0.4 |
| A | RF1b | 140 | 0.350 | 0.393 | 0.271 | 0.236 | +1.0 |
| B | ZL3b | 396 | 0.409 | 0.424 | 0.197 | 0.585 | -20.1 |
| B | RF1b | 418 | 0.402 | 0.488 | 0.164 | 0.555 | -20.3 |

Excluding frequency-bin-1 types (sensitivity check): O gaps -0.076 (ZL3b) and -0.069 (RF1b) pooled; stem S_m 0.50 / 0.39 vs control 0.78 / 0.71. Same direction. Full table incl. the 90-line NA stratum (not interpreted) in the JSON.

## Predictions vs outcome
1. **Partly failed.** |O gap| pooled: ZL3b 0.054 (just over the 0.05 line), RF1b 0.043 (inside). The gap shrank from about -0.12 to about -0.05, so matching final share removed more than half of it, but not clearly all. Excluding freq-1 types the gap is back to about -0.07.
2. **Held.** Stem availability is not higher than control; it is much LOWER pooled (z about -13) and in B (z about -20). In A it is slightly higher (+0.02 to +0.04) but z only 0.4-1.0, below the z>3 bar.
3. **Not triggered** as stated (gap did not stay < -0.08 with z < -5 in both), though the sensitivity gap approaches it; I regard the type-overlap result as inconclusive, not as evidence of a distinct vocabulary.

## What this does and does not show
- The new, not-implied finding is the stem result: even with position propensity and frequency held fixed, line-final m words have markedly fewer mid-line stems (minus the m) than comparable final words. The earlier stem test (z -2.8) was weak; with this control it is large. So the data give no support for the account "line-final m = ordinary word + removable m" in B; A is indeterminate.
- Caveat on z: the matched cells often contain few distinct control types, and O is type-level (all-or-nothing per type), so control draws vary little (O SD is 0 in several rows, hence NaN z). O z-values are therefore unreliable and should not be read; the O gaps themselves are descriptive. S z-values are less affected but are also inflated by thin pools. 
- Controls match two coarse variables only; word length, line length, section and scribe remain uncontrolled (m-words may be shorter or longer than matched controls, which alone affects stem availability). Dropped cells (9-13% of tokens) are a selection.
- Same investigator; exact-string types across two transcriptions with different conventions. No claim about abbreviation, morphology, language, reading or meaning.
