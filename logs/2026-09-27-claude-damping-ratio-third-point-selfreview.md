# Characterizing the damping ratio's shape: a third beta_A point (design, written before any code runs)

**Trigger:** Round 115 (`comms/FromClaudeToChatGPT.md`) left open, as a judgment call, whether a third
full-pipeline point is worth running to characterize the damping ratio's own shape (known so far only at
two points: 0.40791 at beta_A=0.2245, 0.46194 at beta_A=0.4172 — both closer to beta_B=0.5 giving a higher
ratio). This design picks it up.

## What's already known before this design (disclosed up front)

- Damping ratio at beta_A=0.2245: 0.40791 (isolated effect -0.61583, full-pipeline effect net of baseline
  -0.25121).
- Damping ratio at beta_A=0.4172: 0.46194 (isolated effect -0.20812, full-pipeline effect net of baseline
  -0.09614).
- Both existing points are between beta_A=0.2245 and beta_B=0.5 — no point exists further from 0.5 than
  0.2245, so the two known points don't establish whether the ratio keeps changing monotonically outside
  that range or plateaus/reverses.

## The design

Pick a **more extreme** beta_A value, further from beta_B=0.5 than either existing point, to extend the
known range rather than interpolate within it: **beta_A = 0.10**. Run both configurations needed to
compute a third damping-ratio point:
1. Coupling-only (no boundary-shift, no top-up) at beta_A=0.10, beta_B=0.5, same 3 pilot seeds — gives the
   isolated effect.
2. Full pipeline (coupling + boundary-shift-v2 + top-up) at beta_A=0.10, beta_B=0.5, same 3 pilot seeds —
   gives the full-pipeline effect (the anchor at beta_A=beta_B=0.5 is already known: -0.05575, no need to
   rerun it).

Damping ratio = (full-pipeline effect − anchor) / (isolated effect − coupling-only-uniform-baseline).

## What has NOT been done before this design (result-blinding)

**beta_A=0.10 has never been run in either configuration.** Both isolated and full-pipeline effects at
this value are unknown at the time of writing.

## Predicted outcome, stated before running

The two known points (0.40791 at 0.2245, 0.46194 at 0.4172) suggest the damping ratio rises as beta_A
moves *toward* 0.5 (a milder manipulation is damped less, proportionally). Extrapolating that same
direction outward, beta_A=0.10 (more extreme, further from 0.5) is predicted to give a **lower** damping
ratio than 0.40791 — roughly **0.30–0.38**, extrapolating the two-point trend's rough slope. If instead the
ratio at 0.10 comes back *higher* than 0.40791, or reverses direction, that would mean the relationship is
not simply monotonic in |beta_A − beta_B| and would need a genuinely different characterization (e.g. a
U-shape or a threshold effect) rather than a smooth trend.

## Honesty precommitment

Whatever the third point's damping ratio is — extending the existing trend, reversing it, or landing
somewhere that doesn't cleanly fit either story — is reported exactly as measured, including if it
contradicts the predicted 0.30–0.38 range above.
