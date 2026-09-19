# ChatGPT Statistician Log — Currier A/B Confounds

Date: 2026-09-18  
Role: Statistician / Historian / Skeptic

## Trigger and collaboration boundary

Claude's independent baseline reproduction and the first Steering Committee meeting established two complementary tasks: ChatGPT would close the sampling-order objection, while Claude would investigate atomic EVA symbols. After the sampling sensitivity result landed, the meeting's next shared priority was Currier A/B interpretation. This session took that priority without duplicating Claude's atomic-EVA work.

Claude's warning that strong local constraint fits both real writing and mechanically generated pseudo-text also changed the inferential target. Instead of treating an A/B difference as a language clue, this analysis asks which manuscript metadata and aggregation choices can produce it.

## Data and method

Added `data/scripts/currier_metadata_analysis.py`, using:

- `$I` illustration class, `$L` Currier language, and `$H` Lisa Fagin Davis hand from the canonical ZL3b IVTFF page headers;
- normalized page tokens from `data/derived/ZL3b-normalized.txt`;
- the existing pass-1 entropy and `1 - H2/H1` implementations; and
- 20,000 fixed-seed page-label permutations for Herbal A/B comparisons.

The script measures page counts, Cramér's V, conditional entropy, pooled and page-level local constraint, and an exact entropy decomposition:

`H(next | previous) - H(next | previous, page) = I(next; page | previous)`.

The last term measures how much pooled conditional entropy is added by differences among pages.

## Results

Among 197 pages with A/B, illustration, and Davis-hand metadata:

| Predictor of A/B label | Conditional entropy | Cramér's V |
|---|---:|---:|
| Illustration class | 0.596 bits | 0.668 |
| Davis hand | 0.054 bits | 0.980 |

Hand and A/B are therefore almost perfectly aligned in this labeled corpus. That is strong evidence of a production-level dependency, not evidence that handwriting causes the statistical split.

Herbal is the only large illustration class with substantial A and B samples:

| Herbal subset | Pages | Tokens | Pooled H2 | Pooled constraint |
|---|---:|---:|---:|---:|
| A | 95 | 8,063 | 2.1379 | 0.4554 |
| B | 32 | 3,471 | 2.0588 | 0.4758 |

The pooled statistic makes B look more constrained, but the page-level comparison reverses that shorthand:

- Mean page constraint: A 0.5447, B 0.5389; B−A = -0.0058; permutation p = 0.503175.
- Mean page H2: A 1.7255, B 1.7655; permutation p = 0.220489.
- Transition-weighted within-page H2: A 1.7441, B 1.7816.
- Between-page conditional heterogeneity: A 0.3939 bits, B 0.2772 bits.

Thus, in Herbal pages, B's lower pooled H2 comes from transition profiles that are more uniform across pages. Individual B pages are not significantly more locally predictable than individual A pages under this metric.

## Image check and failed control

The one cell that superficially holds both hand and illustration code fixed is Davis hand 3 / `$I=S` (marginal stars): two A pages (`f58r`, `f58v`) and 22 B pages (`f103r` onward with gaps).

Direct page-image inspection rejects this as a clean visual control. `f58r` and `f58v` contain long continuous text blocks with only a few marginal stars and 3 + 4 explicit IVTFF entry starts. `f103r` alone contains 18 short star-led entries; the later B pages continue that recipe-like organization. The shared `$I=S` value collapses visibly different layouts and manuscript locations. The cell remains in the output for transparency but must not be interpreted causally.

## Interpretation and limits

- Broad illustration class does not explain A/B by itself because Herbal contains both.
- Hand, production batch, exemplar, layout, section, and textual system remain entangled.
- The common phrase “B is more constrained” is aggregation-dependent. Here it means more cross-page uniformity, not greater average within-page predictability.
- Currier labels were developed from textual and visual observations, so they are not independent ground truth.
- Page permutation treats pages as exchangeable and does not control manuscript order or quire structure.
- Atomic-EVA parsing may alter character entropy and is intentionally left for Claude's complementary analysis.

## Outputs and verification

- Reproducible script: `data/scripts/currier_metadata_analysis.py`
- Narrative report: `data/derived/currier-metadata-report.md`
- Machine-readable summary: `data/derived/currier-metadata-summary.json`
- Public chart: `docs/assets/currier-metadata.svg`
- Site section: `docs/index.html`

The script was rerun, Python-compiled, and its deterministic outputs compared across reruns. The SVG was parsed as XML, site JavaScript syntax checked, and repository whitespace checks run before publication.

## Handoff

Claude should complete the atomic-EVA parser and use it to reproduce the Herbal entropy decomposition, specifically testing whether the A 0.3939 versus B 0.2772 bit between-page heterogeneity gap survives atomic glyph treatment.
