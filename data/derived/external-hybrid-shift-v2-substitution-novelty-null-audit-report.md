# Hybrid shift-v2+substitution: FAIL, but a genuinely more informative one than the original hybrid's INVALID_CONSTRUCTION

Preregistered design (`data/external/hybrid-shift-v2-substitution-novelty-null-manifest-v1.json`), solo Claude, self-reviewed (`logs/2026-09-22-claude-hybrid-shift-v2-substitution-selfreview.md`). Tests whether hybrid-shift-substitution's known token-order-share failure (PR #35, INVALID_CONSTRUCTION) is the same bug already root-caused and fixed once in the standalone boundary-shift design (PR #34 → PR #36, v1 → v2), by swapping in the already-validated v2 split rule (prefer a split where exactly one piece is new) and keeping the substitution top-up unchanged.

## Result

**Verdict: FAIL** (both manipulation checks pass cleanly, 20/20 each; 0 of 20 primary replicates pass all six criteria jointly).

| Config | beta | nu_sub | joint pass | order-share mean (range) | order passes |
|---|---:|---:|---:|---:|---:|
| primary | 0.5 | 0.01 | 0/20 | 0.0234 (0.0212–0.0269) | 0/20 |
| hybrid_novelty_only | 0.0 | 0.01 | 7/20 | 0.0205 (0.0175–0.0237) | 7/20 |
| shift_only_no_topup | 0.5 | 0.0 | 0/5 | 0.0230 (0.0218–0.0248) | 0/5 |
| stronger_topup | 0.5 | 0.02 | 0/5 | 0.0223 (0.0213–0.0237) | 0/5 |

Every other criterion (H1, H2, learned units, edge, hapax) passes in every replicate of every configuration that has coupling and vocabulary growth turned on — often with comfortable margins (hapax ~92.3%–92.9%, far above the 0.65 floor; edge gain ~0.91–0.94 bits/boundary, far above the 0.15 floor). Token-order-share is the sole, isolated blocker, and it sits *just* above the 0.02 ceiling in every failing configuration.

## Interpretation: the v2 fix hypothesis was partially right — a second, independent cause is also at play

The preregistration's hypothesis was that hybrid's order-share failure is the identical bug already fixed once in the standalone boundary-shift design (v1's "both pieces must be new" split rule guaranteeing `<other>`-collapsed adjacency). **That hypothesis is partially confirmed, not refuted, by this result.** Comparing `primary` (beta=0.5) against `hybrid_novelty_only` (beta=0.0, identical shift-v2 and top-up mechanics, coupling switched off) isolates the effect cleanly: without coupling, order-share sits right at the 0.02 boundary and passes in 7 of 20 seeds — a dramatic improvement over the original v1 hybrid's report of a "wide, consistent margin" failure in all 20 seeds. The v2 split-rule fix did move the needle, substantially.

**But a second, independent, previously-unattributed source of order predictability is also present: the boundary-coupling step itself.** `beta=0.5` — the deterministic rule linking each token's first character to the previous token's last character, reused unchanged across every design in this entire project since the very first Naibbe control — pushes order-share back over the ceiling on its own. `shift_only_no_topup` (coupling on, substitution top-up off entirely) fails order-share just as consistently as the full primary config (0/5, mean 0.0230), and `stronger_topup` (doubling the substitution dosage) doesn't help either (0/5, mean 0.0223) — ruling out the substitution top-up's dosage as a contributing factor. Coupling, not the shift mechanism or the substitution top-up, is what pushes this specific combination over the edge.

**This was not visible in the original hybrid design's own report**, which attributed the order-share failure entirely to the shift mechanism's token-pair determinism. That attribution undersold the coupling step's own contribution, because the original v1 hybrid's shift-rule bug was severe enough (a much wider margin, per that report) to mask a second, smaller effect running underneath it. Fixing the larger bug revealed the smaller one.

## What this does and does not show

**Does not show**: that a section-aware or any other future mechanism combining boundary-shift-v2 with vocabulary-opening substitution can never jointly pass all six criteria. Coupling's own contribution to order predictability appears to be a comparatively small, borderline effect (order-share sits just barely above the ceiling, not by a wide margin, and passes outright in nearly half the seeds once coupling is removed) — a further design that also addresses coupling's contribution, not just the shift rule's, might plausibly close the remaining gap. That is a new, disclosed hypothesis for a possible future preregistration, not attempted here.

**Does show**: this project's own established discipline (change one variable at a time relative to an already-understood design) worked exactly as intended. Swapping only the shift component isolated its real, if partial, contribution and surfaced a second cause that a less careful design (changing several things at once) would have left conflated. The result is a genuine FAIL, not an INVALID_CONSTRUCTION — the manipulation checks confirm this hybrid still constructs a real, if incomplete, effect (both boundary and novelty checks pass cleanly), unlike a design whose underlying construction itself is broken.

**Reframes the section-aware six-criterion question from the prior reasoning log** (`logs/2026-09-21-claude-section-aware-six-criterion-reasoning.md`): hybrid was identified there as the only candidate with both required properties (an H2-moving dosage and a path to 6/6), contingent on fixing its order-share failure first. That fix is now shown to be necessary but not sufficient — a second, coupling-driven cause remains. A section-aware attempt built on this design would inherit both this design's own unresolved order-share problem and its own new complexity; still not a well-motivated next step until coupling's contribution is itself understood or addressed.

## Provenance

- Script: `data/scripts/external_hybrid_shift_v2_substitution_novelty_null_audit.py`, diffed against the original hybrid script before running to confirm only the split-rule (and file-path) changes were made — see `logs/2026-09-22-claude-hybrid-shift-v2-substitution-selfreview.md`.
- Pilot calibration: nu_sub frozen at 0.01 (smallest grid value tested, already saturating the hapax floor far above the manifest's anticipated target band — a disclosed deviation from the literal calibration rule, documented in the self-review log before the full run).
- Full summary: `data/derived/external-hybrid-shift-v2-substitution-novelty-null-audit-summary.json`.
