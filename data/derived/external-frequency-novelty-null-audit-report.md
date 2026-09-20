# Frequency-weighted novelty null: preregistered mechanism-control result

Protocol: `data/external/frequency-novelty-null-manifest-v1.json`, a solo Claude design (ChatGPT not automated at time of design; solo self-review documented in `logs/2026-09-20-claude-frequency-novelty-selfreview.md`). Base mechanism identical to `boundary-state-null` (Naibbe + boundary coupling at beta=0.50); only the novelty-injection rule changes, from uniform substitution to an exhaustive frequency-weighted search over the replicate's own running atom-unigram distribution. `baseline`/`edge_only` are reused by reference from the boundary-state-null audit (not rerun — `baseline` is seed-invariant by construction, `edge_only`'s reuse was frozen in the manifest before this run).

**Manipulation checks: both PASS** (boundary: 20/20 paired increase + 20/20 criterion, reused; novelty: 20/20 paired hapax increase + 20/20 criterion, this run).

**Primary verdict: FAIL** — 0/20 primary replicates pass all six criteria (required >=16/20). But this is the closest any of the six mechanism tests run in this project has come: the primary configuration now passes **four of six** criteria cleanly and a fifth (learned-unit scale) in 16/20 replicates — only H2 fails universally.

## Result

| Configuration | N | H1 | H2 | Unit ckpt (16/20+) | k64 gap | Order share | Hapax | Edge gain | Joint pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline [reused] | 20 | 3.984 | 2.711 | 20/20 | 1.034 | 1.30% | 39.4% | -0.002 | 0/20 |
| edge_only [reused] | 20 | 3.992 | 2.731 | 16/20 | 1.183 | 1.10% | 51.3% | +0.379 | 0/20 |
| frequency_novelty_only [beta=0, nu=0.2] | 20 | 3.996 | 2.945 | 0/20 | 0.848 | 0.88% | 68.5% | -0.005 | 0/20 |
| **primary** [beta=0.5, nu=0.2] | 20 | **4.002** | 2.946 | 16/20 | 1.077 | 0.72% | 71.0% | +0.385 | 0/20 |
| weaker_novelty [beta=0.5, nu=0.1] | 5 | 3.991 | 2.846 | 5/5 | 1.086 | 0.84% | 63.4% | +0.380 | 0/5 |
| stronger_novelty [beta=0.5, nu=0.3] | 5 | 4.010 | 3.020 | 4/5 | 1.030 | 0.63% | 75.8% | +0.387 | 0/5 |

Required bands: H1 3.9763+/-0.15, H2 2.6897+/-0.15, unit-scale minimum at 32/64 merges with k64 gap in [0.90, 1.20], order share [0%, 2.0%], edge gain >=0.15 bits/boundary with >=15/16 positive blocks, hapax >=65%.

## Per-criterion pass counts

- **primary** (beta=0.5, nu=0.2): H1 **20/20** | H2 **0/20** | units **16/20** | order **20/20** | edge **20/20** | hapax **20/20**
- **frequency_novelty_only** (beta=0, nu=0.2): H1 20/20 | H2 0/20 | units 0/20 | order 20/20 | edge 0/20 (as expected, no coupling) | hapax 20/20
- For comparison, the prior **uniform-substitution** design at the equivalent configurations (from `external-boundary-state-null-audit-summary.json`, not rerun): `novelty_only` H1 0/20, H2 0/20, units 0/20; `primary` H1 0/20, H2 0/20, units 0/20 — all three universally failed under uniform substitution.

## Interpretation

