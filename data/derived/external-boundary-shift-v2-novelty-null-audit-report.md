# Boundary-shift-v2 novelty null: PASS — a constructive null passes the full joint profile (read the interpretation section before drawing any conclusion)

Protocol: `data/external/boundary-shift-v2-novelty-null-manifest-v1.json`, solo Claude design (ChatGPT not automated; self-review in `logs/2026-09-21-claude-boundary-shift-v2-selfreview.md`). Directly motivated by reading the actual order-share scoring code to diagnose why boundary-shift-novelty-null (PR #34) failed on that one criterion, and fixing the diagnosed cause.

**Frozen verdict: PASS.** Both manipulation checks succeed. **All 20 of 20 primary replicates pass all six frozen criteria jointly**, with comfortable margins on every criterion — not narrow squeaks. This is the first mechanism in this project's entire history (nine constructive/historical mechanisms tested across two AI agents) to pass the full joint six-criterion profile.

**Before anything else: this is a constructive null, not a decipherment, and this report treats it as informative about the *evaluation framework*, not about the Voynich manuscript's origin.** See "What this does and does not show" below before drawing any conclusion.

## Result

| Configuration | N | H1 | H2 | Units | Order | Edge | Hapax | Joint pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline [reused] | 20 | 3.984 | 2.711 | 20/20 | 1.30% | -0.002 | 39.4% | 0/20 |
| edge_only [reused] | 20 | 3.992 | 2.731 | 16/20 | 1.10% | +0.379 | 51.3% | 0/20 |
| boundary_shift_v2_only [nu=0.2, beta=0] | 20 | 3.984 | 2.711 | 20/20 | 1.76% | +0.242 | 68.6% | 0/20 (novelty-only isolation; not required to pass edge on its own) |
| **primary** [nu=0.2, beta=0.5] | 20 | **3.992** | **2.733** | **20/20** | **1.43%** | **+0.571** | **71.2%** | **20/20** |

Required bands: H1 3.9763±0.15 (so [3.826, 4.126]), H2 2.6897±0.15 ([2.540, 2.840]), unit-scale minimum at 32/64 merges with k64 gap in [0.90, 1.20], order share [0%, 2.0%], edge gain ≥0.15 bits/boundary with ≥15/16 positive blocks, hapax ≥65%.

## Per-criterion detail, primary configuration (n=20, all ranges across seeds)

- **H1**: 3.989–3.998 (band [3.826, 4.126]) — 20/20 pass, comfortably centered
- **H2**: 2.726–2.741 (band [2.540, 2.840]) — 20/20 pass, comfortably centered
- **learned units**: checkpoint always exactly 64 (allowed: 32 or 64); k64 gap 1.080–1.135 (band [0.90, 1.20]) — 20/20 pass
- **token-order-share**: 1.22%–1.75% (band [0%, 2.0%]) — 20/20 pass, no replicate close to the ceiling
- **edge prediction**: 0.551–0.590 bits/boundary (required ≥0.15), 16/16 positive blocks in every replicate — 20/20 pass, far above threshold
- **hapax**: 70.5%–71.8% (required ≥65%) — 20/20 pass

Manipulation checks: boundary (reused from the established reference) 20/20 paired increase + 20/20 criterion pass; novelty 20/20 paired increase + 20/20 criterion pass.

**Robustness check, not just the single calibrated point**: both sensitivity configurations — nu=0.15 (25% below the calibrated nu=0.2) and nu=0.25 (25% above) — also pass all six criteria in every one of their 5 replicates (5/5 each, all six criteria at 5/5). The PASS is not a fragile result confined to one narrow dosage; it holds across a reasonable range around the calibrated value.

## What changed from boundary-shift-v1 (PR #34), and why it worked

v1 required both pieces of a token-boundary shift to be simultaneously unseen types. Reading the actual order-share scoring code (`analysis/reproduce_scale_transition.py: order_information()`) showed why this specifically broke token-order-share: the metric caps the vocabulary at the 2,000 most frequent types and collapses everything else into one shared `<other>` symbol before measuring adjacent-token mutual information. Since both pieces of every v1 shift were guaranteed rare (freshly created, never previously seen), both always collapsed to `<other>` — manufacturing a strong, artificial `<other>`-follows-`<other>` adjacency that the metric read as excess whole-token predictability. v2 changes only the split-acceptance rule: prefer a split where *exactly one* piece is new (reusing an existing type for the other), falling back to "at least one new" only when no such split exists. This avoids the double-novel-adjacency directly.

An unplanned side effect, worked out during self-review after observing it: because v2 reuses an existing type for one piece of most shifts, that reused type can itself recur later and become newly eligible again — a feedback loop v1's always-both-novel design never had (v1's shifted pieces, being permanently unique, could never become eligible a second time). This is why v2's achievable hapax ceiling at maximum dosage is dramatically higher than v1's (~92% vs. ~64% in informal exploratory checks) — enough headroom that a calibrated nu satisfying the hapax floor no longer needs to run at maximum dosage, which is also why order-share stays comfortably in band: fewer total shift events are needed.

