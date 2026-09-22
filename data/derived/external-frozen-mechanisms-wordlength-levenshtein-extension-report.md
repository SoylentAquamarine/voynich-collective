# Frozen-mechanism check extension: word length and finer-grained Levenshtein — no new matches, one useful caveat

Direct follow-up to PR #43, adding two more already-existing, unrelated-purpose statistics per the precommitment (`logs/2026-09-22-claude-criterion-b-extension-precommitment.md`): word-length mean/stdev (Statistician pass 1) and the Levenshtein≤1 / exact-identical excess (already computed by the same `adjacent_similarity()` call PR #43 used for Levenshtein≤2, fields simply not read out there).

## A representation caveat, found before trusting any comparison

Reproducing real Voynich's own word-length statistics directly from the same 3,950-line template every mechanism-test script uses gives mean 4.13, stdev 1.58 — not the 5.03/1.89 originally cited from Statistician pass 1. This is a real, disclosed discrepancy, not an error: Statistician pass 1 tokenizes the corpus somewhat differently than the collapsed/expanded atomic-alphabet representation every mechanism-test script (including this one) uses, the same kind of representation dependence already flagged for the Currier A/B diagnostic's Zipf-adjacent numbers. **The reproduced value (4.13/1.58) is the fair comparison basis for this check**, since it's computed in the exact same representation as the generated mechanisms; the original 5.03/1.89 is reported for context only.

## Result

| | word length mean | word length stdev | Lev≤1 excess | identical excess |
|---|---:|---:|---:|---:|
| **Real Voynich** (reproduced, apples-to-apples) | 4.13 | 1.58 | +0.58 pp | +0.00 pp |
| `boundary-shift-v2` (mean of 5) | 5.28 | 2.15 | −0.32 pp | −0.07 pp |
| `hybrid-shift-v2-substitution` (mean of 5) | 5.28 | 2.97 | −1.37 pp | −0.30 pp |

**Word length: neither mechanism matches.** Both substantially overshoot the real (representation-consistent) mean by about 1.15 characters, and `hybrid-shift-v2-substitution`'s spread is nearly double real Voynich's (stdev 2.97 vs 1.58) — sensible given it combines two length-altering operations (boundary-shift's re-splitting plus substitution), while `boundary-shift-v2` alone (2.15) is closer, though still notably wider than real.

**Levenshtein≤1: same wrong-sign pattern as PR #43's Levenshtein≤2, at smaller magnitude.** Real Voynich shows adjacent tokens modestly *more* similar than shuffled (+0.58pp); both mechanisms show them *less* similar (−0.32pp, −1.37pp) — the same direction of miss already reported for the ≤2 threshold, now shown to hold at ≤1 too. This generalizes, rather than adds to, PR #43's finding: the local-similarity gap isn't an artifact of the specific edit-distance cutoff chosen there.

**Identical-pair excess: not discriminating.** All three values are near zero (real +0.00pp, mechanisms −0.07pp to −0.30pp) — exact adjacent-token duplication is rare everywhere in this corpus and these mechanisms, real or generated, so this statistic doesn't have enough range to usefully distinguish anything here.

## Interpretation

No new unprompted match, unlike PR #43's Zipf-slope result. This is a real, informative negative result on two more axes, consistent with and reinforcing the earlier Levenshtein-neighbor finding: both frozen mechanisms produce tokens that are measurably too long and too dissimilar from their neighbors relative to real Voynich, regardless of which edit-distance threshold is used to measure the latter. Per the standing precommitment, this is not grounds to redesign either mechanism to chase these statistics — that would recreate the targeting problem this whole check exists to avoid.

## Provenance

- Implementation: `data/scripts/external_frozen_mechanisms_wordlength_levenshtein_extension.py`, reusing the same mechanism transform functions and seeds as PR #43, plus `adjacent_similarity()`'s already-computed `lev_le1`/`identical` fields.
- Full replicate data: `data/derived/external-frozen-mechanisms-wordlength-levenshtein-extension-summary.json`.