**The self-review's central hypothesis was correct, and the fix worked further than expected.** Frequency-weighting the novelty substitution — trying the replicate's own most-common atoms first when creating an unseen variant, instead of a uniform draw over all 25 alternatives — was predicted to reduce entropy damage. It didn't just reduce it: **it fully closes the H1 gap.** Every one of the 20 primary replicates now lands inside the required unigram-entropy band (mean 4.002, vs. the uniform design's 4.173-4.209 across its five prior configurations, all of which failed 0/20). This is a clean, mechanistically expected result: H1 is unigram (single-character) entropy, and a substitution rule built directly from the unigram frequency distribution should preserve it almost by construction — the pilot calibration already showed this pattern taking shape.

**H2 (bigram / conditional entropy) tells a different, more informative story.** It improves substantially but does not close: primary's mean H2 is 2.946, versus 2.5-2.84 required and versus 3.35+ under the old uniform design — roughly half the excess is gone, but what remains is a clean, universal 0/20 failure. This makes sense on the same logic that explains the H1 fix: a unigram-frequency-weighted substitution controls *which characters* appear how often, but says nothing about *which pairs* of characters appear together. Creating an unseen variant by swapping in a locally common atom can still produce a locally implausible bigram, which is exactly what H2 penalizes. The fix targeted the right mechanism (frequency vs. uniform) but at the wrong order of statistic (unigram vs. bigram) to fully close this specific gap.

**Learned-unit scale improved from a universal 0/20 failure to 16/20** — most replicates now land the BPE k64 gap inside [0.90, 1.20] (primary mean 1.077, squarely in range), consistent with H2 being the more specifically damaged statistic: unit-scale (multi-symbol compressibility) tracks local structure more like H2 than H1, so it partially — not fully — recovers alongside H1's full recovery.

**A tempting post-hoc observation, explicitly not acted on.** `weaker_novelty` (nu=0.1) lands H2 at 2.846 — only 0.006 bits outside the 2.840 upper bound — while its hapax share (63.4%) is only 0.016 below the 0.65 floor. That's a near-miss in both directions at a configuration this design didn't select as primary. Per the manifest's frozen rule ("sensitivities cannot rescue primary failure") and this project's standing discipline against retroactively picking a parameter after seeing outcomes, this is reported honestly as a near-miss, not chased with a new frozen nu. Any attempt to split the difference would need its own preregistration, run against fresh seeds, with the near-miss disclosed as the reason for testing that region — not treated as if it were the original prediction.

**Net effect on the project's four/five/six-mechanism record**: this is the first constructive null to pass more than one criterion at the primary configuration simultaneously with edge and hapax — four criteria clean, a fifth at 16/20, only H2 a clean universal failure. It does not identify a mechanism or bear on meaning. It does sharpen the open question considerably: the remaining gap is specifically the base mechanism's *pairwise* (bigram) local structure under novelty injection, not vocabulary, not edge-coupling, and now not even unigram character frequency. A novelty mechanism that preserves the *conditional* (order-1) distribution rather than just the unigram distribution is the obvious next candidate — and is exactly the kind of new, non-arbitrary design this result motivates, not a retroactive parameter tweak to this one.

## Provenance and execution

- Design and solo self-review: `logs/2026-09-20-claude-frequency-novelty-selfreview.md`. Caught and fixed one real defect before any outcome existed (a bounded-random-search confound that would have made search thoroughness, not frequency-weighting, the explanatory variable — fixed to an exhaustive frequency-ordered search matching the original design's search guarantee).
- nu calibrated via a 3-seed, self-consistency-only pilot (hapax share only, never compared against H1/H2/units/edge during calibration) before any primary-configuration outcome was computed; frozen at nu=0.2.
- Implementation: `data/scripts/external_frequency_novelty_null_audit.py`, reusing the checksum-pinned Naibbe source and the project's unchanged entropy/BPE/token-order/edge pipeline.
- `baseline`/`edge_only` reused by reference (`data/external/reference/boundary-state-null-baseline-edgeonly-reference.json`) rather than rerun, per the manifest's frozen commitment — `baseline` is provably seed-invariant (beta=nu=0 is an identity transform), `edge_only`'s reuse was committed before this run.
