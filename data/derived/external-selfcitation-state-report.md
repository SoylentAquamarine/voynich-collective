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

Vocabulary is intermediate rather than simply closed. Faithful seeds average **58.9%** singleton types (range 58.1–60.5%), below Voynich's 69.7% but above Naibbe's 40–42%. All five pass the earlier frozen ≥55% openness floor, even though none reaches the Voynich point estimate. The external paper/site shorthand “does not reproduce open vocabulary” should therefore be read as *under-reproduces the Voynich degree of openness*, not “has a closed vocabulary.”

## Interpretation

This is a useful third mechanism data point, not a decipherment result. Self-citation has genuine local copy/mutation state and nearly matches Voynich's adjacent edit-similarity excess, yet remains far below the held-out edge signal. The missing ingredient is therefore narrower than generic “cross-token state”: it must make the final glyph of one token informative about the initial glyph of the next across unseen line blocks. The crude copy/mutate control shows the complementary failure—very high hapax share without the learned-unit scale or edge coupling—so rare-form generation alone is also insufficient.

Applied diagnostically to the already frozen six-part bands (not as a newly preregistered verdict), faithful self-citation passes the 64-merge scale, weak-token-order, and ≥55% hapax criteria; it fails the ≥0.15 edge threshold and generally misses the entropy bands. That intermediate profile is materially more informative than treating Naibbe and Cardan as the only two observations.

## Scope

This narrows the published Python reimplementation and calibration at five seeds. It does not reject copying-with-mutation generally, does not prove semantic text, and does not show that the edge association is intentional. A next mechanism control should encode **boundary-specific** state and freeze its coupling rule before observing outcomes; merely adding memory or novelty is no longer a discriminating design.
