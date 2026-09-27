# Third damping-ratio point confirms the monotonic trend, and surfaces a new boundary condition

Design reasoning and honesty precommitment (written before this ran, including the stated prediction):
`logs/2026-09-27-claude-damping-ratio-third-point-selfreview.md`.
Scripts: `data/scripts/external_coupling_only_beta_third_point_check.py`,
`data/scripts/external_coupling_v2_third_point_full_pipeline_check.py`.
Raw output: `data/derived/external-coupling-only-beta-third-point-check-summary.json`,
`data/derived/external-coupling-v2-third-point-full-pipeline-check-summary.json`.

## Headline result

**The predicted range was hit almost exactly.** At beta_A=0.10 (more extreme than either prior point,
further from beta_B=0.5): isolated net effect -0.8324, full-pipeline net-of-baseline effect -0.3129,
**damping ratio = 0.3759** — within the precommitted predicted range of 0.30–0.38.

| beta_A | Distance from beta_B=0.5 | Damping ratio |
|---:|---:|---:|
| **0.10 (new)** | 0.40 | **0.3759** |
| 0.2245 | 0.2755 | 0.40791 |
| 0.4172 | 0.0828 | 0.46194 |

**This confirms a clean, monotonic trend across three points, not just two**: the damping ratio rises as
beta_A approaches beta_B (a milder section-varying manipulation is proportionally damped less by
boundary-shift-v2 and the substitution top-up), and falls as beta_A moves further from beta_B (a more
extreme manipulation is damped proportionally more). This is now a real, three-point-supported
characterization within the tested range, not an assumption from two points.

## A new boundary condition, disclosed honestly

**Seed 316 failed the six-criterion pass at this more extreme beta_A** (`all_six_pass=False`), the first
time any section-varying-beta design in this thread has failed a criterion at any seed. The other two
seeds (42, 179) still passed. This was not predicted or discussed in the selfreview log, since the design
question was about the damping ratio's shape, not the six-criterion pass rate — it's an honest,
unanticipated side observation, not swept aside. **Practical implication**: beta_A=0.10 is likely too
extreme a manipulation to use directly as a candidate design (even setting aside that it wasn't chosen to
target the real gap) — this is useful information for ruling out the far end of the range, not just for
characterizing the damping-ratio curve.

## What remains open

Whether the damping ratio's rise continues smoothly all the way to beta_A=0.5 (where it would need to
approach some limiting value, since the isolated effect itself approaches zero there) or has a different
shape very close to 0.5, is untested — the closest point so far (0.4172) is still 0.083 away from 0.5. Not
attempted here. The six-criterion failure at beta_A=0.10 for one seed also raises a new, unexplored
question — which specific criterion failed and why — not investigated in this check, which only computed
the damping ratio.
