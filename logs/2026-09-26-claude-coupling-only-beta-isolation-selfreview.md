# Isolating section-varying-beta's own contribution from the boundary-shift confound: design reasoning (written before any code runs)

**Trigger:** the immediately preceding cycle's diagnostic conclusively localized the section-varying-beta
design's anchor bias to `boundary-shift-v2`, not `coupling-v2`'s own mechanism — but left open whether
`beta`'s own deliberate per-section manipulation contributes anything real once that confound is
factored out. This design isolates exactly that.

## What's already known before this design (disclosed up front)

- Coupling-v2 alone (no boundary-shift, no top-up), **uniform** beta=0.5: mean generated edge-gain-gap
  = +0.0064 (noise-level, flips sign across seeds) — already measured.
- Coupling-v2 + boundary-shift-v2 (no top-up), uniform beta=0.5: mean gap = -0.0575 — already measured,
  confirms the confound is in boundary-shift, not coupling.
- The full section-varying-beta design (beta_A=0.2245, beta_B=0.5, WITH boundary-shift and top-up):
  mean gap = -0.3070 — already measured, but confounded.

## What has NOT been done before this design (result-blinding)

**Coupling-v2 alone, with the design's own PER-SECTION beta values (beta_A=0.2245, beta_B=0.5, no
boundary-shift, no top-up) has never been run.** This is the missing data point: if coupling-v2's own
mechanism, isolated from boundary-shift entirely, shows a real, non-noise-level edge-gain-gap when beta
is varied by section, that would be beta's own clean contribution — comparable directly to the
already-measured uniform-beta coupling-only baseline (+0.0064).

## The design

Run `apply_section_varying_coupling` (already built) at `beta_A=0.2245`, `beta_B=0.5` — the exact same
per-section values as the confounded design — but **skip boundary-shift-v2 and the substitution top-up
entirely**, identical in structure to the already-run "coupling only, uniform beta" diagnostic. Same 3
pilot seeds (42, 179, 316).

**Predicted outcome, stated before running**: if `beta`'s own per-section manipulation contributes
something real (not just noise), this result should differ from the uniform-beta coupling-only baseline
(+0.0064) by a similar direction and rough order of magnitude to *part of* the confounded design's own
-0.3070 gap — though not necessarily the full amount, since the confounded run's boundary-shift and
top-up steps could themselves interact with the now-varied beta in ways not present in the uniform-beta
diagnostic. If this isolated result is itself noise-level (close to the uniform-beta coupling-only
baseline, +0.0064), that would mean essentially all of the confounded design's -0.3070 gap traces back
to the same boundary-shift artifact, not to beta at all — a genuinely different, and rather deflating,
conclusion from what the confounded result on its own suggested.

## Honesty precommitment

Whatever this isolated coupling-only result is — a clear beta-attributable effect, pure noise, or
something in between — is reported exactly as measured, including if it contradicts the stated
prediction above (which is disclosed precisely so it can be checked against the actual result, not
substituted for it).
