# Independent arithmetic audit: GE4 family-B tolerance sensitivity — 2026-11-24

## Pinned input
- Voynich repository file: `data/derived/ge4-famB-seed-panel.json`
- Git blob SHA: `3a085f5e7d228b12afe4b3250b73c465a2d1f2ff`
- Claude execution: `logs/2026-11-25-ge4-famB-seed-panel-execution.md`

## Method
Parsed the saved JSON independently and recomputed absolute d1 differences from the committed Voynich value (1.268), plus a joint Euclidean distance over d1/d2/d3 against (1.268, 1.090, 1.084). This is an arithmetic reproduction of saved values, not a raw pipeline rerun or independent regeneration of the 20 seeds.

## Results
| Mutation p | d1 within 0.10 | d1 within 0.05 | d1 within 0.03 | joint d1/d2/d3 distance <= 0.10 |
|---|---:|---:|---:|---:|
| 0.005 | 14/20 | 2/20 | 0/20 | 0/20 |
| 0.01 | 6/20 | 1/20 | 1/20 | 0/20 |
| 0.02 | 0/20 | 0/20 | 0/20 | 0/20 |

## Interpretation and limits
The frozen d1-only 0.10 rule classifies p=.005 and p=.01 as “not distinguishable,” but tighter d1 tolerances and the joint profile show separation. This confirms the caveat in Claude's execution log that d2/d3 remain materially different; it does not invalidate the preregistered d1 rule after the fact. The joint metric and tighter thresholds are exploratory and must be precommitted before any new decisive test. No source reading, language identification, cipher mechanism or translation is established.

## Decision
Do not rerun the seed panel. Next useful test is a precommitted joint d1+d2+d3 metric and tolerance-sensitivity analysis on these saved values, followed by separate source-language evidence gates. J11 remains queued and undispatched.
