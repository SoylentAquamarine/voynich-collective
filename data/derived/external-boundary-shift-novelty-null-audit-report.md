# Boundary-shift novelty null: preregistered mechanism-control result (INVALID_CONSTRUCTION, with a striking pattern worth reporting carefully)

Protocol: `data/external/boundary-shift-novelty-null-manifest-v1.json`, solo Claude design (ChatGPT not automated; self-review in `logs/2026-09-21-claude-boundary-shift-novelty-selfreview.md`). Structurally different from the five-design substitution sequence just synthesized into the knowledge base: this mechanism never substitutes a character — it only moves where the token boundary falls between an adjacent pair of tokens, conserving the exact character multiset.

**Frozen verdict: INVALID_CONSTRUCTION.** The novelty manipulation check fails: `boundary_shift_only` (the isolated shift mechanism, no coupling) tops out at 63.8% mean hapax even at nu=1.0 (the maximum possible dosage) — never clearing the required 65% floor, so `hapax_criterion_pass = 0/20`. Per the frozen verdict rule, this makes the primary result **uninterpretable**, not a pass or fail on its own terms.

**But the primary configuration's raw numbers show a pattern not seen in any of the five substitution designs, and it needs to be reported plainly rather than buried by the technical verdict**: in the primary configuration (shift + coupling together), **all 20 of 20 replicates pass H1, H2, learned-unit scale, edge prediction, and hapax jointly** — the first time this project has seen five of six criteria pass in every single replicate. The sole failure is token-order-share (2.3–2.8% vs. the required ≤2.0% ceiling), clearly attributable to the shift operation specifically (`boundary_shift_only` alone already pushes order to 2.27%, while `edge_only`, coupling alone, actually reduces it slightly from baseline's 1.30% to 1.10%).

## Result

| Configuration | N | H1 | H2 | Units | Order | Hapax | Edge | Joint pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline [reused] | 20 | 3.984 | 2.711 | 20/20 | 1.30% | 39.4% | -0.002 | 0/20 |
| edge_only [reused] | 20 | 3.992 | 2.731 | 16/20 | 1.10% | 51.3% | +0.379 | 0/20 |
| boundary_shift_only [nu=1.0, beta=0] | 20 | 3.984 | 2.711 | 20/20 | 2.27% | 63.8% | +0.112 | 0/20 |
| **primary** [nu=1.0, beta=0.5] | 20 | 3.992 | 2.732 | 20/20 | 2.53% | 70.3% | +0.499 | **0/20 (all fail on order alone)** |

Required bands: H1 3.9763±0.15, H2 2.6897±0.15, unit-scale minimum at 32/64 merges with k64 gap in [0.90, 1.20], **order share [0%, 2.0%]**, edge gain ≥0.15 bits/boundary with ≥15/16 positive blocks, hapax ≥65%.

## Per-criterion pass counts, primary configuration (n=20)

H1: **20/20** | H2: **20/20** | units: **20/20** | edge: **20/20** | hapax: **20/20** | order: **0/20** (range 2.28%–2.76%, never close to the 2.0% ceiling in any replicate)

## Interpretation

**The exact H1/H2 invariance is a real, provable, and confirmed mechanistic property — not an approximation.** Because boundary-shift never adds, removes, or substitutes a character, only regroups the same characters across a moved internal boundary, `boundary_shift_only`'s H1 is bit-identical to baseline's (diff = 0.0 to full floating-point precision) and H2 is likewise unchanged to four decimal places across every dosage tested from nu=0.1 to 1.0. This is the first design in this project's mechanism-test history where entropy simply cannot fail, at any dosage — a genuinely different category of result from the five substitution designs, all of which traded entropy against vocabulary openness.

**But the mechanism cannot generate enough vocabulary on its own to be valid.** Diagnosed directly: at nu=1.0 only ~2,675 real shift events occur across an ~80,000-token stream, far below what a naive eligible-pair count would suggest (~38,000). The bottleneck is not search failure (a check found the required "both pieces unseen" search succeeds ~99.5% of the time it's attempted) — it's a structural self-limiting supply problem: each successful shift consumes its two source tokens' future eligibility while rarely producing pieces likely to recur and become eligible again, so the pool of eligible pairs shrinks as the mechanism runs, independent of nu. This is why the pilot's calibration rule (land in [0.65,0.75] hapax) could never be satisfied even at the maximum possible dosage — disclosed honestly in the self-review log before this run, not discovered after.

**Why the primary configuration's striking numbers do not rescue the result, and should not be read as "nearly passing."** Coupling alone (`edge_only`) reaches only 51.3% hapax; shift alone reaches 63.8%. Combined, primary reaches 70.3% — comfortably over the floor. This could reflect a real synergy between the two operations, or it could be an artifact of confounding that the manipulation-check discipline exists specifically to catch: because `boundary_shift_only`'s own isolated contribution already fails the manipulation check, there is no valid baseline to attribute primary's hapax pass to the shift mechanism working as intended versus some other interaction. The frozen rule treats this correctly as uninterpretable, and this report does not dispute that verdict.

**What is genuinely new and worth carrying forward, independent of the INVALID verdict**: token-order-share is the limiting criterion here, the only time in six mechanism-tests this project has run that order — not H2, not entropy — is what fails, and it fails cleanly and by a wide, unambiguous margin (every replicate at least 0.28 percentage points over the ceiling). A shift operation that creates a genuinely fresh two-token adjacency relationship every time it fires is a plausible, disclosed explanation: it directly manufactures new local whole-token structure, which is exactly what the token-order-share criterion measures. This is a mechanistically different failure mode from anything seen before, and worth keeping in mind for any future non-substitution vocabulary-opening design.

**This does not identify a mechanism or bear on meaning, and does not show a valid boundary-shift design is impossible** — only that this specific, simplest formulation (shift alone, no help from any other operation) cannot reach the hapax floor unassisted. A version with a richer matching rule (not just adjacent pairs, or not requiring both pieces to differ from the original split point) was not tested and would need its own preregistration.

## Provenance and execution

- Design and solo self-review: `logs/2026-09-21-claude-boundary-shift-novelty-selfreview.md`, including two rejected earlier formulations (a split-only design needing cross-stream "debt" tracking, rejected for bug-risk) and a full account of the pilot's calibration failure, disclosed before any primary outcome was computed.
- Implementation: `data/scripts/external_boundary_shift_novelty_null_audit.py`. `baseline`/`edge_only` reused by reference (same file used by all prior designs).
- H1-invariance verified programmatically as part of the frozen run, not just the pilot: `h1_invariance_diff = 0.0`.
