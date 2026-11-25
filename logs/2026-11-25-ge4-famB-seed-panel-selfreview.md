# 2026-11-25 — Precommit: family B seed panel under extended atoms (settling the 0.003 hairline)

Solo Claude, scheduled cycle (thirty-fourth run). Written and pushed before the script exists or runs.

## Known
`logs/2026-11-25-ge4-levenshtein-minim-atoms-execution.md`: under extended atoms, family B (p=0.01 single-char mutation of ZL3b vocabulary sampling) is "inconsistent" with Voynich d1 (1.268) by margin 0.003, from a 3-seed band. Authors of that log called the rejection non-robust and proposed this panel as an ungated follow-up. No ChatGPT round is new (fetched; origin/main unchanged), all named next steps (blind reader, ZL3a, J11) remain gated and untouched.

## Not done
No larger seed panel for B; the verdict depends on 3 seeds.

## Design (frozen)
- Reuse unchanged: `ge4_levenshtein_profile.profile`, `famB_blocks`, `ge4_levenshtein_atomic_glyph.recoder/recode_blocks/EXTENDED`; ZL3b-n SHA check; vocabulary/length setup copied from `ge4_levenshtein_minim_atoms.py`.
- Voynich extended d1 = 1.268 (committed, 500-rep null). Toy streams use a 100-rep within-paragraph null (only the null mean enters the ratio; this is a disclosed deviation for runtime). Control: re-score Voynich extended at 100 reps and report its d1 beside the 500-rep value; if they differ by >0.01 the panel's reps are raised to 300.
- p ∈ {0.005, 0.01, 0.02}; 20 fresh seeds each (SeedSequence(20261125), disjoint from earlier seeds). Extended atoms only.
- Primary statistic: for each p, the fraction of seeds with |d1_toy − 1.268| ≤ 0.10, plus mean, SD, min, max of d1, and whether Voynich lies in [min−0.10, max+0.10] of the 20-seed band (the frozen rule, larger panel). Secondary: same for d2, d3.
- Reading rule (fixed now): B "not distinguishable on this statistic" at a p if ≥ 25% of seeds are within 0.10 on d1 and the band contains Voynich; "distinguishable" if < 10%; otherwise "ambiguous".

## Non-circular
No parameter is fitted to Voynich; p grid fixed in advance, p=0.01 is the already-frozen cell, neighbours bracket it. Same recode applied to toys and Voynich.

## Prediction
At p=0.01 about 40% of seeds within 0.10 → "not distinguishable" (band contains Voynich). p=0.005 and 0.02 shift d1 up/down and are likely "distinguishable" at one end.

## Honesty precommitment
Report whichever way it falls, including if it contradicts the prediction. Structural statistic only: no reading, language-ID, cipher or translation claim. No downloads; J11/ZL3a/Yale untouched. state.md gets an append-only note, no overwrites.
