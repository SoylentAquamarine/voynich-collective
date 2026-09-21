# Bigram-conditional novelty null: preregistered mechanism-control result

Protocol: `data/external/bigram-novelty-null-manifest-v1.json`, a solo Claude design (ChatGPT not automated; self-review in `logs/2026-09-21-claude-bigram-novelty-selfreview.md`). Third in a sequence testing the same coupling mechanism (beta=0.50, unchanged) against three different novelty-substitution statistics: uniform (boundary-state-null), unigram-frequency (frequency-novelty-null, PR #29), and now bigram-conditional (order-1, this result).

**Manipulation checks: both PASS.** **Primary verdict: FAIL** — 0/20 (required >=16/20). Incremental improvement over frequency-novelty-null: learned-unit scale moves from 16/20 to **19/20**, and H2 improves slightly (2.925 vs. 2.946), but the primary configuration's H2 gap does not close — still 0/20.

## Result

| Configuration | N | H1 | H2 | Units (of N) | k64 gap | Order | Hapax | Edge | Joint pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline [reused] | 20 | 3.984 | 2.711 | 20/20 | 1.034 | 1.30% | 39.4% | -0.002 | 0/20 |
| edge_only [reused] | 20 | 3.992 | 2.731 | 16/20 | 1.183 | 1.10% | 51.3% | +0.379 | 0/20 |
| bigram_novelty_only [beta=0, nu=0.2] | 20 | 4.016 | 2.920 | 0/20 | 0.858 | 0.86% | 67.2% | -0.004 | 0/20 |
| **primary** [beta=0.5, nu=0.2] | 20 | **4.020** | 2.925 | **19/20** | 1.076 | 0.76% | 69.8% | +0.381 | 0/20 |
| weaker_novelty [beta=0.5, nu=0.1] | 5 | 4.002 | **2.836** | 5/5 | 1.098 | 0.90% | 62.9% | +0.377 | 0/5 |
| stronger_novelty [beta=0.5, nu=0.3] | 5 | 4.033 | 2.997 | 5/5 | 1.067 | 0.66% | 74.9% | +0.381 | 0/5 |

Required bands: H1 3.9763+/-0.15, H2 2.6897+/-0.15, unit-scale minimum at 32/64 merges with k64 gap in [0.90, 1.20], order share [0%, 2.0%], edge gain >=0.15 bits/boundary with >=15/16 positive blocks, hapax >=65%.

## Per-criterion pass counts

- **primary** (beta=0.5, nu=0.2, bigram): H1 20/20 | H2 **0/20** | units **19/20** | order 20/20 | edge 20/20 | hapax 20/20
- **frequency-novelty-null primary** (unigram, same nu=0.2, for comparison): H1 20/20 | H2 0/20 | units 16/20 | order 20/20 | edge 20/20 | hapax 20/20
- **weaker_novelty sensitivity** (bigram, nu=0.1): H2 passes in **3/5** seeds (mean 2.836, inside the 2.540-2.840 band) — the first time any novelty-active configuration in this three-design sequence has H2 pass in a majority of seeds, though this is a non-primary sensitivity, and hapax fails at this dosage (62.9%, below the 65% floor).

## Interpretation

**Bigram-conditioning is a genuine, mechanistically real improvement over unigram-frequency-weighting — but a smaller one at the dosage vocabulary-openness requires.** At the calibrated primary dosage (nu=0.2, chosen purely for hapax, identical to frequency-novelty-null's choice for a clean comparison), H2 moves from 2.946 (unigram) to 2.925 (bigram) — a real but modest step, nowhere near closing the ~0.09-bit gap to the 2.840 upper bound. Learned-unit scale improves more substantially, from 16/20 to 19/20 passing seeds — nearly complete.

**The `weaker_novelty` sensitivity (nu=0.1, not primary) is the most informative single data point in this result.** At half the substitution rate, bigram-conditioning gets H2 to pass in 3 of 5 seeds (mean 2.836, inside the required band) — something no novelty-active configuration in this or either prior design has done before, even as a non-primary sensitivity. The same nu under the *unigram*-frequency design (frequency-novelty-null's own `weaker_novelty`) landed H2 at 2.846, just outside the band, 0/5 passing. This is a real, disclosed comparison at matched nu: bigram-conditioning outperforms unigram-frequency specifically when substitution volume is lower.

**The likely explanation, stated as a hypothesis and not overclaimed**: the H2 gap is driven by *how many* pairwise-disrupting substitutions accumulate over a replicate at least as much as by *which* statistic selects each individual substitution. At nu=0.1, few enough events happen that a bigram-conditional choice (locally plausible given what precedes it) keeps most of the stream's pairwise structure intact. At nu=0.2 — the rate needed to clear the hapax floor — enough substitutions accumulate that their cumulative disruption to pairwise structure outweighs how "locally sensible" each individual one is, regardless of which statistic ordered the search. This reframes the open question: not just "which local statistic should order novelty substitutions" (now tested three ways: uniform, unigram, bigram) but **"can vocabulary openness be achieved with fewer, more surgical interventions rather than many nu-gated ones"** — a length-preserving single-substitution-per-repeat-event design may simply need too many events to hit 65%+ hapax on an ~80,000-token stream.

**Net effect on the project's mechanism-test record**: this is now a monotonic sequence — uniform (H1/H2/units all universally fail) -> unigram-frequency (H1 closes, units mostly closes, H2 stays open) -> bigram-conditional (H1 closes, units nearly closes at 19/20, H2 narrows further but stays open, and closes in a majority of seeds at half dosage). Three designs sharing one base mechanism and one coupling rule, differing only in the statistic ordering an otherwise-identical exhaustive search, produce a clean, interpretable gradient rather than a flat wall of failures — itself informative about where the remaining difficulty actually lives (substitution volume/dosage, not statistic choice).

**This does not identify a mechanism or bear on meaning.** It does sharpen the open question a second time: from "which novelty rule" (frequency-novelty-null's contribution) to "how much novelty volume is compatible with H2 at all" (this result's contribution) — a dosage question, not a rule-design question, and the natural next preregistration follows directly from that reframing rather than from another substitution-statistic variant.

## Provenance and execution

- Design and solo self-review: `logs/2026-09-21-claude-bigram-novelty-selfreview.md`. No defects found requiring a design change this time (the exhaustive-search lesson from frequency-novelty-null was applied from the first draft); one real uncertainty flagged and not glossed over (possible interaction between boundary coupling's position-0 rewrite and the very next substitution's "preceding atom" context).
- nu calibrated via a 3-seed, self-consistency-only, hapax-only pilot; frozen at nu=0.2, matching frequency-novelty-null exactly. H2 was recorded during the pilot for later interpretation but explicitly not used to select nu — nu=0.1, which happened to land H2 in-band during the pilot, was not chosen, since it undershoots the hapax floor and the calibration rule is hapax-only by design.
- Implementation: `data/scripts/external_bigram_novelty_null_audit.py`. `baseline`/`edge_only` reused by reference (same `data/external/reference/boundary-state-null-baseline-edgeonly-reference.json` used by frequency-novelty-null) rather than rerun.
