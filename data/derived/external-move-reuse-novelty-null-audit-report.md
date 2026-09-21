# Move-reuse novelty null: preregistered mechanism-control result (negative finding)

Protocol: `data/external/move-reuse-novelty-null-manifest-v1.json`, solo Claude design (ChatGPT not automated; self-review in `logs/2026-09-21-claude-move-reuse-novelty-selfreview.md`). Fifth in the novelty-rule sequence, and the second (after budget-capped) to include a frozen honesty precommitment written before any outcome existed.

**Manipulation checks: both PASS.** **Primary verdict: FAIL** — 0/20. **A second consecutive negative finding, reported plainly per precommitment**: caching and reusing a small repertoire of validated substitution moves is worse than deriving a fresh bigram-conditional move each time, at matched dosage — and considerably worse on learned-unit scale specifically.

## Result

| Configuration | N | H1 | H2 | Units (of N) | Hapax | Edge | Joint pass |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline [reused] | 20 | 3.984 | 2.711 | 20/20 | 39.4% | -0.002 | 0/20 |
| edge_only [reused] | 20 | 3.992 | 2.731 | 16/20 | 51.3% | +0.379 | 0/20 |
| move_reuse_novelty_only [nu=0.2, beta=0] | 20 | 4.023 | 2.976 | 0/20 | 69.1% | -0.005 | 0/20 |
| **primary** [nu=0.2, beta=0.5] | 20 | 4.024 | **2.977** | **7/20** | 71.3% | +0.383 | 0/20 |
| weaker_novelty [nu=0.1] | 5 | 4.003 | 2.863 | 5/5 | 63.6% | +0.380 | 0/5 |
| stronger_novelty [nu=0.3] | 5 | 4.042 | 3.067 | 2/5 | 76.3% | +0.387 | 0/5 |

Required bands: H1 3.9763+/-0.15, H2 2.6897+/-0.15, unit-scale minimum at 32/64 merges with k64 gap in [0.90, 1.20], order share [0%, 2.0%], edge gain >=0.15 bits/boundary with >=15/16 positive blocks, hapax >=65%.

**Reuse diagnostic** (primary configuration): mean 10,442.5 reuse events vs. 392.8 fresh-search events per replicate — a **96.4% reuse rate**. The design worked exactly as intended mechanically (the cache converges to a small repertoire and gets heavily reused) — it just doesn't help.

## Direct comparison at matched dosage (the actual test)

| Design | nu | H2 | H2 pass | Units pass |
|---|---|---:|---:|---:|
| bigram-novelty-null (fresh search, PR #30) | 0.1 | 2.836 | 3/5 | 5/5 |
| move-reuse-novelty-null (cached, this result) | 0.1 | **2.863** | 0/5 | 5/5 |
| bigram-novelty-null (fresh search, PR #30) | 0.2 (primary) | 2.925 | 0/20 | 16/20 |
| move-reuse-novelty-null (cached, this result) | 0.2 (primary) | **2.977** | 0/20 | **7/20** |

At both matched dosages, reuse is worse for H2, and at the primary dosage it is substantially worse for learned-unit scale (7/20 vs. 16/20) — the largest single regression of any comparison in the five-design sequence.

## Interpretation

**The hypothesis under test — that reusing a small repertoire of moves builds learnable, repeated substructure that costs less than always-fresh locally-optimal moves — is not supported.** The mechanism behaves exactly as designed (heavy reuse, small cache, no degeneration to "always fresh search"), which rules out an implementation confound as the explanation. The most plausible account, offered as a hypothesis and not independently verified further here: stamping the *same* (position, replacement-atom) pair onto thousands of different tokens creates an artificially concentrated statistical spike at that specific transition — a much more extreme distortion of the stream's local structure than a bigram-conditional search re-derived fresh each time, which spreads its choices smoothly according to the running frequency distribution rather than repeatedly hammering the same few transitions. Repetition of the *same* move is not the same thing as repetition of *structure* in the sense BPE/H2 reward — the former is a narrow statistical anomaly, not a generalizable learnable pattern.

**Net effect on the five-design novelty-rule sequence**: uniform substitution (universal failure) -> unigram-frequency (closes H1) -> bigram-conditional (nearly closes units, closes H2 at low dosage in a majority of seeds) -> budget-capped (negative: front-loading is worse than spreading) -> move-reuse (negative: caching/reuse is worse than fresh derivation). Two consecutive negative results after bigram-novelty-null's partial win narrow the productive direction considerably: **the best evidence for closing H2 remains bigram-novelty-null's own `weaker_novelty` sensitivity** (nu=0.1, fresh bigram-conditional search, spread throughout the stream) — not a further mechanism variant. Continuing to invent reparameterizations of the same underlying idea has, twice in a row, made things worse rather than better; this is treated as sufficient evidence to synthesize the sequence for the knowledge base rather than test a sixth mechanism.

**This does not identify a mechanism or bear on meaning.**

## Provenance and execution

- Design and solo self-review: `logs/2026-09-21-claude-move-reuse-novelty-selfreview.md`, including the explicit rejection of two more naive "reuse" formulations (literal re-emission, which trivially fails; whole-suffix splicing, which increases rather than decreases disruption magnitude) before settling on the move-cache design actually tested.
- nu calibrated via a 3-seed, self-consistency-only, hapax-only pilot; frozen at nu=0.2, matching bigram-novelty-null and frequency-novelty-null for direct comparability. The pilot itself already showed the negative result (H2 worse at every nu tested) before the full run, disclosed rather than hidden.
- Implementation: `data/scripts/external_move_reuse_novelty_null_audit.py`. `baseline`/`edge_only` reused by reference (same file used by all three prior spread-mechanism designs).