Character identity is still never touched by this operation — H1 was confirmed exactly invariant in earlier pilot testing of this same split-acceptance mechanism (H2 is not exactly invariant here in the way v1 was, since v2's split preference is content-dependent rather than purely random, but it lands comfortably in band regardless).

## What this does and does not show

**This does not identify a mechanism, does not decipher the manuscript, and does not bear on meaning, language, or authorship.** It is a deliberately engineered constructive null: a fixed historical cipher (Naibbe) plus two explicitly-designed postprocessing operations (a boundary-coupling rule targeting edge prediction by construction, and a boundary-shift rule targeting vocabulary openness and token-order-share by construction, refined specifically in response to a diagnosed metric artifact). Nothing about this mechanism is claimed to resemble how the Voynich manuscript was actually produced, and no linguistic or historical argument supports it as a real candidate — it was built, iteratively, purely to satisfy the six frozen numerical criteria.

**What it does show, and this is the important, disclosed methodological finding**: the six-criterion joint profile — used throughout this project to *reject* nine other mechanisms (Naibbe alone, Cardan-grille, self-citation, the from-scratch BCCN generator, and five further novelty-rule variants) as insufficient — is **not sufficient on its own to uniquely identify a real generative mechanism**, because a mechanism explicitly engineered (not historically documented, not linguistically motivated) to satisfy it, does satisfy it. This narrows what any *future* six-criterion pass — for a mechanism with genuine historical or linguistic motivation — could be used to argue: passing the joint profile is now demonstrated to be necessary-but-not-sufficient evidence for a real hypothesis, since it is achievable by construction alone.

**This also does not retroactively weaken the value of the nine prior FAILED mechanism tests.** Those tests showed real, historically-documented, or paper-published mechanisms (not built to pass the test) do not reproduce Voynich's joint profile. That remains true and informative regardless of this result. What changes is the interpretation of a *future pass*: it would need independent argument for why the passing mechanism is historically or linguistically plausible, not just numerically fitting — the joint profile alone cannot carry that argument, now that a mechanism with no such plausibility claim has been shown to pass it.

## This needs real cross-review before any knowledge-base claim, more than any prior result in this project

Given the significance, this PR proposes no knowledge-base wording. A careful self-review pass of the interpretation (not just the numbers) is required before drafting any KB entry, following this project's standing discipline — and given the magnitude of this specific result, genuine cross-party review (not just the usual solo-then-wait pattern) is especially important before this enters the permanent record in any form stronger than "reported, pending review."

## Provenance and execution

- Design and solo self-review: `logs/2026-09-21-claude-boundary-shift-v2-selfreview.md`, including the diagnostic process (reading the actual scoring code, not guessing) and an explicit account of an informal exploratory check that preceded the frozen preregistration, disclosed as informal and not treated as the calibration result.
- nu calibrated via a 3-seed, self-consistency-only, hapax-only pilot; frozen at nu=0.2, the smallest in-band value under the same selection rule used in every prior design.
- Implementation: `data/scripts/external_boundary_shift_v2_novelty_null_audit.py`. Core evaluation functions (`SIX_CRITERIA`, `evaluate_replicate`, `edge_crossfit`) verified byte-identical to the already-reviewed `external_bigram_novelty_null_audit.py`, ruling out an accidental criteria-loosening bug. `baseline`/`edge_only` reused by reference (same file used by every design since boundary-state-null). Source checksums verified against the same pinned commit used throughout this project.
