# Execution: within-page / within-paragraph shuffle nulls for long same-initial runs

Date: 2026-11-17 (scheduled cycle) — Claude. Precommit: `logs/2026-11-17-initial-run-within-scope-shuffle-selfreview.md`
(pushed as 297bf66 before any code). Script: `data/scripts/repeated_initial_within_scope_null.py` (imports the
11-14 parse/segmentation/paragraph scope unchanged). Output: `data/derived/repeated-initial-within-scope-null.json`
(input SHA-256 pinned). 2,000 reps, seed 20261117, runtime ~12 s. Observed S1 values reproduce the 11-14 JSON (3/3/2/2).

## Results (paragraph scope; S1 = runs >= 8 same-initial words; S2 = adjacent same-initial pairs)

| Cell | S1 obs | N3 mean (11-14) | N4 page mean / p | N5 paragraph mean / p | S2 obs | N5 S2 mean ± sd | S2 z | S2 p (N4, N5) |
|---|---|---|---|---|---|---|---|---|
| **ZL3b eva (primary)** | 3 | 0.248 | 1.110 / 0.109 | **1.118 / 0.106** | 5679 | 5417.7 ± 61.4 | 4.25 | 0.0005, 0.0005 |
| ZL3b atomic | 3 | 0.205 | 0.834 / 0.050 | 0.820 / 0.046 | 5154 | 4898.8 ± 60.8 | 4.20 | 0.0005, 0.0005 |
| RF1b-er eva | 2 | 0.271 | 1.250 / 0.367 | 1.221 / 0.343 | 5700 | 5439.5 ± 62.9 | 4.14 | 0.0005, 0.0005 |
| RF1b-er atomic | 2 | 0.186 | 0.813 / 0.188 | 0.838 / 0.217 | 5109 | 4866.2 ± 61.6 | 3.95 | 0.0005, 0.0005 |

The S2 p-values are at the 2,000-rep floor (1/2001). Bonferroni alpha = 0.00625.

## Against the frozen decision rule and the predictions
- **Verdict: "composition-explained."** The primary-cell N5 p is 0.106, which is ≥ 0.05. No S1 cell is
  Bonferroni-significant under N4 or N5. Only ZL3b atomic is nominal, at p ≈ 0.05.
- **P1 held.** The N5 mean is 1.12, which is ≥ 0.8, and p ≥ 0.05.
- **P2 held.** S2 exceeds both N4 and N5 at the p floor in all four cells (z ≈ 4.0–4.3). That is about
  4.8–5.0% more adjacent same-initial pairs than within-paragraph order alone gives.
- **P3 held only partly.** Both N4 and N5 are far above N3 (about 4.5×), but N4 ≈ N5 within Monte Carlo
  noise. The precommitted ordering N3 < N4 < N5 holds in 2 of 4 cells. The material information is that
  **page composition alone** recovers almost all of the expected long-run rate. Paragraph composition adds
  nothing measurable beyond the page.

## What this means (bounded)
1. **The 11-14 "modest residual excess" of ≥8-runs is explained by composition.** Reshuffling words within
   their own page or paragraph produces ~1 such run per corpus on average and ≥3 about 10% of the time. The
   3 observed Herbal runs (f2v, f8v, f24v) are therefore not evidence of an ordering mechanism beyond local
   vocabulary concentration. This **tests and supports** the 11-14 log's untested "consistent with local
   clustering" wording, with a refinement: the relevant level is page composition.
2. **A separate first-order ordering signal does exist.** Adjacent words share an initial ~5% more often than
   paragraph composition predicts, and this holds in both transcriptions and both segmentations. It is
   high-count and robust, but it is small in effect. It was **not decomposed**. It likely overlaps the repo's
   known adjacent-token repeat tendency (`data/derived/adjacent-token-repeat-summary.json`), so this run does
   not say whether exact-repeat pairs account for it.
3. For the Turenne audit, the claim that 8-word same-initial runs are surprising is weaker still. Even the
   ordering-agnostic local null makes them unremarkable. ZL3a and the paper remain unread by Claude.

## Disclosures
- `?` words are shuffled with unique codes, the same as N3. The N4 groups are pages restricted to
  paragraph-text loci.
- The S2 decomposition (exact repeats vs. different words with the same initial) is not done. It is a
  natural bounded follow-up.
- No language, reading, pastiche or translation claim follows. No network access was used, J11 is
  untouched, and no Yale bytes were used.
