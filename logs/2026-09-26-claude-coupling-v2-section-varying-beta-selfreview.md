# Section-varying-beta coupling-v2 design: design reasoning (written before any code runs)

**Trigger:** this project's own note, from the immediately preceding cycle, that "the actual
section-varying-beta mechanism design... remains a distinct, not-yet-started task" now that real
grounding data exists (`external-currier-ab-real-edge-gain-stats-summary.json`: Currier A's real
held-out edge-prediction gain is 0.1069 bits/boundary, Currier B's is 0.2381 — B's is ~2.227x A's).

## What's already known before this design (disclosed up front)

- `coupling-v2`'s `beta` parameter (currently fixed at 0.5 globally) is the probability, per token,
  that the coupling mechanism overwrites a token's first character with the previous token's last
  character — this is the mechanism that *directly constructs* the cross-token dependency the
  edge-gain criterion measures. Unlike the `nu_sub`-to-H2 relationship (which needed empirical
  discovery of direction, and turned out counter to the first guess), the `beta`-to-edge-gain
  relationship is close to definitional: more coupling probability for a section's tokens should
  produce a stronger held-out edge signal for that section's generated output, monotonically.
- The real edge-gain ratio (B:A = 2.227:1) is large — much larger than the `nu_sub` ratios that were
  found insufficient (4:1 was the mildest tested and failed; the real corpus ratios there were only
  ~1.15–1.36:1). This ratio is not directly comparable across mechanisms, but it is disclosed as a
  reason this design might behave differently from the `nu_sub` case, not as a prediction of success.
- No `beta` value has been varied by section in any design so far. `coupling-v3`/`coupling-v3.1`
  varied `beta` globally (uniformly across the whole corpus) to buy H2 headroom for the `nu_sub` work
  — a completely different use of the same parameter, not a precedent for this design's direction or
  magnitude.

## What has NOT been done before this design (result-blinding)

No coupling-v2 stream has been generated with a per-token, section-dependent `beta`. No per-section
edge-gain-gap has been computed for any generated (as opposed to real) stream. No claim about whether
this closes any fraction of the real edge-gain asymmetry, or whether it disturbs the pooled
six-criterion profile, has been made or estimated.

## The design

New mechanism function `apply_section_varying_coupling`: identical to `coupling-v2`'s own
`apply_coupling_v2` (target = prev_last, unchanged), except `beta` is looked up per-token from that
token's real Currier-label section instead of being one global value. Everything downstream
(`apply_boundary_shift_v2`, the substitution top-up) stays at its already-established primary
values (`nu_shift=1.0`, `nu_sub=0.01` global, unchanged — this design varies *only* `beta`, mirroring
exactly how the `nu_sub` design varied only that one parameter and left `beta` fixed).

**Beta pair — derived directly from the real edge-gain ratio, anchored at this family's own already-
established primary value:**
- `beta_B = 0.5` (unchanged — `coupling-v2`'s own existing primary value, kept for whichever section
  the ratio implies needs the *stronger* coupling, per the near-definitional beta→edge-gain relationship).
- `beta_A = 0.5 / 2.227 = 0.2245` (derived arithmetically from the real ratio, anchored at the existing
  primary value for B — not picked to hit any target, not reused from an unrelated grid).
- `beta_default = 0.5` for the 89 unlabeled lines (matching the existing primary value, same convention
  as every prior section-aware design in this project).

**New per-section criterion**: a generated-stream edge-gain-gap, computed by wrapping the transformed
stream to the real line-length template, splitting by real Currier label, and running the *same*
`edge_crossfit` function (16-fold, alpha=1.0) separately on each section's generated lines — exactly
analogous to how `section_gap` computes a per-section H2 gap for the `nu_sub` designs, but for edge-
gain instead of character-bigram entropy.

**Section-manipulation (anchor) check**: at `beta_A = beta_B = 0.5` (uniform, i.e. `coupling-v2`'s
own unmodified primary configuration), the generated edge-gain-gap should be small — this is
checked directly as part of this same run, using the identical seeds, before interpreting the
`beta_A=0.2245` result. Threshold fixed now, before any output exists: **the anchor's edge-gain-gap
must have absolute value under 0.05 bits/boundary** to pass (chosen as roughly 25% of the real gap's
own magnitude, 0.1312 bits/boundary — generous enough for seed noise, small enough to catch a real
labeling/splitting artifact, the same reasoning used for the analogous `nu_sub` anchor threshold).

**Seeds**: reuse `coupling-v2`'s own 3 pilot seeds (42, 179, 316) for a quick check, matching every
prior design's pilot-before-primary discipline.

## Honesty precommitment

Whatever the pooled six-criterion result and per-section edge-gain-gap are is reported exactly as
measured — including a result that disturbs the pooled edge-gain criterion (plausible, since `beta`
directly drives that criterion and is now being lowered for one section), a result that fails the
anchor check, or a result that succeeds at reproducing part of the real asymmetry but breaks
something else. This is a diagnostic (one disclosed configuration), not a preregistered mechanism
test with pass/fail promotion criteria — matching every prior section-aware diagnostic's own
categorization. It does not retry with a different beta pair or additional parameter changes without
a fresh precommitment.

## Why this is genuinely new work

This is the first design in this project's history to vary `beta` by section, and the first to test
edge-gain (rather than H2) as the per-section target statistic — a different criterion from every
prior section-aware attempt (`coupling-v3.1` x2, `coupling-v2` pilot grid, the corpus-derived `nu_sub`
check), all of which targeted the H2/Currier-A/B-entropy-gap question. This is a distinct empirical
question: can this mechanism family's `beta` lever construct the real edge-gain asymmetry, independent
of whether any `nu_sub` lever can construct the H2 asymmetry.
