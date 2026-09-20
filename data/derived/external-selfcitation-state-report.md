# Self-citation state audit

## Question

Does the published Timm–Schinner self-citation generator already provide the kind of cross-token state needed to explain the Voynich edge signal, or does its state live at a different level?

## Method

- Pinned external bundle: `956a7c4fc39981f4d116fa3f4edfccce6d065571`; driver SHA-256 `005eef529b314aabb917273bdd906d1cc3aff42ab348ff1b73445d494f6e84d9`.
- Ran the external driver unchanged with its built-in published calibration (`p_copy=0.10`, replacement weights `30/50/20`), five fixed seeds, 20 shuffle replicates, and the expensive substitution attack disabled.
- Collapsed EVA with the same nine substitutions used by the external bundle.
- Evaluated the first 3,950 generated lines with the project's existing 16-block held-out last-glyph → next-first-glyph predictor (`alpha=1`).
- Compared that edge signal with the generator driver's own adjacent-token Levenshtein≤2 excess over within-line shuffles.

The generator is deliberately favorable to the hypothesis: its parameters were calibrated against Voynich token length/vocabulary, and its default seed line is a real Voynich line. This is a mechanism diagnostic, not an independent natural-language baseline.

**Correction (Claude's independent audit, `logs/2026-09-20-skeptic-selfcitation-state-audit.md`):** "the first 3,950 generated lines" are the driver's own naturally-generated line breaks, not the Voynich line-length template Naibbe and Cardan forced via `wrap_to_lengths` — self-citation's own line lengths mostly match Voynich's early lines but diverge later (e.g. line 6 is length 1 vs. Voynich's 8), and the first 3,950 lines carry 32,362 tokens versus Voynich's 32,747 (a 1.2% shortfall). This is a real, disclosed methodological difference from the Naibbe/Cardan pattern, not an exact-template match. It does not change any conclusion below — the edge-gain gap (≈0 vs. 0.187) is roughly two orders of magnitude larger than a 1.2% token-count difference could plausibly produce — but a stricter version of this test should force the same line-length template used elsewhere.

## Results

| Stream | Edge gain (bits/boundary) | Positive blocks | Hapax share | Levenshtein≤2 excess | BPE minimum | Token-order share |
|---|---:|---:|---:|---:|---:|---:|
| Voynich | +0.1871 | 16/16 | 69.6% | +1.83 pp | 64 | 0.79% |
| selfcite_seed1 | -0.0015 | 6/16 | 58.4% | +1.26 pp | 64 | 0.19% |
| selfcite_seed2 | +0.0028 | 12/16 | 58.1% | +1.86 pp | 64 | 0.54% |
| selfcite_seed3 | +0.0034 | 13/16 | 60.5% | +1.62 pp | 64 | 0.40% |
| selfcite_seed4 | -0.0050 | 4/16 | 58.1% | +0.97 pp | 64 | 0.23% |
| selfcite_seed5 | +0.0001 | 8/16 | 59.4% | +1.73 pp | 64 | 0.66% |
| Crude copy/mutate | -0.0172 | 2/16 | 72.0% | -0.07 pp | 0 | -0.12% |

Across the five faithful self-citation seeds, edge gain averages **-0.0000 bits/boundary** (range -0.0050 to +0.0034), versus **+0.1871** for Voynich. Voynich is higher in 80/80 seed/block comparisons. The generator nevertheless preserves a local resemblance signal: its Levenshtein≤2 excess averages **+1.49 percentage points**, close to Voynich's **+1.83 points**.

Vocabulary is intermediate rather than simply closed. Faithful seeds average **58.9%** singleton types (range 58.1–60.5%), below Voynich's 69.7% but above Naibbe's 40–42%. **Correction:** the Cardan-grille preregistration's actual frozen hapax floor is **≥65%** (`data/external/cardan-grille-source-manifest-v1.json`), not 55% — all five seeds fall below it and **fail** this criterion, though by a real margin less than Naibbe's failure. The external paper/site shorthand “does not reproduce open vocabulary” should be read as *under-reproduces the Voynich degree of openness, and still fails the frozen threshold*, not “has a closed vocabulary” and not “passes.”

## Interpretation

This is a useful third mechanism data point, not a decipherment result. Self-citation has genuine local copy/mutation state and nearly matches Voynich's adjacent edit-similarity excess, yet remains far below the held-out edge signal. The missing ingredient is therefore narrower than generic “cross-token state”: it must make the final glyph of one token informative about the initial glyph of the next across unseen line blocks. The crude copy/mutate control shows the complementary failure—very high hapax share without the learned-unit scale or edge coupling—so rare-form generation alone is also insufficient.

**Correction:** applied diagnostically to the actual frozen six-part bands (not as a newly preregistered verdict — the checkpoint *location* and its *gap magnitude* are both required for the learned-unit criterion, and the hapax floor is 65%, not 55%), faithful self-citation passes only **token-order share** cleanly in all five seeds, and **H2** in four of five (seed 3 misses narrowly). It **fails** H1 (all five: 3.70–3.82, below the required 3.83–4.13), the learned-unit criterion (the checkpoint correctly lands at k=64, but the gap itself is 0.65–0.73 bits — below the required 0.90–1.20, so the *scale* is right while the *magnitude* is not), the hapax floor (58.1–60.5% vs. the required ≥65%), and the edge threshold (all five). Under the frozen joint rule this is a 0-of-6-criteria pass in every seed — a broader failure than the table above's headline framing suggested, not a partial success on three criteria. That corrected, more thoroughly-failing profile is still materially informative: it rules out "self-citation's local state alone" more decisively than the original framing implied, while confirming precisely which two criteria (edge, vocabulary) remain the standing discriminators across all three mechanisms tested so far.

## Scope

This narrows the published Python reimplementation and calibration at five seeds. It does not reject copying-with-mutation generally, does not prove semantic text, and does not show that the edge association is intentional. A next mechanism control should encode **boundary-specific** state and freeze its coupling rule before observing outcomes; merely adding memory or novelty is no longer a discriminating design.
