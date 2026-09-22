# Frozen-mechanism check: one unprompted match, one clear miss

Precommitted before running (`logs/2026-09-22-claude-criterion-b-precommitment.md`): does either already-frozen, already-merged mechanism (`boundary-shift-v2`, PR #36; `hybrid-shift-v2-substitution`, PR #40 — both built purely to satisfy the six frozen criteria, neither ever calibrated against these statistics) happen to reproduce two already-existing measurements taken for unrelated original purposes — the overall Zipf log-log slope (Statistician pass 1) and the adjacent-token Levenshtein≤2 excess over within-line shuffles (self-citation report)?

## Result

5 already-frozen seeds per mechanism, each mechanism's own already-merged primary configuration, no new parameters chosen.

| | Zipf slope | Levenshtein≤2 excess |
|---|---:|---:|
| **Real Voynich** | −0.9266 | +1.833 pp |
| `boundary-shift-v2` primary (mean of 5) | **−0.9232** | −0.78 pp |
| `hybrid-shift-v2-substitution` primary (mean of 5) | −1.1196 | −3.33 pp |

**Zipf slope**: `boundary-shift-v2` lands within 0.0034 of the real value across all 5 seeds (range −0.9132 to −0.9300) — a close, unprompted match on a statistic that played no role in its design or calibration. `hybrid-shift-v2-substitution` does not match (consistently steeper, around −1.12, a real and substantial difference from −0.9266).

**Levenshtein≤2 excess**: neither mechanism reproduces this at all. Real Voynich shows adjacent tokens are *more* similar to each other than a within-line shuffle would predict (+1.83pp). Both generated mechanisms show the *opposite* sign — adjacent tokens are consistently *less* similar than shuffled (boundary-shift-v2 ≈ −0.8pp, hybrid-shift-v2-substitution ≈ −3.3pp, worse) — a clear, consistent miss in every one of the 10 replicates checked, not a near-boundary or ambiguous case.

## Interpretation, honoring the precommitment made before running this

**This is not evidence toward promoting either mechanism.** The precommitment stated plainly that a single retrospective match on one already-frozen design is suggestive at most, not sufficient — and that remains true even though the Zipf match is real and closer than might be expected by chance. A few reasons for caution, stated directly rather than glossed over:

- Zipf-like frequency distributions are a very common emergent property of many stochastic generative processes in general (not unique to natural language, real ciphers, or this specific mechanism) — this project's own falsification standard already names "the result only restates a known corpus property, such as Zipf-like frequency... without a prediction that separates mechanisms" as an automatic stop condition against over-reading exactly this kind of match.
- One match out of two tested statistics, on one of two mechanisms, is a small, underpowered sample for drawing any general conclusion about whether boundary-shift-v2 "really" resembles Voynichese beyond the six criteria it was built to satisfy.
- The Levenshtein-neighbor miss is arguably more informative than the Zipf match: it shows a real, structural, unprompted difference between both generated mechanisms and Voynich — neither mechanism has any built-in notion of "produce near-duplicate neighboring tokens," and indeed neither does, in the wrong direction relative to Voynich's own real local-similarity structure. This is a genuine, disclosed limitation of both mechanisms as candidates for anything beyond the six criteria, surfaced by exactly the kind of check criterion (b) calls for.

**What this does show**: this is a legitimate, if modest, working example of a criterion-(b)-style check that avoids the statistic-naming trap diagnosed in `logs/2026-09-22-claude-criterion-b-reasoning.md` — the mechanisms were frozen before this check was conceived, and the statistics were measured for unrelated original purposes. It produced a genuinely mixed, non-cherry-picked result (one match, one clear miss, across two mechanisms), which is itself evidence the check wasn't rigged to succeed.

## Not done

No further mechanism design in response to this result — retuning either mechanism to also close the Levenshtein gap, having now seen it fail, would immediately recreate the statistic-targeting problem this check was built to avoid. If a future, independently-designed mechanism is later found to reproduce it without having been built to, that would be worth checking the same way.

## Provenance

- Implementation: `data/scripts/external_frozen_mechanisms_zipf_levenshtein_check.py`, importing `zipf_slope()` from `data/scripts/statistician_pass1.py` and `adjacent_similarity()` from the external `voynich-units` bundle's `reproduce_selfcitation_control.py` directly — no new statistic code written.
- Both mechanisms' transform functions imported directly from their already-merged scripts, using their already-frozen manifest seeds exactly (verified before running: `8000042...` matches `boundary-shift-v2-novelty-null-manifest-v1.json`'s postprocessor seeds; `7100042...` matches `hybrid-shift-v2-substitution-novelty-null-manifest-v1.json`'s).
- Full replicate data: `data/derived/external-frozen-mechanisms-zipf-levenshtein-check-summary.json`.
