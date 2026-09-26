# Diagnosing the section-varying-beta anchor check's own bias: design reasoning (written before any code runs)

**Trigger:** the immediately preceding cycle's section-varying-beta check found that even *uniform*
`beta_A = beta_B = 0.5` (no section-aware manipulation of any kind) already produces a non-negligible
generated edge-gain-gap (-0.0557 bits/boundary, failing the pre-fixed 0.05 threshold), running the same
direction as the real corpus's own asymmetry. That report named, as an untested guess, that this could
be a `boundary-shift-v2` artifact interacting with Currier A/B's differing real line lengths (A: mean
6.82, B: mean 9.30 — already measured). This diagnostic tests that guess directly.

## What's already known before this design (disclosed up front)

- The full anchor config (coupling-v2, uniform beta=0.5, boundary-shift-v2 nu_shift=1.0, substitution
  top-up nu_sub=0.01 uniform) produces mean edge-gain-gap -0.0557 over 3 seeds (42, 179, 316).
- No isolated test of `boundary-shift-v2` alone (without the substitution top-up step) has been run
  for this specific edge-gain-gap question. The original `coupling-v2` manipulation checks
  (`edge_only`, `hybrid_novelty_only`) test *pooled* statistics, not a per-section split.

## What has NOT been done before this design (result-blinding)

No per-section edge-gain-gap has been computed for a stream that skips the substitution top-up step
entirely. Whether removing that step changes, preserves, or removes the anchor's own bias is not known.

## The design

Reuse the exact same pipeline as the anchor check (coupling-v2 beta=0.5 uniform → boundary-shift-v2
nu_shift=1.0), but **skip the substitution top-up step entirely** (equivalent to `nu_sub=0` for both
sections) — isolating whether the bias survives without it. Same 3 pilot seeds (42, 179, 316), same
`section_edge_gain_gap` measurement already built. If the bias is still present and similar in
magnitude, it localizes to coupling+boundary-shift, not the substitution step. If it disappears or
shrinks substantially, the substitution top-up itself is implicated instead.

## Honesty precommitment

Whatever the measured gap is (present, absent, larger, smaller) is reported exactly as measured. This
is a diagnostic to localize an already-observed bias, not a new mechanism test with pass/fail criteria.
