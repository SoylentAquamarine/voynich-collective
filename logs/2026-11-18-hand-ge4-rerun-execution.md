# Execution: independent rerun of the Davis-hand >=4 split (precommit: 2026-11-18-hand-ge4-rerun-selfreview.md, pushed first)
`python3 -I data/scripts/d_ge4_hand.py`, unchanged, in a separate session (numpy 2.5.3; ~48 s). Input SHA-256 pins passed.
## Result
- Regenerated `data/derived/d-ge4-hand.json` is **byte-identical** to the committed file from `d200adf` (sha256 `344064b5941c55370c7987ac98b6610a2dca7dfa85be1eb0948b575e4f363b79` before and after; `git diff` empty). Prediction TRUE.
- All 20 cells reproduce exactly, including the threshold cell RF1b-er|eva|hand 2: ratio 1.236, p = 25/2001 = .01249 (24 null reps >= observed). One more exceedance would flip it to "not replicated" (26/2001 = .01299 > .0125). That cell should therefore be read as **marginal**, not as a clean pass; the precommitted rule is unchanged and it still formally passes.
## Scope
Reproduction only (same seed, same data); it shows determinism across environments, not robustness to seed. No new statistic, no promotion. Post-hoc >=4 cut, hand/language/section confound, same manuscript: all caveats from `logs/2026-11-18-hand-ge4-execution.md` stand. No reading/translation/ZL3a claim; J11 untouched; no network.
