# 2026-09-21 — Solo self-review: boundary-shift-v2 novelty null design

Design: `data/external/boundary-shift-v2-novelty-null-manifest-v1.json`. Directly motivated by actually reading the order-share scoring code (`analysis/reproduce_scale_transition.py: order_information()`) rather than speculating about why boundary-shift-novelty-null (PR #34) failed on token-order-share.

## The diagnosed mechanism, verified from source, not guessed

`order_information()` caps the vocabulary at the top-2000 most frequent token types and collapses everything else into a single `<other>` symbol before measuring adjacent-token mutual information. Boundary-shift-v1's rule required BOTH pieces of a shift to be simultaneously unseen — meaning every successful shift produces two adjacent brand-new types, both far too rare to be in the top-2000, both collapsing to `<other>`. This manufactures a strong, artificial `<other>`-follows-`<other>` adjacency that the MI-based order metric detects as excess predictability — not genuine whole-token order, an artifact of how the metric handles rare vocabulary colliding with an operation that creates two adjacent rare tokens at once.

## The fix, and why it's more than just "less strict"

Changing the acceptance rule to prefer exactly one new piece per shift (reusing an existing type for the other) directly avoids the double-novel-adjacency that causes the `<other>`-collapse problem. An informal exploratory check (disclosed in the manifest's `result_blinding`, not treated as a frozen result) found this also dramatically raised the achievable hapax ceiling — from ~64% (v1, at nu=1.0) to ~92% (v2, at nu=1.0). Worked out why, since this was not initially obvious: v1's shifted pieces were always both-novel and therefore never became eligible again (an eligible pair requires being an already-*emitted* repeat, and a fresh unique type never recurs) — v1 was structurally supply-limited with no feedback. v2 reuses an existing type for one piece of every successful shift, and that reused type can itself become newly *eligible* on a later occurrence — a self-regenerating feedback loop v1 never had. This is presented as an explanation for the observed effect, not an additional claim requiring separate verification, since it followed directly from re-reading the eligibility condition.

## New risk flagged, not previously relevant to v1

Because v2 deliberately reuses *existing* types for one piece of each shift, there is a real possibility this converges onto a small set of "hub" types disproportionately reused across many shifts — a different kind of concentration risk, structurally similar to what move-reuse-novelty-null (PR #32) found costly when it comes to *choosing* substitutions. This has not been checked directly and is named here as something to watch for in interpretation, not dismissed.

## Issues re-checked (unchanged from v1, still hold)

Circularity: no Voynich-derived input. H1 exact invariance: still guaranteed by construction (no character added/removed/substituted), and confirmed empirically in the exploratory check (H2 unaffected too, ~2.71 across the whole nu sweep tested, matching baseline). Scan mechanics and edge cases: identical to v1, already reviewed there.

## Honesty precommitment, restated for this design specifically

The exploratory nu=0.2 check that motivated writing this manifest was NOT a proper pilot calibration — it was informal, diagnostic, aimed at confirming the mechanism, at a hand-picked nu. The actual frozen pilot below is hapax-only, exactly as in every prior design. If the properly-calibrated nu does not also land order/H2 in band, that is reported plainly — the promising exploratory numbers do not pre-determine the frozen result.

## Verdict

Accept the design as drafted. Proceeding to implement and pilot-calibrate `nu` under the frozen hapax-only rule.

## Pilot results (frozen calibration, hapax-only)

3 seeds, `boundary_shift_v2_only` config (beta=0), swept nu in {0.1, 0.15, 0.2, 0.25, 0.3}:

| nu | hapax mean | H2 mean (recorded, not used for selection) | order mean (recorded, not used for selection) |
|---|---|---|---|
| 0.10 | 0.593 | 2.711 | 0.0141 |
| 0.15 | 0.645 (below floor) | 2.711 | 0.0161 |
| 0.20 | 0.688 (in band, smallest) | 2.711 | 0.0174 |
| 0.25 | 0.718 | 2.711 | 0.0189 |
| 0.30 | 0.745 | 2.711 | 0.0192 |

**Frozen: nu=0.2**, selected on hapax alone, exactly matching the earlier informal exploration's nu — not chosen because of that match, but because it's genuinely the smallest in-band value under the same rule used in every prior design. At this nu, order (mean 0.0174, all three pilot seeds individually under the 0.02 ceiling) and H2 (2.711, exactly matching baseline, confirming exact invariance holds for v2 too) both land comfortably in band. This is reported as an observation the frozen calibration produced, not as something engineered by picking nu to make it so.
