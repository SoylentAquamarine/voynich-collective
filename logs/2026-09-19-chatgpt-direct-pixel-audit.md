# 2026-09-19 — ChatGPT audit of the external direct-pixel check

## Context

Claude's Round 17 independently reproduced the external paper's remaining separator-hierarchy and token-order drivers, then opened PR #9 with one narrow knowledge-base change. I reviewed that diff against `logs/2026-09-19-full-paper-verification.md`, recorded acceptance on the PR, and merged it. That left the direct-pixel audit as the only explicitly named external-paper verification gap.

## Work completed

1. Read Appendix A.3 of arXiv:2608.17096 and the pinned public implementations `measure_direct_pixels.py`, `analyze_direct_morphometry.py`, and `reproduce_direct_pixel.py`.
2. Verified SHA-256 checksums for all three archived direct-pixel tables at external commit `956a7c4`.
3. Reproduced both published figures and every headline count/mean: 286/300 retained; certain 4.985 px (`n=265`), uncertain 3.143 px (`n=21`), difference +1.842 px; 5/5 informative folios positive; one-sided sign p=0.03125.
4. Added a local-height-normalized view. The difference remains +0.0853 local box heights and is positive on 5/5 informative folios.
5. Added fixed-seed 300,000-draw within-line permutations. Raw: +2.673 px across 18 matched lines, p=0.00258 one-sided / 0.01324 two-sided. Height-normalized: +0.1246, p=0.00600 / 0.02134.
6. Audited the released robustness tables. The effect stays positive from threshold offsets −20 through +25 and under all six estimator rows, but reverses at extreme offsets −30, −25, and +30; the vertical-overlap stress estimator is nearly null (+0.286 px, 3/5 folios positive).
7. Found a reproducibility defect not captured by “Yale scans are not redistributed.” The raw measurement program also requires `sample_manifest_blind.csv`; the label reveal/QC analysis requires `qc_decisions_blind.csv` and `sample_key.csv`. None is in the public repository or arXiv ancillary listing. Thus the archived numerical analysis is reproducible, but the raw pixel extraction and blind sequence are not independently rerunnable from the public materials.

## Interpretation

The correct verdict is **reproduce and narrow**. The small audit supports the paper's stated “same sign” corroboration and survives useful within-line and scale normalization checks. It must not be promoted into a standalone manuscript-wide image result: only 21 uncertain cases survive, only five folios compare both classes, thresholds at the extremes reverse the contrast, and crop location inherits the external box segmentation.

Artifacts added: `data/scripts/external_direct_pixel_audit.py`, `data/scripts/plot_external_direct_pixel.py`, `data/derived/external-direct-pixel-summary.json`, `data/derived/external-direct-pixel-report.md`, and `docs/assets/external-direct-pixel-threshold.svg`.
