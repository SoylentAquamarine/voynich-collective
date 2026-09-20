# 2026-09-20 — Execution of the boundary-coupled constructive null (solo)

Session: by Claude, executing `methods/boundary-coupled-null-preregistration.md` after its own solo adversarial self-review (`logs/2026-09-20-claude-solo-boundary-null-selfreview.md`), user-authorized to proceed without ChatGPT's review given their extended silence.

## What happened

- Built the generator (`data/scripts/external_boundary_null_audit.py`) reusing the project's own established checksum-pinning conventions: `voynich-units` commit `956a7c4...` and the Latin ITTB treebank (three conllu files, all checksum-verified against the manifest already pinned in `data/scripts/language_baselines.py`).
- **Implementation surfaced two further design defects beyond the two the paper self-review caught**, both fixed and documented inline in the design document as "Implementation-pilot correction" notes:
  1. The originally-designed alphabet (`grille.ALL_GRAPHEMES`, multi-character EVA fragments) doesn't actually let the coupling rule control what the scoring metric (`edge_crossfit`) measures, since that metric reads only the raw trailing/leading *character* of each token string, not a "glyph unit." Fixed by switching to the 25 single EVA letter-characters that actually appear in real Voynich tokens, closing the gap between design intent and implementation completely.
  2. The `p_novel` novelty-splice mechanism pushed the wrong direction: piloting the order-2 Latin-trained internal model showed it already produces ~83% hapax share with *zero* novelty injection — well above Voynich's ~70% target — so a mechanism to *increase* openness was backwards. Replaced with a `p_reuse` mechanism (resample previously-generated internal parts from a length-bucketed memory) that can push hapax share *down*, calibrated via a self-consistency-only pilot (three seeds, never compared to Voynich's actual profile) to `p_reuse = 0.87`, landing at 69.9–70.3% hapax.
- Smoke-tested the full pipeline on one replicate before committing to the full run: caught and fixed one more implementation bug (tracking a token's "last glyph" as the trailing string *character* rather than a discrete unit — harmless once the alphabet became single-character, but would have been a real bug with the original multi-character alphabet).
- Ran the full frozen sweep: 5 primary `p_couple` values (0.3/0.5/0.7/0.9/1.0) × 20 seeds = 100 replicates, negative control (`p_couple=0.0`) × 20 seeds, and an ablation (uniform-random internal characters instead of the order-2 Latin model, at whichever primary configuration had the highest mean edge gain — `p_couple=1.00`) × 5 seeds. 125 replicates total, ~12s each, ~24 minutes wall-clock.

## Result

**Primary verdict: FAIL** — 0/20 joint passes at every `p_couple` value, per the frozen 16/20 rule.

But the failure shape is the opposite of all three historical mechanisms tested so far:

- **Edge prediction**: passes cleanly, 20/20 seeds, at every non-zero `p_couple`, with a clean monotonic dose-response (mean gain +0.225 at p=0.30 rising to +2.409 at p=1.00 — all far exceeding both the 0.15 threshold and Voynich's own +0.1871). The negative control (p_couple=0) collapses to near-zero (-0.013, 0.1/16 positive blocks), and the ablation confirms the internal-structure model contributes nothing to this signal either way. This is a clean, unambiguous demonstration that the coupling rule does exactly what it was built to do.
- **Vocabulary openness**: passes cleanly, 20/20, in every configuration including the negative control (69.6–71.3% hapax vs. Voynich's 69.7%) — the calibrated `p_reuse` mechanism transfers robustly and is fully decoupled from coupling strength, as designed.
- **Token-order-share**: partially satisfied, varying 5–14/20 by configuration — real seed variance, not a clean pass or fail.
- **Character entropy (H1/H2) and the learned multi-symbol-unit scale**: fail universally, in all 125 replicates including the negative control and the ablation. The BPE dependence-gap minimum lands at k=0 merges in every single replicate (required 32 or 64) — the internal-structure model's character-level output has essentially no redundancy that multi-symbol merging exploits, unlike Voynich's real glyph-cluster structure.

## Assessment

This is a materially informative result, not just another failure to log. The three historical mechanisms (Naibbe, Cardan, self-citation) all failed primarily on edge-prediction and vocabulary openness while passing some mix of entropy/unit-scale/order. This constructive null inverts that pattern completely: it satisfies edge-prediction and vocabulary trivially (because it was built specifically to) while failing entropy and unit-scale universally (because that component was deliberately left uncontrolled, to avoid circularity). That the four mechanisms tested so far fail on different, non-overlapping subsets of the six criteria is itself evidence the joint profile is doing real discriminating work — it isn't just one easy-to-fail property restated five different ways, since a mechanism purpose-built to pass two of the criteria that trip up every other mechanism still cannot jointly satisfy all six.

The honest limitation: this design deliberately left the internal-structure component uncontrolled by construction (using a plain Latin-trained order-2 character model, specifically to keep the coupling result free of circularity). It does not show that entropy/unit-scale are hard to construct in general — only that this specific, disclosed, non-Voynich-tuned internal model doesn't happen to produce Voynich-like compression structure. A generator that combined the now-validated boundary-coupling mechanism with an internal-structure model deliberately tuned toward Voynich's entropy/unit-scale profile might do much better — but building and testing that would need its own preregistration, not a retroactive parameter change to this one (per the stop conditions already frozen in the design document).

## Not done yet

- **Update, same session**: ChatGPT returned before this PR was reviewed and gave the design a "challenge; pause execution" verdict on three points, posted while this execution was already running. Claude did not see it until after finishing and had already opened this PR — a real process lapse, disclosed in `logs/2026-09-20-skeptic-boundary-state-null-review.md`. All three points were accepted after independent verification (including hand-recomputing ChatGPT's channel-capacity math, which matched exactly), and the report's interpretation was revised accordingly before any knowledge-base proposal.
- A combined boundary-coupling + Voynich-tuned-internal-model generator was not attempted and would need a new preregistration.
