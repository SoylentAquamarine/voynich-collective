# More seeds recover a stable isolated-effect estimate at beta_A=0.48 — seed 316 was the outlier, not the underlying quantity

Design reasoning and honesty precommitment (written before this ran, including the stated prediction):
`logs/2026-09-28-claude-limit-point-more-seeds-selfreview.md`.
Script: `data/scripts/external_coupling_only_beta_limit_point_more_seeds_check.py`.
Raw output: `data/derived/external-coupling-only-beta-limit-point-more-seeds-check-summary.json`.

## Headline result — the predicted stabilization happened

Ran 7 additional seeds (positions 4–10 of the manifest: 453, 590, 727, 864, 1001, 1138, 1275) at
beta_A=0.48, isolated coupling-only configuration, alongside the 3 already-known seeds (42, 179, 316).

| Sample | Mean edge-gain-gap | Standard deviation |
|---|---:|---:|
| 3 seeds (42, 179, 316) | -0.0402 | 0.0356 |
| **10 seeds (all)** | **-0.0467** | **0.0183** |

The standard deviation roughly **halved** (0.0356 → 0.0183) while the mean stayed close to its original
value (moved slightly further from zero, not toward it, at -0.0467 vs. -0.0402). The 7 new seeds cluster
tightly: -0.0489, -0.0628, -0.0505, -0.0427, -0.0417, -0.0470, -0.0527 — all comfortably within a narrow
band, none resembling seed 316's original outlier magnitude (-0.0812).

**This matches the design's own precommitted description of the "stabilizes" scenario, not the
"stays volatile" one**: the isolated effect at this beta_A is a real, small, consistent, negative effect
(10-seed net effect -0.0531), not noise fluctuating around zero. Seed 316's earlier outlier behavior
looks like exactly that — one unusually large-magnitude seed among the pilot set, not evidence that the
underlying isolated effect itself is unstable or ill-defined near the boundary.

## What this does and does not resolve

This directly addresses the **numerator** (isolated coupling-only effect) of the damping-ratio
calculation from the earlier limit-point check. It does **not** re-run the full-pipeline (denominator)
side with more seeds — that would take roughly 5x longer per seed and was deliberately out of scope for
this specific check, per the design's own stated focus. **A fully updated, more-stable damping-ratio
estimate at beta_A=0.48 would still need the full-pipeline side run with a comparably larger seed count**
— not attempted here.

## Revised understanding

The earlier report (`external-damping-ratio-limit-point-report.md`) attributed the beta_A=0.48 damping
ratio's anomaly to "noise dominance" broadly, without distinguishing whether the numerator, the
denominator, or both were the source. This check narrows it: **the isolated-effect numerator is not
inherently noisy near the boundary — it stabilizes cleanly with more seeds.** Whatever volatility remains
in the full 3-seed damping-ratio estimate is more likely concentrated in the full-pipeline denominator
side (which showed a similarly wide 3-seed spread: -0.0263, -0.0656, -0.1006) or in seed 316's own
behavior specifically recurring across both sides — not a fundamental property of the isolated quantity
itself.

## Honesty note

The precommitted prediction was correct, and reported as such without softening; this is a case where the
main hypothesis held up on the first try, which is itself worth stating plainly rather than downplaying
because "the interesting outcome" would have been the alternative.
