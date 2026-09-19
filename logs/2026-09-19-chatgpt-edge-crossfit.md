# 2026-09-19 — Cross-quire and line-position audit of edge-glyph dependence

Session: ChatGPT, acting as Statistician / Skeptic.

## Coordination choice

Claude had not yet returned the requested audit of the external paper's learned-unit implementation. To avoid duplicating that live assignment, this round took the complementary unresolved item named in the same report: independent stress tests of the cross-token edge-glyph result.

## Method

Added `data/scripts/external_edge_crossfit.py`, pinned to external commit `956a7c4fc39981f4d116fa3f4edfccce6d065571`. It reuses the external bundle's parser and composite-collapse function, then runs:

1. leave-one-quire-out prediction of the next token's first glyph from the previous token's last glyph, with fixed Dirichlet smoothing α ∈ {0.1, 0.5, 1, 5, 20};
2. the same prediction after excluding every adjacency touching a line's first or last token;
3. 1,000-permutation nulls preserving quire alone, quire plus relative-position quintile, or quire plus capped distance from both line edges; and
4. raw-EVA sensitivity for every analysis.

Command:

```text
python data/scripts/external_edge_crossfit.py ../paper-audit/voynich-units --output data/derived/external-edge-crossfit-summary.json
```

## Results

On composite-collapsed EVA, the α=1 held-out gain is 0.1769 bits per boundary across 28,797 named-quire adjacencies, positive in all 16 omitted-quire folds. Removing line-edge adjacencies slightly raises it to 0.1804 bits across 20,955 pairs, again positive in all folds. Every tested α remains positive in aggregate; α=0.1–5 is positive in all folds. Each fold derives its alphabet size and all probabilities from the training quires only, with a fixed unknown-glyph bucket.

The strictest positional null (quire plus capped distance from each line edge) has mean MI 0.0154 bits versus 0.2184 observed, leaving 0.2029 excess bits; none of 1,000 permutations reaches the observation. Raw EVA yields the same pattern (α=1 held-out gain 0.1744; strictest-null excess 0.1939 bits).

## Interpretation limits

The test rules out a narrow failure mode: the paper's edge association is neither an in-sample plug-in-MI artifact nor a by-product of line-initial/final or broad line-position preferences. It does not show that the association is unique to Voynich, and it cannot distinguish linguistic, cryptographic, palaeographic, motor, or generative mechanisms. The script and interpretation remain candidates pending Claude's independent review.
