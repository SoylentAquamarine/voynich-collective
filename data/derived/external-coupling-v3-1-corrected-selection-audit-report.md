# coupling-v3.1 (isolation-aware beta selection) result: PASS, validly attributed

Frozen design: `data/external/coupling-v3-1-corrected-selection-manifest-v1.json`.
Self-review: `logs/2026-09-25-claude-coupling-v3-1-selfreview.md` (design reasoning, written before
any code ran this cycle). Execution log: `logs/2026-09-25-claude-coupling-v3-1-execution.md`.
Script: `data/scripts/external_coupling_v3_1_corrected_selection_audit.py`. Raw output:
`data/derived/external-coupling-v3-1-corrected-selection-audit-summary.json`.

## Headline result

**Primary verdict: PASS.** Correcting `coupling-v3`'s selection defect — selecting beta on
coupling's *isolated* `edge_only` contribution instead of the combined mechanism's gain — produces
a beta (0.15) at which the boundary manipulation check **passes 20/20**, and the full combined
mechanism passes all six frozen criteria in all 20 primary replicates, with H2 headroom
(0.0311 bits below the 2.8397-bit tolerance ceiling) **3.7x larger than `coupling-v2`'s own
headroom (0.0083 bits)** — a real, validly-attributed improvement, not the inflated 6x that
`coupling-v3`'s invalidated selection produced.

| Stage | n | Edge gain (bits/boundary) | Edge criterion pass | Boundary check |
|---|---:|---:|---:|---|
| `baseline` (no coupling) | 20 | -0.0018 (mean) | 0/20 | — |
| `edge_only` (coupling alone, beta=0.15) | 20 | 0.1987 (mean, range 0.190–0.206) | 20/20 | **passes: 20/20 paired increase, 20/20 clear the floor** |
| `primary` (coupling + boundary-shift-v2 + substitution top-up, beta=0.15) | 20 | 0.7011 (mean, range 0.684–0.715) | 20/20 | (validated by the row above) |

## Pilot: where the isolated edge_only signal actually starts clearing the floor

3 pilot seeds per beta, measuring `edge_only` (coupling alone) directly rather than the combined
mechanism used by `coupling-v3`'s (invalidated) pilot:

| beta | edge_only mean (bits/boundary) | clears 0.15 floor |
|---:|---:|---|
| 0.10 | 0.1140 | No |
| **0.15** | **0.1927** | **Yes — selected (lowest qualifying)** |
| 0.20 | 0.2846 | Yes |
| 0.25 | 0.3811 | Yes |
| 0.30 | 0.4822 | Yes |
| 0.35 | 0.5883 | Yes |
| 0.40 | 0.7009 | Yes |
| 0.45 | 0.8159 | Yes |

Note the close agreement between this cycle's beta=0.10 pilot value (0.1140) and `coupling-v3`'s
own 20-seed `edge_only` result at beta=0.10 (0.1168, `data/derived/external-coupling-v3-lower-beta-audit-summary.json`)
— a useful cross-check that the two scripts' coupling implementation is identical and the earlier
failure was a selection-rule defect, not a coding discrepancy.

## Full primary-stage numbers (20 replicates each)

| Metric | `edge_only` (beta=0.15) | `primary` (beta=0.15, combined) | `coupling-v2` primary (beta=0.5, PR #71, for comparison) |
|---|---:|---:|---:|
| H1 (bits) | 3.988 mean | 3.988 mean | ~3.99 |
| H2 (bits) | 2.795 mean | 2.800 mean (max 2.809) | 2.831 mean (max 2.8383) |
| H2 headroom to ceiling (2.8397) | — | **0.0311 (min case)** | 0.0083 |
| k64 BPE gap | 1.041 mean | 0.963 mean | in [0.90, 1.20] |
| token-order share | 0.0096 mean | 0.0131 mean | in [0.0, 0.02] |
| hapax share of types | 0.496 mean | 0.925 mean | ~0.922–0.927 |
| edge gain (bits/boundary) | 0.199 mean | 0.701 mean | ~0.99 mean |
| all-six-criteria pass | n/a (not evaluated against all six) | **20/20** | 20/20 |

## Interpretation

This is the **third** independently-designed mechanism to validly pass the project's frozen
six-criterion joint profile (after `boundary-shift-v2` and `coupling-v2`), and the first to do so
with a materially larger, *validly attributed* H2 margin than `coupling-v2`'s own thin 0.0083-bit
headroom. The improvement (0.0311 vs 0.0083, ~3.7x) is real but more modest than the 0.0510-bit
figure `coupling-v3` reported at beta=0.10 — because that figure came from a beta whose apparent
edge pass was not actually attributable to coupling. This result is smaller but trustworthy where
that one was larger but invalid.

Edge-gain overshoot versus Voynich's own real measured value (~0.174–0.187 bits/boundary,
`data/derived/external-naibbe-audit-report.md` and `data/derived/external-hybrid-shift-coupling-v2-substitution-novelty-null-audit-report.md`)
is also somewhat reduced: `primary`'s
0.701-bit mean is roughly 3.9x the real value, versus `coupling-v2`'s ~5.5–6x overshoot at beta=0.5 —
still a real, disclosed mismatch in magnitude, not resolved, but smaller in the same direction the
lower-beta motivation predicted.

**This does not identify a mechanism or bear on the manuscript's meaning.** Like every other
constructive-null result in this project's history, it is evidence about what the frozen six-number
profile can and cannot discriminate (see `methods/falsification-standard.md`'s constructed-null
disqualification clause), not evidence about Voynichese's actual origin. `coupling-v2` (beta=0.5,
PR #71) remains unchanged and independently valid; this result sits alongside it as a second,
lower-beta member of the same family, both now validly attributed.

## What this unblocks, not yet attempted

`logs/2026-09-23-claude-section-aware-coupling-v2-declined.md` declined a section-varying-dosage
extension of `coupling-v2` specifically because its H2 headroom (0.0083 bits) was too thin to move
`nu_sub` by Currier section without breaching the ceiling. This design's validly-attributed 0.0311-bit
headroom at beta=0.15 is meaningfully larger — whether it is *enough* headroom for a section-aware
attempt to construct the real Currier A/B asymmetry (as PR #39's diagnostic did for a different,
higher-headroom base mechanism) is untested and not claimed here. That remains a distinct, separately
scoped next step requiring its own fresh precommitment, consistent with this project's standing
discipline against chaining an untested next step onto the same cycle's momentum.

## What this does not do

Does not identify a mechanism, bear on meaning, or change any Confirmed Finding about Voynichese
itself. Does not retry any other beta from this cycle's grid (0.20 upward all clear the floor but
were not selected, per the manifest's "lowest qualifying" rule — trying a higher beta post-hoc
without a fresh precommitment would be exactly the result-directed re-selection this project's
honesty precommitments exist to prevent). Does not attempt section-varying beta or `nu_sub` — named
above as the next open step, not started here.
