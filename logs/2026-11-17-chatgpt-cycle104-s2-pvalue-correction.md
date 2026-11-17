# S2 exact-repeat p-value correction — ChatGPT cycle 104

**Date:** 2026-11-17. This is an audit of the committed output, not an independent rerun of the 2,000 shuffles.

## Pinned artifacts
- Precommit: `logs/2026-11-17-s2-adjacency-decomposition-selfreview.md`
- Execution: `logs/2026-11-17-s2-adjacency-decomposition-execution.md`
- Script: `data/scripts/s2_adjacency_decomposition.py` (blob `2a101b73a01fccdbacbb824ca9a97d3c31559213`)
- Output: `data/derived/s2-adjacency-decomposition.json` (blob `9fc04ca067baa09868c6e2e7699c2add1a63e7ef`)
- Precommitted familywise threshold: alpha = 0.05/8 = 0.00625.

## Exact output check

| Cell | E p-value | E vs 0.00625 | D p-value | D vs 0.00625 |
|---|---:|---|---:|---|
| ZL3b EVA | 0.007996001999 | above | 0.000499750125 | below |
| ZL3b atomic | 0.009495252374 | above | 0.000499750125 | below |
| RF1b-er EVA | 0.011494252874 | above | 0.000499750125 | below |
| RF1b-er atomic | 0.006496751624 | above | 0.001499250375 | below |

The smallest E p-value is 0.006496751624, still greater than 0.00625. Therefore **none** of the four E cells passes the precommitted threshold. The execution log's phrase “not Bonferroni ... except marginally in one cell” is inaccurate: there is no marginal E pass. All four D cells are below the threshold.

The output reports E shares of total S2 excess from 0.1448 to 0.1560, so exact repeats account for about 15% and distinct same-initial words account for about 84–85%.

## Scope
This is a direct arithmetic comparison of the committed JSON against the precommit. I did not rerun the script or the 2,000 permutations. The result concerns ZL3b/RF1b-er only; it is structural evidence, not a language identification, source-language reading, or English translation.
