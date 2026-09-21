# Hybrid shift+substitution novelty null: preregistered mechanism-control result (INVALID_CONSTRUCTION, close miss on calibration, order is the persistent wall)

Protocol: `data/external/hybrid-shift-substitution-novelty-null-manifest-v1.json`, solo Claude design (ChatGPT not automated; self-review in `logs/2026-09-21-claude-hybrid-shift-substitution-selfreview.md`). First design to deliberately combine two previously-tested mechanisms: boundary-shift (PR #34, entropy-invariant but capped near 64% hapax) run at its own established maximum, topped up by a small amount of bigram-conditional character substitution (PR #30's mechanism) to close the remaining hapax gap cheaply.

**Frozen verdict: INVALID_CONSTRUCTION** — close, not comfortable. The novelty manipulation check requires `hybrid_novelty_only` to pass the hapax criterion in ≥16/20 seeds; it passed in **14/20**. Every one of the 20 seeds showed a hapax *increase* over baseline (`paired_hapax_increase: 20/20`), and the hapax range was 0.6447–0.6582 — essentially all 20 seeds clustered right around the 0.65 floor, with roughly a third falling just under it by chance. This is a calibration-precision issue (nu_sub=0.02 was calibrated on a 3-seed pilot mean of 0.6543, too close to the floor to guarantee margin across 20 seeds), not evidence the hybrid approach doesn't work.

**Per this design's own explicit precommitment, nu_sub is not being retuned now that the full-scale outcome is known** — that would be exactly the outcome-driven parameter selection this project's discipline forbids. This result is reported as INVALID_CONSTRUCTION, honestly, and a properly-margined recalibration would need its own preregistration.

## Result

| Configuration | N | H1 | H2 | Units | Order | Hapax | Edge | Joint pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline [reused] | 20 | 3.984 | 2.711 | 20/20 | 1.30% | 39.4% | -0.002 | 0/20 |
| edge_only [reused] | 20 | 3.992 | 2.731 | 16/20 | 1.10% | 51.3% | +0.379 | 0/20 |
| hybrid_novelty_only [nu_shift=1.0, nu_sub=0.02, beta=0] | 20 | 3.986 | 2.735 | 20/20 | 2.17% | 65.2% | +0.107 | 0/20 |
| **primary** [nu_shift=1.0, nu_sub=0.02, beta=0.5] | 20 | **3.994** | **2.753** | **19/20** | 2.45% | **70.9%** | **+0.487** | **0/20 (order alone)** |

Required bands: H1 3.9763±0.15, H2 2.6897±0.15, unit-scale minimum at 32/64 merges with k64 gap in [0.90, 1.20], **order share [0%, 2.0%]**, edge gain ≥0.15 bits/boundary with ≥15/16 positive blocks, hapax ≥65%.

## Per-criterion pass counts, primary configuration (n=20)

**H1: 20/20 | H2: 20/20 | units: 19/20 | edge: 20/20 | hapax: 20/20 | order: 0/20**

This is the strongest joint result of any design tried in this project — five of six criteria pass essentially perfectly at the primary configuration (with coupling active, dosage above the manipulation-check calibration point). Only token-order-share fails, and it fails by a wide, consistent margin (mean 2.45%, required ≤2.0%).

## Interpretation

**The hybrid approach works exactly as hypothesized for entropy and vocabulary.** H2 at the primary configuration (2.753) sits comfortably inside the required band, far from the failures seen in every substitution-only design (2.925–2.997 across bigram/budget-capped/move-reuse). H1, edge, and hapax all pass cleanly. This confirms the core idea: letting boundary-shift absorb most of the vocabulary-growth burden for free, with substitution handling only a small residual gap, keeps the combined entropy cost far below what substitution alone requires to reach the same hapax level.

**But two real problems remain, and neither is solved by this result.**

1. **The manipulation check's near-miss is a calibration problem, not a discovery.** `hybrid_novelty_only`'s hapax values cluster tightly around the 0.65 floor (0.6447–0.6582), meaning the pilot's 3-seed mean (0.6543) didn't carry enough margin for the full 20-seed distribution. A properly-margined recalibration (targeting a mean further into the band, or using more pilot seeds for a tighter estimate) would very plausibly clear 16/20 — but this report does not make that claim by retuning nu_sub now; that would need its own preregistration, run fresh.
2. **Token-order-share is a persistent, unaddressed wall.** It fails by a wide margin in `hybrid_novelty_only` (2.17%, required ≤2.0%) and in `primary` (2.45%) — both close to boundary-shift-novelty-null's own order failure (2.27% shift-only, 2.53% primary, from PR #34). Adding the small substitution top-up did not materially change this. **Even a properly-recalibrated nu_sub that clears the hapax manipulation check would still not produce a PASS, because order would still fail.** This is the real remaining scientific question, not calibration precision.

**A plausible, undiagnosed explanation for the order failure, offered as a hypothesis**: every successful boundary-shift creates a `(left, right)` token pair where `right` is a deterministic function of `left` and the shift's chosen split point — the two output tokens are, by construction, more tightly statistically linked to each other than an arbitrary adjacent pair would be. If this linkage is strong and common enough across the corpus, it could inflate a whole-token order-prediction statistic even without either piece recurring often. This has not been directly verified (would need inspecting the order metric's internals against the shift-created pairs specifically) and is not claimed as established.

**Net effect on the project's mechanism-test record**: this is the first design to solve H1, H2, edge, and vocabulary openness simultaneously and comfortably (not just narrowly) — a genuine advance over every substitution-only design. It sharpens the open question to two separable, now well-characterized problems: (a) a calibration-precision gap on hapax, straightforward to fix with a properly-margined recalibration, and (b) a structural order-share excess specific to the boundary-shift mechanism, not yet understood or addressed by any design tried. **This does not identify a mechanism or bear on meaning.**

## Provenance and execution

- Design and solo self-review: `logs/2026-09-21-claude-hybrid-shift-substitution-selfreview.md`, including an explicit precommitment not to retune nu_sub after seeing the outcome, honored in this report.
- nu_sub calibrated via a 3-seed, self-consistency-only, hapax-only pilot; frozen at nu_sub=0.02, the smallest tested value with a pilot-mean hapax in-band — in hindsight too close to the floor to carry margin across 20 seeds, disclosed as a real limitation of the calibration procedure, not hidden.
- Implementation: `data/scripts/external_hybrid_shift_substitution_novelty_null_audit.py`, combining `apply_boundary_shift` (from PR #34) and the bigram-conditional substitution mechanism (from PR #30) as two sequential passes. `baseline`/`edge_only` reused by reference (same file used by every design since boundary-state-null).
