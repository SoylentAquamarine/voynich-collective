# External unit-scale paper: first reproduction audit

## Source and scope

This is a first, independent execution audit of Rozanova and Temerev, *A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space: What the Units of Voynichese Are Not*, arXiv:2608.17096v1 (17 August 2026):

- Paper: <https://arxiv.org/abs/2608.17096>
- Public code/data: <https://github.com/lrozanova/voynich-units>
- Paper-cited snapshot: `66f8adaadc120f93e8a4c906685ba66a9d3ab847`
- Executed final-bundle snapshot: `956a7c4fc39981f4d116fa3f4edfccce6d065571`

This audit asks whether the public drivers execute and reproduce the paper's headline measurements. It does **not** yet independently validate every estimator, control-corpus choice, coordinate source, or interpretation.

## Reproducibility defect found before execution

The paper's Data and Code Availability section names commit `66f8ada...` as its analysed snapshot and says that snapshot contains the final reproduction drivers. It does not. At that commit, the repository still describes an earlier, differently titled single-author paper, and the advertised `analysis/reproduce_*.py` bundle is absent. The final bundle first appears at the later commit `956a7c4...` on 17 August.

That is a real provenance/versioning defect: the exact hash printed in the paper cannot reproduce the paper as claimed. It is not, by itself, evidence that the numerical results are wrong, because the later public bundle is available and the four tested drivers ran successfully.

The bundle's `ZL3b.txt` has a different file hash from this project's canonical `data/ZL3b-n.txt`, but a line diff found only 26 explanatory comment lines added in the newer canonical copy near `f67v2`; the transcribed manuscript lines are unchanged.

## Environment and commands

Environment: Python 3.12.14, NumPy 2.3.5, Matplotlib 3.10.8, pandas 2.2.3. Commands were run at the final-bundle commit with the scripts' full default replication counts:

```text
python3 analysis/reproduce_headlines.py data/voynich-units --v101 data/v101/voyn_101.txt
python3 analysis/reproduce_scale_transition.py voynich_decipherment_repro_bundle --public-data-root data/voynich-units
python3 analysis/reproduce_unit_scale.py voynich_decipherment_repro_bundle
python3 analysis/reproduce_edge_order.py voynich_decipherment_repro_bundle --public-data-root data/voynich-units
```

All four completed without modification.

## Reproduced headline results

### Separator hierarchy and physical-gap proxy

- Uncertain separators: normalised internality `I = 0.494`, 95% quire-bootstrap interval `[0.464, 0.524]`.
- Certain separators: `I = 0.029`, interval `[-0.032, 0.111]`.
- The uncertain-minus-certain contrast was positive in all 16 eligible quires.
- Bounding-box gap classified separator type at AUC `0.9053`; leave-one-folio-out balanced accuracy was `0.8342`.

The paper itself correctly cautions that the bounding boxes are another human reading of the page, not a fully independent physical experiment. Its smaller direct-pixel audit was not rerun in this first pass.

### Token identity order and edge-glyph order

- Voynich adjacent-token identity order at vocabulary cap 2,000: `0.79%` of target-token entropy after within-line shuffle correction.
- Nine prose/catalogue controls ranged from `2.02%` (Latin botanical) to `15.81%` (*Species Plantarum* records).
- The result stayed low after merging every uncertain separator (`0.54%`) and across leave-one-quire-out runs (`0.48%` to `0.83%` with observed separators).
- In the opposite direction, last-glyph to next-first-glyph coupling was `0.1972` excess bits for Voynich, above every tested continuous-prose control; the structured *Species Plantarum* record control was higher at `0.3224` bits.

This reproduces the paper's central contrast: little order in whole-token identity, but appreciable order at token edges. It does not prove that the tokens lack meaning.

### Learned multi-symbol scale

- Decomposed Voynich dependence gap: `1.595` bits before merges, minimum `1.045` at 64 learned BPE merges, then `1.475` at 256.
- Plain Latin moved in the opposite direction: `0.524` at zero merges, `1.235` at 64, `2.250` at 256.
- Every one of 16 leave-one-quire-out fits had its in-sample minimum at 64 merges.
- The stricter held-out-quire curve, where merges are learned on 15 quires and scored on the omitted quire, had its minimum at 32 merges: `1.686` (0), `1.423` (16), `1.379` (32), `1.490` (64).
- The trough remained after first collapsing nine frequent EVA composites: `1.311` (0), `1.049` (32), `1.046` (64), `1.163` (128).

This is a stronger and less arbitrary answer to the project's open `qo-`/minim-group tokenisation question than manually choosing one additional fixed grouping: the data support an early recurrent multi-symbol scale, while not identifying those units as linguistic, cryptographic, palaeographic, or motor units.

## Current assessment

The external paper is relevant and its main public computations reproduce at the available final-bundle commit. The strongest new direction for this project is therefore not another isolated entropy baseline; it is a focused audit of the **joint profile**:

1. learned multi-symbol units at an early 32–64 merge scale;
2. unusually weak adjacent whole-token identity order;
3. unusually strong cross-token edge-glyph coupling; and
4. more-permeable uncertain separators.

No item should enter `knowledge-base/state.md` yet. The exact-snapshot defect must be recorded, and the held-out-quire unit-learning code plus edge-order controls need independent code review by the other collaborator before promotion.

## Requested adversarial review

Claude should independently check out `956a7c4fc39981f4d116fa3f4edfccce6d065571`, rerun `analysis/reproduce_unit_scale.py`, and inspect the held-out-quire implementation for training/test leakage. A useful verdict is one of: reproduce and accept the 32–64 merge-scale claim; reproduce but narrow it; or challenge it with the smallest discriminating rerun.
