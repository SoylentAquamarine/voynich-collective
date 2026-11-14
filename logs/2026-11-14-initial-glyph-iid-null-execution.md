# Execution: repeated-initial run null (steering #72 / PR #116 item 3 follow-up)

Date: 2026-11-14 (~13:10 UTC, scheduled cycle) — Claude
Precommit: `logs/2026-11-14-initial-glyph-iid-null-selfreview.md`. The original 7-glyph-word design
(589402c) was withdrawn unrun. The executed design is the appended redesign (0b52409), pushed before
any code existed.
Script: `data/scripts/repeated_initial_run_null.py` (reuses `normalize_eva.py` functions unchanged).
Output: `data/derived/repeated-initial-run-null.json`. Inputs are SHA-256 pinned in the JSON.
Settings: 2,000 reps, seed 20261114. Runtime about 1 min.

## Results (event: a maximal run of ≥ 8 consecutive words with the same initial unit)

| Cell | K | obs | longest | N0 uniform-K (exp.) | N1 iid analytic (exp.) | N1 mean / p | N2 section-iid mean / p | N3 section-shuffle mean / p |
|---|---|---|---|---|---|---|---|---|
| ZL3b eva line | 117 | 1 | 8 | 3.0e-11 | 0.042 | 0.031 / 0.029 | 0.073 / 0.072 | 0.071 / 0.070 |
| **ZL3b eva paragraph (primary)** | 117 | **3** | 9 | 1.1e-10 | 0.155 | 0.120 / 0.0005 | 0.267 / 0.0015 | **0.248 / 0.0040** |
| ZL3b atomic line | 123 | 1 | 8 | 2.1e-11 | 0.034 | 0.031 / 0.031 | 0.061 / 0.059 | 0.059 / 0.056 |
| ZL3b atomic paragraph | 123 | 3 | 9 | 7.7e-11 | 0.127 | 0.083 / 0.0010 | 0.195 / 0.0015 | 0.205 / 0.0005 |
| RF1b-er eva line | 21 | 0 | 7 | 4.8e-06 | 0.040 | 0.037 / 1.0 | 0.074 / 1.0 | 0.064 / 1.0 |
| RF1b-er eva paragraph | 21 | 2 | 9 | 1.8e-05 | 0.152 | 0.129 / 0.011 | 0.312 / 0.037 | 0.271 / 0.025 |
| RF1b-er atomic line | 27 | 0 | 7 | 8.2e-07 | 0.030 | 0.029 / 1.0 | 0.053 / 1.0 | 0.054 / 1.0 |
| RF1b-er atomic paragraph | 27 | 2 | 9 | 3.1e-06 | 0.115 | 0.091 / 0.0045 | 0.187 / 0.016 | 0.186 / 0.017 |

Bonferroni α = 0.05/24 = 0.00208. N0 is the expected count of qualifying length-8 windows
(windows × K·K^-8), so it is per corpus, not per window.

The observed runs (descriptive, listed after the test):
- f2v (H): `chokeos chees chr cheaiin chokoishe chor cheol chol`. Present in both transcriptions.
- f8v (H): `chol chan ch{ck}y chor cheain char cheeky chor`. ZL3b only.
- f24v (H): `otol otaiir otchos okchom okcho octhyl odchees oesearies okam`, 9 words. Present in both transcriptions.

All three are in Herbal pages, and all three cross line boundaries inside a paragraph.

## Against predictions
- **Q1 held.** The primary cell has 3 runs, which is ≥ 1 and < 20.
- **Q2 held.** The N1 (global iid) p is below 0.05 in 6 of 8 cells. The two exceptions are the RF1b line-scope cells, which have 0 observed runs.
- **Q3 held only narrowly.** The primary N3 p = 0.0040 is above Bonferroni α = 0.0021, so it is not significant after correction. But it is nominally significant. Its sibling cell, ZL3b atomic paragraph N3 (p = 0.0005), passes Bonferroni. The RF1b paragraph cells are nominal only (p = 0.017–0.037). In plain terms, a small excess of long same-initial runs survives realistic nulls in ZL3b. It is weaker in RF1b. It is absent at line scope.
- **P1 (original design, partly reused as a descriptive check):** the "alphabet size" is not 26 or 47 under either segmentation.
  - RF1b K = 21 / 27 (EVA / atomic).
  - ZL3b K = 117 / 123. This is inflated by distinct `@NNN;` extended-EVA codes and `{..}` ligature units, each of which counts as its own initial.
  - "47 symbols" therefore has no fixed meaning without a stated segmentation.

## What this means (bounded)
1. **The paper's chance figure is far too small.** A uniform-alphabet chance figure for "eight words with the same initial" (26^-7 ≈ 1.2e-10, or 47^-7) is not the right scale for the question.
   - Searched corpus-wide, with the real skewed initials (o ≈ 20%, c/ch ≈ 16–19%, q ≈ 15%), the expected number of such runs is about **0.1–0.3 per corpus**. That makes the per-window uniform figure about nine orders of magnitude too small.
   - This holds whichever of 26 or 47 is used. It is the substantive point behind PR #116 item 3, now measured on pinned inputs.
2. **A modest residual excess remains.** Observed runs are 3 against a section-shuffle mean of about 0.25. This is consistent with known local (page- or paragraph-level) word-form clustering in Voynichese. It is not a measurement of Turenne's specific run, which Claude cannot identify because the paper is unread. It is not evidence for or against the pastiche hypothesis, any language, or any reading.

## Disclosures
- The listing of observed runs was produced after the test, by a short ad-hoc script that is not committed. It reproduces the JSON counts for EVA paragraph scope.
- In N3, `?`-containing words are shuffled along with the others, each with a unique code. In N1/N2 they stay fixed in place. This is a minor asymmetry.
- arxiv.org is refused by this sandbox, so neither the paper nor its supplement was read by Claude. The facts about the paper come from PR #116 and steering #72.
- No Yale bytes were used and no corpus was acquired. J11 remains QUEUED.
