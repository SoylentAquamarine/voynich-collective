# 2026-09-20 — Solo self-review: frequency-novelty-null design

Design: `data/external/frequency-novelty-null-manifest-v1.json`. Solo self-review because ChatGPT is no longer automated (user runs it manually, on their own schedule) — disclosed as a weaker substitute for cross-party review, not treated as equivalent, per this project's established practice.

## What this design is testing

`boundary-state-null`'s `edge_only` control already passes 5 of 6 criteria (fails only hapax, 51.3% vs required 65%). `novelty_only`'s uniform-substitution rule opens vocabulary but wrecks entropy/units. The natural next test: keep the coupling rule fixed at its already-validated `beta=0.50`, and replace only the novelty rule's *replacement-atom distribution* — from uniform-over-25-alternatives to the replicate's own running atom-unigram frequency — to see whether that specifically fixes the entropy/unit damage while still opening vocabulary.

## Issues found and fixed in this pass

**1. Search-thoroughness confound (real design defect, fixed).** My first draft used bounded random resampling (50 attempts) to find an unseen variant, versus the original boundary-state-null's exhaustive deterministic cyclic search over every position x all 25 alternatives. If the new design's hapax gain comes out lower than `novelty_only`'s, that could be an artifact of a weaker search rather than a real effect of frequency-weighting — the two designs would no longer be a clean single-variable comparison. **Fixed**: rewrote the search to be exhaustive like the original — iterate all non-initial positions in a random-but-deterministic order (seeded), and at each position, iterate all 25 alternative atoms in a *frequency-weighted* order (highest running-frequency atom tried first) rather than the original's fixed cyclic order, accepting the first unseen type. This guarantees an unseen variant is found whenever one exists, matching the original's guarantee, so any difference in outcome is attributable to *which* atom gets tried, not *how hard* the search tries.

**2. Cold-start behavior.** For the first few tokens, there's no meaningful running frequency distribution yet. Fallback to uniform-over-alternatives for tokens before 5 have been emitted — this affects a negligible fraction of an ~80,000-token stream and doesn't meaningfully leak into the aggregate result. Kept as specified.

**3. Circularity check.** The replacement distribution is built only from the replicate's own generated output (the boundary-coupled Naibbe stream), never from Voynich's transition statistics or its lexicon. No leak found.

**4. Honest uncertainty flagged, not fixed (can't be fixed by design, only reported honestly).** As the stream grows long, the running unigram distribution over 25 atoms may flatten toward near-uniform anyway, since all atoms will have accumulated broadly comparable counts over tens of thousands of tokens — the frequency-weighting effect could fade for later tokens in a replicate, making this design's benefit (if any) concentrated early and diluted late. This is not a bug to fix; it's a real property of the mechanism that the result needs to be interpreted honestly against, not glossed over if the primary result is a FAIL.

## Manifest update

Rewrote `transformation.frequency_novelty_injection` in the manifest to reflect the fixed exhaustive frequency-weighted search (item 1 above) before any pilot or outcome was computed.

## Verdict

Accept the design as corrected. Proceeding to pilot-calibrate `nu` (self-consistency only, per the manifest's frozen rule) and then implement and run the full sweep.

## Pilot calibration (self-consistency only, run after this review)

3 seeds, `frequency_novelty_only` config (beta=0), swept nu in {0.05, 0.1, 0.15, 0.2, 0.3, 0.45, 0.6, 0.75}, measuring only `hapax_share_of_types` (no other criterion checked during calibration):

| nu | mean hapax (3 seeds) |
|---|---|
| 0.05 | 0.514 |
| 0.10 | 0.589 |
| 0.15 | 0.647 (just below the 0.65 floor) |
| 0.20 | 0.685 (in band) |
| 0.30 | 0.746 (overshoots) |
| 0.45 | 0.803 |
| 0.60 | 0.848 |
| 0.75 | 0.894 |

Frozen: **nu=0.2**. Sensitivities set to nu=0.1 (weaker) and nu=0.3 (stronger) around it. Manifest updated with these frozen values before generating any primary/control-config outcome.
