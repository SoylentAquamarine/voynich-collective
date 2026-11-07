# Self-review (precommitment): line-final m type overlap with controls matched on type frequency AND final share

Date: 2026-11-07 UTC (scheduled cycle, ~06:45 UTC). Solo Claude. Written and pushed BEFORE any code for this test exists or runs. No network; committed transcriptions only.
Origin: ChatGPT 2026-11-07 04:00 UTC handoff ("preregister a final-share/position-matched control and proceed without waiting") and my own proposed next step of the 03:45 round. PR #101 (ChatGPT's independent audit) is Director-gated; I do not merge it.

## What is known
- Line-final 'm' enrichment 17-18x vs within-line shuffle null (b4de0ae). Type overlap of final-m words with mid-line types is LOWER than frequency-matched finals (O 0.52-0.57 vs 0.64-0.70), but that control was not matched on final-position propensity, so the result is largely implied by the position effect (disclosed in dcb3869; ChatGPT agrees).

## What is not done
- Whether, once a type's tendency to end lines is held fixed, final-m types still differ in mid-line overlap or stem availability.

## Design (non-circular)
Same loci, parser, tokenisation, strata and seed convention as `data/scripts/line_final_m_type_overlap.py` (import its loaders by copy). Per transcription and stratum:
- Type final share f(w) = (#line-final tokens of type w) / (#all tokens of type w), computed on the same loci set. Fixed bins now: f <= 0.25, 0.25-0.5, 0.5-0.75, > 0.75. Frequency bins unchanged (1, 2, 3-4, 5-8, 9-16, 17-32, 33+).
- Control for each line-final m token: a line-final non-m token drawn from the pool with the same (frequency bin, final-share bin) cell. With replacement (pool sizes are small; stated now, not post hoc). If a cell has no non-m pool, the token is dropped from both arms and the number dropped is reported.
- Statistics O (exact type occurs mid-line) and S (stem, length >= 3, occurs mid-line) exactly as before; 2,000 draws, seed 20261108; z against control draws.
- Caveat built in: f includes the token itself, so a type seen once and final has f = 1 by construction; frequency-bin 1 cells therefore sit in the top share bin for both arms and compare like with like. Also report the result excluding frequency-bin 1 as a sensitivity check (stated now).
- Report ZL3b and RF1b, all / Currier A / Currier B. Strata < 300 lines reported, not interpreted.

## Predictions (stated before running)
1. Under matching on both, the O gap shrinks sharply: |O_m - O_ctrl| < 0.05 in 'all' for both transcriptions (confidence ~60%; the earlier gap of -0.12 was probably mostly position propensity).
2. S (stem test): still not higher than control by z > 3 pooled (confidence ~70%); A/B sign split may persist.
3. If instead the O gap remains < -0.08 with z < -5 in both, then final-m types are more end-restricted than their final share explains, a genuine type-level distinctiveness. I do not expect this (~25%).

## Honesty precommitment
All cells reported whatever they show, including predictions failing, dropped tokens, and transcription disagreement. Same investigator as the prior steps; matched on only two coarse variables, so residual confounds (e.g. line length, section, word length) remain and no claim about abbreviation, morphology, language or reading is made. Script and JSON committed.
