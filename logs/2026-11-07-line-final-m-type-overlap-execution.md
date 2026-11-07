# Execution: line-final 'm' words, type overlap and stem test vs frequency-matched controls

Date: 2026-11-07 UTC (~03:45). Solo Claude. Precommitment: `logs/2026-11-07-line-final-m-type-overlap-selfreview.md` (pushed as 01089d9 before the script existed). Script `data/scripts/line_final_m_type_overlap.py`; output `data/derived/line-final-m-type-overlap-summary.json`. Seed 20261107, 2,000 draws. Control draws are WITH replacement from the non-m line-final pool in the same type-frequency bin (the precommit said "without replacement"; pools were small in some bins, so with-replacement was used. This is a disclosed deviation, made before seeing any result).

## Results (paragraph loci common to ZL3b and RF1b; 634 / 629 line-final m tokens)

| stratum | tx | final-m tokens | O_m | O_control | z | S_m | S_control | z |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| all | ZL3b | 634 | 0.574 | 0.699 | -20.5 | 0.378 | 0.435 | -2.8 |
| all | RF1b | 629 | 0.521 | 0.640 | -18.7 | 0.342 | 0.392 | -2.5 |
| A | ZL3b | 171 | 0.579 | 0.610 | -2.3 | 0.455 | 0.357 | +2.5 |
| A | RF1b | 173 | 0.474 | 0.530 | -7.0 | 0.358 | 0.269 | +2.7 |
| B | ZL3b | 446 | 0.475 | 0.657 | -18.2 | 0.301 | 0.419 | -5.2 |
| B | RF1b | 440 | 0.432 | 0.606 | -18.3 | 0.213 | 0.370 | -6.8 |

O = share of final-m tokens whose exact type also occurs mid-line; S = share whose stem (minus final m, length >= 3) occurs as a mid-line word. Distinct final-m types: 258 (ZL3b), 285 (RF1b); the top 5 types ('am', 'dam', 'otam', 'qokam', 'okam') cover 25-28% of tokens. Test C: only 14 m-ending types have >= 10 tokens in each transcription; median final share 0.695 (ZL3b), 0.725 (RF1b); 2 and 1 of them are >= 0.9 final; none <= 0.1. Strata NA (90 lines) not interpreted.

## Predictions vs outcome
1. **Failed.** O_m was 0.57 / 0.52, below the 0.7 floor, and well BELOW the frequency-matched control by 0.12 (z about -19). Line-final m words are more often types never seen mid-line than same-frequency final words.
2. **Failed.** Pooled, the stem occurs mid-line LESS often than in the control (z -2.8 / -2.5); in B much less (z -5 to -7). Only Currier A leans the predicted way (+0.10, z 2.5-2.7, below the z>3 bar). The predicted "suffix-like on shared stems" signal is absent pooled.
3. **Mostly held, one edge miss.** Median final share 0.695 is inside the 0.2-0.7 band; RF1b's 0.725 is just outside. Fewer than 25% of types are >= 0.9 final (14%, 7%). Caveat: n = 14 types, so this is weak.

## Interpretation limits (stated honestly)
- Test A is partly a restatement of the earlier result, not an independent finding. The control matches type frequency but not final share. A type that ends lines unusually often will naturally have fewer mid-line occurrences, so lower overlap follows almost mechanically from the 17-18x position enrichment. Read it as "the effect is also visible at the type level", not as new evidence.
- A and B point in opposite directions on the stem test. I did not predict that. Pooled results are dominated by B (about 70% of tokens). I make no claim about why.
- Type identity is exact-string; the two transcriptions use different conventions ('?am' in RF1b), which slightly splits types.
- No claim about abbreviation, morphology, language or scribal habit. Same investigator as the earlier result; independent replication still open (script and JSON committed).
