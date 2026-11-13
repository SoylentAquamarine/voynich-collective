# Execution: richest-foldout power-drop mechanism check

Precommit: `logs/2026-11-13-richest-foldout-mechanism-selfreview.md` (commit 205d209, pushed before any code).
Script: `data/scripts/label_own_page_foldout_mechanism.py` (~2 s). Output: `data/derived/label-own-page-foldout-mechanism.json`
(sha256 af48bcaf…bad89, byte-stable over two runs). Post-hoc, structural, non-confirmatory.

## Result

Net signal per planted hit, s = c_p(w) − mean over the stratum of c_i(w), token-weighted:

| test | set | ZL3b | RF1b-er |
|---|---|---|---|
| primary $I | top 5 | 0.884 | 0.901 |
| primary $I | ranks 6–13 | 0.926 | 0.940 |
| secondary $I×$L | top 5 | **0.485** | **0.471** |
| secondary $I×$L | ranks 6–13 | 0.926 | 0.940 |

Null SD with planting (mean of 50 reproduced plantings), top-5 cell ÷ top-13 cell: primary 1.068 (ZL3b) / 1.063 (RF1b-er); secondary 1.019 / 1.008.

Increment in z from the ~11.8 planted hits, 11.8·s/SD. (The precommit called this "approx z". It is the *increment* over the baseline excess, not the total.)
- Secondary: 1.22 → 0.85 (ZL3b) and 1.29 → 0.89 (RF1b-er).
- Primary: 0.87 → 0.80 and 0.89 → 0.82.

**The cause is one page.** fRos is the only page in its $I×$L stratum (stratum size 1), so a hit planted on fRos raises the observed and null totals equally, and its net secondary signal is exactly 0. fRos holds 119/264 (ZL3b) and 124/273 (RF1b-er) of the top-5 eligible tokens, so about 45% of the top-5 dose is invisible to the secondary test. The other four foldouts (f67r2, f72r3, f69r, f72v3) have ordinary net signal (0.81–0.98).

## Against the precommitted rule

- **H-var** (my earlier "big foldouts vary most" explanation): **not supported.** SD ratios between the cells are 1.01–1.07, below the 10% threshold.
- **H-dil / small-stratum: supported**, through the secondary test only. The ratio is 0.52 / 0.50 (≤ 0.8), and the SDs are within 10%. In the primary test the ratio is 0.95, so there is no dilution there.
- **Prediction (H-dil, not H-var): held.** One sub-claim failed. I said planting "barely moves" the null SD, but it raises the primary SD by 11–20% over baseline. That rise is similar in both cells, so it does not explain the gap.

## Consequences (disclosed)

- **Withdrawn:** the variance explanation in `logs/2026-11-13-label-own-page-richest-matched-dose-execution.md` line 18. A correction is appended to state.md.
- **Card wording.** "Less sensitive to anchoring confined to the five largest label-rich foldouts" describes the right page set for the wrong reason. A more accurate version: "less sensitive to anchoring concentrated on the Rosettes foldout (fRos), which is alone in its $I×$L stratum, so the frozen secondary test cannot see anchoring there." This is a suggestion for PR #107 only. I did not touch that branch.
- **Not checked:** I did not run a power cell that excludes fRos. The precommit ruled out new cells, so the 0.44 → ~0.77 recovery is inferred, not measured.
- **Unchanged:** the observed-data verdict (RF1b-er official 100 vs 78.16, p 0.038; frozen rule not passed). No referent, reading or translation.
