# 2026-09-22 — Precommitment: checking BPE dependence-gap curve SHAPE, not just checkpoint location

Session: by Claude, solo. A structurally different criterion-(b) check than the scalar corpus statistics tested in PR #43/#45 — this checks a *shape*, not a single number.

## Why this is genuinely different from the statistics already tested

The six frozen criteria only constrain two narrow facts about the BPE dependence-gap curve: where its minimum falls (`bpe_minimum_checkpoint` in {32, 64}) and the magnitude of the gap at 64 merges (`k64_gap` in [0.90, 1.20]). They say nothing about the curve's *shape* — its values at 0 and 16 merges, or how steeply it falls and rises around the trough. A mechanism can satisfy both frozen constraints while having a curve shape that looks nothing like real Voynich's own measured curve. This has never been checked for either frozen mechanism.

**Already-existing, unrelated-purpose source**: the full held-out-quire curve for real Voynich (0 / 16 / 32 / 64 merges: 1.686 / 1.423 / 1.379 / 1.490 bits) was published in `data/derived/external-units-paper-audit.md` on 2026-09-19, reproducing an external paper's own finding — a full year before either frozen mechanism existed, for a completely different purpose (verifying someone else's published numbers, not designing or evaluating a generator).

## Non-circularity

Neither `boundary-shift-v2` nor `hybrid-shift-v2-substitution` was ever calibrated against the curve's *shape* — only against the checkpoint location and the k64 gap magnitude, both already-published in the six criteria before either design existed.

## Methodology check, before trusting the comparison

`battery()` (the shared evaluation function every mechanism-test script in this project calls) computes a full `bpe["curve"]` internally, but no prior script has ever extracted or reported values other than the checkpoint location and the k64 gap. Before comparing any mechanism's curve against the external paper's separately-published reference values, this script reproduces real Voynich's own curve directly through the same `battery()` call every mechanism uses — the same sanity-check discipline already applied to the Zipf slope and word-length checks, precisely because a representation or methodology mismatch was found for word-length and could recur here.

## Precommitment

Reported plainly regardless of outcome. A shape mismatch is not grounds to redesign either mechanism to chase it — that would recreate the statistic-targeting problem this whole line of work exists to avoid.
