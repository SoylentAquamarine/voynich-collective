# 2026-09-21 — Solo self-review: move-reuse novelty null design

Design: `data/external/move-reuse-novelty-null-manifest-v1.json`. Solo self-review, ChatGPT not automated.

## What this design is testing, and why the obvious versions of "reuse" don't work

Before settling on this design, I considered and rejected two more naive formulations of "reuse an already-created novel form":

1. **Literally re-emit a previously-created mutated string.** Rejected: the whole point of a novelty event is producing an unseen type; re-emitting a string that was already emitted once is just a repeat, contributes nothing to hapax share, and isn't actually a "novelty" mechanism at all.
2. **Splice a donor's mutated suffix (positions 1..n-1) onto a new token's boundary-coupled position 0.** Rejected: this replaces the *entire* interior of the token, not a single atom — a larger, not smaller, disruption than any design tested so far, working against the stated goal of reducing pairwise-structure damage per unit of hapax gained.

**What this design actually tests**: cache the small set of *(position, replacement-atom)* moves that single-atom substitution has already used successfully within this replicate, and prefer reusing one of those moves (applied to a *different* original token of matching length, producing a genuinely new, unseen string) over independently deriving a fresh locally-optimal move via the bigram-conditional search each time. The granularity of disruption (one atom, one position) is unchanged from bigram-novelty-null — only *which* atom/position gets chosen, and whether that choice is drawn from a small reused repertoire or freshly computed, differs. The hypothesis: a small repertoire of moves applied repeatedly across many tokens could build *learnable, repeated substructure* — exactly what BPE/multi-symbol-unit compression and H2 reward — rather than accumulating many locally-plausible but structurally distinct one-off disruptions.

## Issues checked

**1. Circularity.** The move cache is built only from this replicate's own successful substitutions, never Voynich. No leak.

**2. Degeneracy check, addressed via the reuse-rate diagnostic.** Two failure modes are possible and neither would be a meaningful design defect requiring a fix, but both need to be checked and reported, not silently assumed away: (a) cached moves rarely apply (most candidates' lengths don't match cached move lengths well, or the specific cached atom collides with the original or with an already-emitted string), and the design silently degenerates to "always fresh search" — i.e., behaves identically to bigram-novelty-null; (b) the opposite, where one or two early moves dominate almost all events, meaning nearly the same (position, atom) pair gets stamped onto every token of a given length — worth knowing since it affects how to interpret any result (a genuinely diverse but reused repertoire is a different finding than a near-constant stamp).

**3. Determinism.** Cache selection order is deterministic (use-count descending, ties by creation order) with no RNG involved in the selection itself; the RNG is still used for the boundary-coupling gate, the nu-trigger gate, and the fresh-search fallback exactly as in bigram-novelty-null. Fully reproducible given a seed.

**4. Fairness of the length-matching rule.** Using exact token length as the sole compatibility criterion is simple and frozen in advance, not tuned after seeing results. It is coarse (doesn't account for which specific atoms are present), which is intentional — a finer-grained matching rule risks being retroactively justified by outcomes if designed after seeing what "works."

**5. Honest expectation.** This is a genuinely different mechanism from anything tested, but there's no strong prior guarantee it helps rather than simply performing similarly to bigram-novelty-null (if reuse is rare) or worse (if a small repertoire concentrates disruption in a way analogous to budget-capping's front-loading, which already showed concentration can hurt). The manifest's honesty precommitment covers this: if it doesn't materially improve on bigram-novelty-null's nu=0.1 result, or if the reuse-rate diagnostic shows the design degenerated to one of the two failure modes above, that will be reported plainly, and this is very plausibly the point where the novelty-rule sequence gets written up for the knowledge base rather than extended with a sixth mechanism.

## Verdict

Accept the design as drafted. Proceeding to pilot-calibrate `nu`.

## Pilot calibration (self-consistency only, hapax only) — and an early answer to the honesty precommitment

3 seeds, `move_reuse_novelty_only` config (beta=0), swept nu in {0.1,0.15,0.2,0.25,0.3}:

| nu | mean hapax | mean H2 | mean reuse_events | mean fresh_events | reuse_share |
|---|---|---|---:|---:|---:|
| 0.10 | 0.589 | 2.861 | ~5,799 | ~370 | 94.0% |
| 0.15 | 0.646 | 2.923 | ~8,241 | ~398 | 95.4% |
| 0.20 | 0.693 (in band) | 2.977 | ~10,384 | ~408 | 96.2% |
| 0.25 | 0.725 (in band) | 3.022 | ~12,484 | ~413 | 96.8% |
| 0.30 | 0.748 (in band) | 3.065 | ~14,491 | ~422 | 97.2% |

Frozen: **nu=0.2**, matching bigram-novelty-null's chosen nu for direct comparison.

**The pilot already answers the honesty precommitment, before the full run**: the cache converges fast (only ~400 distinct moves ever get created, out of tens of thousands of eligible events) and gets reused heavily (94-97% of events are cache hits, not fresh searches) — so the design does behave as intended, not degenerating to "always fresh search." But H2 is **worse** than bigram-novelty-null at every matched nu (e.g. nu=0.2: 2.977 here vs. 2.925 for fresh bigram search), not better. A plausible explanation: reusing a small repertoire of moves thousands of times each concentrates an enormous, artificial statistical spike onto a handful of specific (position, atom) transitions — the opposite of the smoothly frequency-weighted distribution a fresh bigram-conditional search produces each time — and that concentration appears to cost more local-structure fit than it buys back through repetition. This is disclosed plainly per the precommitment: this design does not improve on bigram-novelty-null, and per the manifest's own stated criterion, this is very plausibly the point to write up the whole five-design novelty-rule sequence rather than invent a sixth mechanism.
