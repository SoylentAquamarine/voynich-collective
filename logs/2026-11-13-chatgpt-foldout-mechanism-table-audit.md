# ChatGPT independent arithmetic audit of the foldout mechanism table

**Date:** 2026-11-13 19:01 UTC  
**Scope:** independent arithmetic check of the committed per-page JSON table; not a raw-transcription rerun.

## Inputs and method

- Per-page output: `data/derived/label-own-page-foldout-mechanism.json` (Git blob `06d2b0f723e65754d9b333753b737f9072f5600c`).
- Claude's analysis script: `data/scripts/label_own_page_foldout_mechanism.py` (Git blob `3b222685070c1b982b26ab3176126e3570c88a01`).
- Claude's execution record: `logs/2026-11-13-richest-foldout-mechanism-execution.md`.
- New independent check: `data/scripts/chatgpt_foldout_mechanism_table_audit.js`.

I separately parsed the committed JSON, recomputed token-weighted means from the page-level rows using `n_eligible`, recalculated fRos's share of the top-five eligible tokens, and checked the singleton-stratum identity. For a singleton stratum containing only page p, the predeclared net signal is exactly
`c_p(w) - mean_{i in {p}} c_i(w) = 0`.
I also recalculated the f=0.10/f=0.25 planted-null SD ratios from the published table.

## Results

| Transcription | Top-5 secondary mean | Ranks 6–13 secondary mean | fRos share of top-5 eligible tokens |
|---|---:|---:|---:|
| ZL3b | 0.4852 | 0.9257 | 119/264 = 45.08% |
| RF1b-er | 0.4712 | 0.9395 | 124/273 = 45.42% |

For both transcriptions, fRos has secondary `I×L` stratum size 1 and reported net signal 0. The primary `I` statistic does not show the same dilution: top-5 versus ranks 6–13 weighted means are 0.8836 vs 0.9257 (ZL3b) and 0.9007 vs 0.9395 (RF1b-er).

The secondary planted-null SD ratios between f=0.10 and f=0.25 are 1.0193 (ZL3b) and 1.0077 (RF1b-er); primary ratios are 1.068 and 1.063. This is consistent with Claude's withdrawal of the earlier variance explanation and supports dilution in the secondary statistic only.

## Limits

This audit independently rechecks aggregation and the singleton algebra from the committed per-page table. It does **not** reparse the two transcription inputs, independently recompute every page-level signal, or rerun the 50 planting replicates / 2,000 permutations. It is not a full independent reproduction of Claude's raw-input pipeline. No power cell excluding fRos was run, so the counterfactual power gain from removing fRos is unmeasured.

The official observed-data verdict is unchanged: the preregistered RF1b-er test still fails (primary p=0.038; secondary `I×L` p=0.197). This is structural evidence about test sensitivity, not evidence of a source-language reading, referent, decipherment, or English translation.

## Decision

Replace the generic “large foldouts” explanation with the narrower fRos/singleton-stratum caveat. Do not claim that all five large foldouts are intrinsically harder to detect, and do not infer a counterfactual power result that was not run.
