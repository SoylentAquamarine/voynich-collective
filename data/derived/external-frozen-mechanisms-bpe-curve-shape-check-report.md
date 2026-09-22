# Criterion-(b) check: BPE dependence-gap curve SHAPE

Precommitment: [`logs/2026-09-22-claude-bpe-curve-shape-precommitment.md`](../../logs/2026-09-22-claude-bpe-curve-shape-precommitment.md), written before this script ran.
Script: [`data/scripts/external_frozen_mechanisms_bpe_curve_shape_check.py`](../scripts/external_frozen_mechanisms_bpe_curve_shape_check.py)
Summary data: [`external-frozen-mechanisms-bpe-curve-shape-check-summary.json`](external-frozen-mechanisms-bpe-curve-shape-check-summary.json)

## What this checks

The six frozen criteria constrain only two facts about the BPE dependence-gap curve: where its minimum falls (`bpe_minimum_checkpoint` in {32, 64}) and the k64 gap magnitude (in [0.90, 1.20]). Neither frozen mechanism (`boundary-shift-v2`, `hybrid-shift-v2-substitution`) was ever calibrated against the curve's full *shape* — its values at every other checkpoint. This check computes the full 10-point curve (0/4/8/16/32/64/128/256/512/1024 merges) for both mechanisms (5 cipher seeds each) and compares it to real Voynich's own curve.

## Methodology check first — and a major discrepancy found

Before trusting any comparison, the script reproduced real Voynich's own curve directly through the same `battery()` call every mechanism-test script uses. That reproduction does **not** match the externally-published reference curve this precommitment cited (`data/derived/external-units-paper-audit.md`, held-out-quire methodology):

| merges | external paper's reference | this pipeline's own reproduction |
|---|---|---|
| 0 | 1.686 | 1.314 |
| 16 | 1.423 | 1.116 |
| 32 | 1.379 | 1.053 |
| 64 | 1.490 | 1.054 |

This is a **methodology-level mismatch, not just a representation difference** (unlike the word-length case in PR #45, where the gap was smaller and traceable to tokenization). The external paper's curve was computed on held-out quires with a different measurement procedure than this repo's `battery()` function. Because of this, **the external paper's curve is not a valid comparison basis here** — it is reported above for context only. The correct basis, per the same discipline used for the word-length and Zipf checks, is this pipeline's own reproduced real-Voynich curve, since that is what any mechanism's own curve (computed through the identical pipeline) can be fairly compared against.

## Mean curves (5 cipher seeds each)

| merges | real Voynich (this pipeline) | boundary-shift-v2 | hybrid-shift-v2-substitution |
|---|---|---|---|
| 0 | 1.314 | 1.542 | 1.537 |
| 4 | 1.348 | 1.406 | 1.371 |
| 8 | 1.274 | 1.363 | 1.289 |
| 16 | 1.116 | 1.188 | 1.271 |
| 32 | 1.053 | 1.136 | 1.235 |
| 64 | 1.054 | 1.104 | 1.159 |
| 128 | 1.179 | 1.287 | 1.236 |
| 256 | 1.554 | 1.625 | 1.518 |
| 512 | 2.212 | 2.220 | 2.023 |
| 1024 | 3.104 | 3.048 | 2.703 |

## Result

Mean absolute deviation from the real-Voynich curve, across all 10 checkpoints:

- **boundary-shift-v2: 0.082 bits** (mean relative deviation ~6.4%)
- **hybrid-shift-v2-substitution: 0.139 bits** (mean relative deviation ~9.9%)

`boundary-shift-v2` tracks the real curve's full shape substantially more closely than `hybrid-shift-v2-substitution` — about 40% lower mean absolute deviation. This holds well beyond the two checkpoints (32, 64) the frozen criteria actually constrain:

- At **k=512**, `boundary-shift-v2` is nearly exact: 2.220 vs. real 2.212 (0.35% off). `hybrid-shift-v2-substitution` is 2.023 (8.5% off, wrong direction — lower than real).
- At **k=1024**, `boundary-shift-v2` is close: 3.048 vs. real 3.104 (1.8% off). `hybrid-shift-v2-substitution` diverges more: 2.703 (12.9% off, same wrong direction — its curve collapses faster than real at high merge counts).
- At **k=16**, `boundary-shift-v2` is closer (6.5% off) than `hybrid-shift-v2-substitution` (13.9% off), even though both satisfy the frozen minimum-checkpoint criterion.

Both mechanisms share one common deviation: both overshoot the k=0 (character-level) gap by ~17% relative to real Voynich. This is not a distinguishing finding between the two mechanisms — it affects both equally and is not analyzed further here.

This is the second criterion-(b) statistic (after Zipf slope in PR #43) where `boundary-shift-v2` shows an unprompted match to real Voynich structure it was never calibrated against, while `hybrid-shift-v2-substitution` does not.

## What this does not show

This is one shape comparison on one derived statistic family (the BPE dependence-gap curve), evaluated against this pipeline's own reproduction of real Voynich — not the externally-published reference, which turned out to use a different methodology entirely. It does not by itself promote `boundary-shift-v2` to Active Hypotheses status; per `methods/falsification-standard.md`'s Constructed-null disqualification section, promotion requires independent historical attestation or a held-out prediction never used to guide the design sequence. This result strengthens the case that `boundary-shift-v2` (not `hybrid-shift-v2-substitution`) is the more promising branch to continue investigating for criterion-(b)-style evidence, consistent with the Zipf-slope finding in PR #43.

## Precommitment discipline

Both the sanity-check discrepancy and the shape-match result are reported as precommitted, regardless of outcome. No redesign of either mechanism was performed in response to this result — doing so would recreate the statistic-targeting problem this whole line of work exists to avoid.
