# Currier A/B construction diagnostic: section-varying dosage gets partway to the real asymmetry, not all the way

Diagnostic, not a preregistered mechanism test — direct follow-up to `external_currier_ab_diagnostic.py` (PR #38, merged), which found every homogeneous mechanism tested so far shows essentially zero A/B pooled-entropy asymmetry, versus Voynich's real +0.278 bits. That diagnostic's own stated limitation was that no tested design has any notion of "section" at all. This is the direct test: can a mechanism *built to try*, varying its dosage between Currier-A-labeled and Currier-B-labeled output, construct an asymmetry of comparable size?

## The test

Base mechanism: bigram-novelty-null's substitution transform (chosen over boundary-shift-v2, whose dosage parameter is proven exactly entropy-invariant and so could never move this statistic at all). Built a per-token Currier-label array in flat generation-stream order, from the same real per-line A/B labels used in the prior diagnostic (never fed into generation as content — used only to pick which of two dosages applies at each position). Ran the substitution mechanism with nu looked up per-token by section instead of one global value.

**Non-circularity discipline**: nu_A=0.3 and nu_B=0.1 are reused unchanged from bigram-novelty-null's own already-frozen sensitivity configurations (`stronger_novelty` and `weaker_novelty`), established in an earlier, unrelated design before this diagnostic existed — not chosen now to match this target's magnitude.

**One disclosed exception to full blindness**: assigning the *stronger* dosage to A rather than B was informed by real Voynich's known direction (A > B on this metric) plus the already-established fact that higher nu increases H2. That is a single binary choice informed by the real *direction*; the specific *magnitudes* (0.3, 0.1) were not tuned to the real *size* of the gap.

## Result

| | A | B | gap (A − B) | % of real gap |
|---|---:|---:|---:|---:|
| **Real Voynich** | 2.5198 bits | 2.2418 bits | **+0.2780 bits** | 100% |
| Section-varying (seed 42) | 2.3951 | 2.2851 | +0.1101 | 39.6% |
| Section-varying (seed 179) | 2.3876 | 2.2730 | +0.1146 | 41.2% |
| Section-varying (seed 316) | 2.3887 | 2.2810 | +0.1078 | 38.8% |
| Section-varying (seed 453) | 2.3829 | 2.2876 | +0.0953 | 34.3% |
| Section-varying (seed 590) | 2.3789 | 2.2746 | +0.1043 | 37.5% |
| **Section-varying mean** | 2.3866 | 2.2803 | **+0.1064** | **38.3%** |

Every replicate is positive (same direction as real) and tightly clustered (0.0953–0.1146 bits), reaching just over a third to two-fifths of the real gap's magnitude.

## Interpretation

**A mechanism built to try gets substantially, but not fully, toward the real asymmetry — using dosages it was never tuned to match.** This is a materially different result from the prior diagnostic's near-zero finding: giving a substitution mechanism any notion of "section" at all, even with off-the-shelf dosages borrowed from an unrelated design, recovers over a third of the real gap's size, consistently, across all five seeds.

**This is a partial result, not a reconstruction.** 38% of the real magnitude leaves the majority of the real gap unexplained by dosage variation alone at these specific, non-tuned values. It does not show the full +0.278-bit asymmetry is constructible; it shows dosage variation is a real, substantial contributor, not a false lead.

**This does not show the six-criterion profile and the A/B asymmetry are jointly constructible.** bigram-novelty-null's underlying substitution family does not pass the six frozen criteria at any dosage tested in this project — this diagnostic tested the A/B question in isolation, using the mechanism best suited to move that one statistic, not a candidate for the project's full six-criterion bar.

**What would be needed to test further, and why it wasn't done here**: larger dosage separation between sections might close more of the remaining gap, but testing that now — after seeing this result — would break the non-circularity discipline this run relied on. Any follow-up at different dosages should be framed and frozen as its own new test, not a retuning of this one.

## Dose-response follow-up: does recovered fraction scale with separation?

Motivated directly by the primary result leaving 62% of the gap unexplained: is dosage separation a small, saturating effect, or does it scale further? Ran one additional frozen configuration, decided and fixed *before* seeing its outcome: nu_A=0.5, nu_B=0.0 — a round-number extrapolation of the primary grid's separation (0.3/0.1 → 0.5/0.0), where 0.0 is the natural boundary of the dosage parameter (novelty substitution fully off for B), not a value reverse-fit to any target.

| Configuration | Separation | Mean gap | % of real gap |
|---|---:|---:|---:|
| Primary (nu_A=0.3, nu_B=0.1) | 0.2 | +0.1064 bits | 38.3% |
| Wide (nu_A=0.5, nu_B=0.0) | 0.5 | +0.3098 bits | **111.4%** (range 107.7%–113.9%) |

**Dosage separation is not a small, saturating effect — it scales past the real magnitude.** At the wider, still non-circularly-chosen separation, every one of 5 replicates *exceeds* Voynich's real +0.278-bit gap. This answers the section-aware feasibility question cleanly: yes, this one statistic (pooled A/B bigram-conditional entropy gap) is fully constructible in magnitude by dosage variation alone, given enough separation.

**What this does not show.** Matching one statistic's magnitude is not the same as a real candidate mechanism: nu_B=0.0 means B-labeled tokens get no novelty substitution at all, an extreme, not subtle, difference between sections — likely a large part of why the gap overshoots rather than lands near 100%. This says nothing about whether such a mechanism could also jointly pass the six frozen criteria (bigram-novelty-null's family doesn't, at any dosage tested in this project), and nothing about linguistic or historical plausibility for a real section-dependent process.

**Deliberately stopping at two points.** A natural next question is what separation lands closest to exactly 100% — but searching for that now, after seeing this result, would be exactly the retuning-to-target this whole design was built to avoid. Two frozen points, decided before their outcomes were known, are enough to establish the qualitative finding (separation scales, and can exceed real magnitude); pinning down a precise midpoint is not pursued here.

## Provenance

- Implementation: `data/scripts/external_currier_ab_construction_diagnostic.py`, reusing bigram-novelty-null's substitution mechanics exactly (only the per-token nu lookup is new), and the external repo's own line-parsing code for Currier labels (checksum-pinned commit `956a7c4...`, already verified throughout this project).
- Sanity-checked before trusting the comparison: reproduced the real Voynich A/B gap (+0.2780 bits) exactly matching the prior diagnostic's figure before interpreting the generated-data comparison.
- Full replicate data: `data/derived/external-currier-ab-construction-diagnostic-summary.json`.
