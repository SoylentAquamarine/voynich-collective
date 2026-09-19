# Token-order sensitivity audit

## Question

Rozanova and Temerev report that adjacent whole-token identity carries only 0.79% of Voynich target-token entropy after subtracting a within-line shuffle baseline, versus 2.02–15.81% in nine comparison corpora. Their public driver first keeps each corpus's 2,000 most frequent token types and maps every other type to one `<other>` symbol. Because the corpora have very different vocabulary tails, this audit asks whether that fixed type cap creates part of the reported separation.

Primary source: [Rozanova & Temerev, *A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space*](https://arxiv.org/abs/2608.17096). Code was run at the project's already-audited final bundle commit, `956a7c4fc39981f4d116fa3f4edfccce6d065571`.

## Method

`data/scripts/external_token_order_sensitivity.py` imports the paper's own corpus builder and mutual-information function. It adds three views:

1. fixed vocabulary caps from 50 to 8,000 types;
2. corpus-specific vocabularies chosen to retain the same token coverage (50%, 60%, 70%, 80%, 90%, 95%, and 97.5%); and
3. ten contiguous held-out blocks in which both the retained vocabulary and smoothed transition probabilities are learned from the other nine blocks; and
4. a nested leave-one-quire-out Voynich test in which vocabulary cap and smoothing strength are selected by inner leave-one-quire-out validation using only the other fifteen quires.

The main equal-coverage comparison was located by a broad 30-shuffle grid and then rerun with 1,000 shuffles. This is a sensitivity analysis, not a preregistered confirmatory test. The ten-block comparison preserves manuscript/corpus order but is not document-stratified for all external controls. The Voynich-only nested analysis fixes that limitation on the target side by treating each of the sixteen manuscript quires as an outer test fold.

## Results

### The 2,000-type cap does not mean equal information retention

The cap retains 84.27% of observed-separator Voynich tokens. Coverage varies substantially across controls: 67.46% for Latin botanical, 77.45% for Latin narrative, 92.98% for English narrative, and 95.56% for English herbal. Thus “2,000 types” is not a representation-matched comparison.

At the published cap, Voynich excess order is 0.7845% of target entropy and Latin botanical is 2.0597%. At equal 70% token coverage, the focused 1,000-shuffle estimates nearly coincide:

| Corpus | Retained types | Actual coverage | Excess order / target entropy |
|---|---:|---:|---:|
| Voynich observed separators | 563 | 70.013% | 1.8411% |
| Latin botanical | 2,392 | 70.003% | 1.8588% |

The difference is 0.0177 percentage points. In both corpora the observed mutual information exceeds all 1,000 within-line shuffles, so the result is not “no token order.” It is that the apparent distance between Voynich and the nearest control depends strongly on how the rare-token tail is represented.

The conclusion is not erased at every coverage. At 84.27% coverage—the amount retained for Voynich by the original cap—Latin botanical remains higher (1.4135% versus 0.7845%). Across the full coverage curve, Voynich remains at or below the nearest control, but the size of that gap is not stable.

### Held-out prediction keeps the qualitative ranking

With a fixed 500-type vocabulary and Dirichlet shrinkage strength 500, the previous token improves held-out log likelihood by 0.0675 bits per boundary for observed-separator Voynich, positive in all 10 contiguous blocks. The corresponding Latin botanical gain is 0.0940 bits, also positive in all 10 blocks; continuous narrative controls are higher (0.232–0.660 bits among Latin, German, Italian, English, and French narrative). Other smoothing strengths produce the same broad picture but materially different absolute gains.

### True leave-one-quire-out prediction confirms the signal

The fixed 500-type/alpha-500 model gains 0.0551 bits per held-out boundary across complete Voynich quires, positive in 15/16 folds. More importantly, a nested analysis selects among caps 500/2,000/4,000 and alpha 1/5/20/100/500/2,000 entirely inside each outer training set. It gains **0.0647 bits per boundary**, positive in **15/16** held-out quires. The only negative fold is quire J (−0.0143 bits across 119 boundaries); the largest folds M and T remain positive.

The nested model most often selects cap 500/alpha 500, but independently chooses cap 4,000 for the two largest atypical folds. This result is not created by applying one globally selected hyperparameter after inspecting the held-out quires. It is also directly comparable in units to the previously verified edge-glyph cross-fit: whole-token gain is about 0.065 bits/boundary versus about 0.174 bits/boundary at token edges.

This supports a narrower claim than the paper's headline wording: whole-token succession in Voynich is **weak but generalizable**, and generally weaker than the controls tested. It does not support treating the exact 0.79%-versus-2.02% separation as representation-invariant.

## Interpretation

This audit narrows rather than overturns the external result.

- Supported: whole-token identity is a weak but genuine source of out-of-quire prediction in Voynich (0.0647 bits/boundary, 15/16 positive); edge-glyph order remains substantially stronger (about 0.174 bits/boundary, 16/16 positive).
- Qualified: the numerical distance to the closest control is sensitive to fixed type cap versus equal token coverage.
- Not established: that weak token order is unique to Voynich, or that it identifies language, cipher, or generated text.

The full arrays, fold values, cap curve, coverage curve, and permutation summaries are in `data/derived/external-token-order-sensitivity-summary.json`.

## Reproduction

```bash
python data/scripts/external_token_order_sensitivity.py \
  ../paper-audit/voynich-units \
  --output data/derived/external-token-order-sensitivity-summary.json

python data/scripts/plot_external_token_order_sensitivity.py \
  data/derived/external-token-order-sensitivity-summary.json \
  docs/assets/external-token-order-sensitivity.svg
```

The original 415 KB JSON reproduced byte-for-byte before the quire extension. After adding the nested quire analysis, the expanded output was generated twice independently and compared byte-for-byte; the deterministic SVG remained unchanged because it displays only the equal-coverage curve.
