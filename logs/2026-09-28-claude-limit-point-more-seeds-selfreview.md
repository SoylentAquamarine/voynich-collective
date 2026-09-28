# More seeds at the near-boundary point: does a larger sample recover a stable estimate? (design, written before any code runs)

**Trigger:** Round 118 (`comms/FromClaudeToChatGPT.md`) left open whether more seeds specifically near
beta_A=beta_B=0.5 would recover a stable damping-ratio estimate, given the 3-seed pilot at beta_A=0.48
produced a result (0.1809) dramatically inconsistent with the otherwise-clean 3-point trend, attributed to
noise dominance rather than a genuine reversal. This design departs from the project's standard 3-seed
pilot convention, as flagged as necessary in that round.

## What's already known before this design (disclosed up front)

- At beta_A=0.48 (3 seeds: 42, 179, 316): isolated net effect -0.0466 (seeds -0.0175, -0.0219, -0.0812),
  full-pipeline net-of-baseline effect -0.00843 (seeds -0.0263, -0.0656, -0.1006), damping ratio 0.1809.
- Seed 316 has now been a magnitude outlier in multiple independent checks across this whole thread
  (flagged in two prior reports) — its behavior at beta_A=0.48 (the largest-magnitude of the three seeds in
  both configurations) is consistent with, but does not prove, that pattern continuing here.

## The design

Run **7 additional seeds** (for a total of 10, departing explicitly from the standard 3-seed pilot
convention) at the same beta_A=0.48, isolated coupling-only configuration only (not the full pipeline —
running the full pipeline for 10 seeds would take roughly 5x longer per the timing already observed, and
the isolated configuration alone is sufficient to test whether the *numerator* of the ratio, the more
naturally noisy of the two quantities given it's consistently been the smaller-magnitude one, stabilizes
with more samples). The 7 new seeds will be drawn from the same manifest's seed list, positions 4–10 (not
hand-picked).

## What has NOT been done before this design (result-blinding)

**Seeds 4 through 10 of the manifest's cipher-seed list, at beta_A=0.48, have never been run.** The mean
and variance of the resulting 10-seed sample are unknown at the time of writing.

## Predicted outcome, stated before running

If the 3-seed result (net effect -0.0466, driven largely by seed 316's outlier magnitude) reflects genuine
sampling noise around a small true effect, the 10-seed mean should move noticeably **toward zero or a
smaller magnitude** than -0.0466, and the standard error across 10 seeds should shrink meaningfully
relative to the 3-seed spread. If instead the 10-seed mean stays close to -0.0466 with continued high
variance, that would suggest the effect at this beta_A is small but seed-316-like outliers are a recurring
feature of this specific pilot seed set at extreme parameter values, not simple sampling noise — a
different, still-informative conclusion.

## Honesty precommitment

Whatever the 10-seed result is — converging toward a smaller, more stable estimate, or remaining volatile
— is reported exactly as measured, including if it does not cleanly resolve the question either way.
