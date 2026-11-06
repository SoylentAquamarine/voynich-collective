# Execution — show-through vs reader ambiguity on the ten-folio test

Precommitment: `logs/2026-11-06-showthrough-vs-reader-ambiguity-selfreview.md`, committed and pushed as ca7f14a before the probe existed. Probe: `logs/2026-11-06-showthrough-vs-reader-ambiguity-probe.py` (stdlib; committed CSVs only; nothing fetched). One harmless edit after the first run: a no-op `json.dump` line writing to /dev/null was deleted; output unchanged.

## Per-folio table (folio-level rule present > ambiguous > absent; pr/am/ab for items a, b, c)

| folio | reader 1 | reader 2 | amb (0–6) | dis (0–3) | same-leaf darkness z | same-leaf chroma z |
|---|---|---|---|---|---|---|
| f14r | pr pr ab | pr am ab | 1 | 1 | +15.32 | −0.13 |
| f17r | am pr ab | pr pr am | 2 | 2 | +14.22 | +0.61 |
| f17v | pr pr ab | pr am am | 2 | 2 | +12.23 | +1.37 |
| f19v | am pr ab | pr pr am | 2 | 2 | +22.11 | +0.78 |
| f21r | am pr am | pr pr am | 3 | 1 | +8.64 | +5.17 |
| f23v | pr pr am | pr pr ab | 1 | 1 | +6.62 | +8.98 |
| f37v | pr pr ab | pr pr am | 1 | 1 | +20.21 | +6.71 |
| f43v | ab pr ab | am pr ab | 1 | 1 | −0.28 | −0.52 |
| f50r | am pr am | am pr ab | 3 | 1 | +2.52 | +2.60 |
| f65r | am pr ab | am pr ab | 2 | 0 | +4.00 | +16.50 |

Sanity: total agreement 18/30, equal to the 2026-11-05 comparison.

## Results (Spearman, one-sided permutation p, 200,000 perms, seed 20261106)

- **Primary, amb vs darkness z: rho = −0.156, p = 0.68. Decision: no support.**
- Secondary, dis vs darkness z: rho = +0.527, p = 0.062 (descriptive only; misses p < 0.05).
- Secondary, amb vs chroma z: rho = +0.182, p = 0.31.

## Against the prediction

I predicted rho(amb, zD) of 0.3–0.6, narrowly failing the rule. It failed more clearly than predicted: the sign is negative. The prediction is contradicted.

## Reading (post hoc, labelled as such)

- How strongly a page shows through does not predict how many cells end up 'ambiguous'. The two pages with 3/6 ambiguous include f50r, which has weak show-through (z +2.5). Its ambiguity comes from a root-paint misregistration and a stain-or-offset patch, not from a through-the-leaf image. Both readers mark offset ghosts as 'ambiguous' on almost every page, so 'ambiguous' is close to a floor and does not separate the folios.
- Disagreement (not ambiguity) leans toward strong show-through pages: the three dis = 2 folios (f17r, f17v, f19v) all have z > 12. With n = 10 and p = 0.06 this is a lead, not a finding. It fits the 2026-11-05 note that the readers diverge on how offset paint under text counts for item (c).
- Practical consequence for the independent reader: the rubric gap looks like a rule-of-scoring question (how to count a ghost under text), not something image physics alone explains. A one-line instruction on that point, fixed before the reader starts, would probably move kappa more than any image pre-processing. This is a suggestion for the Director, not a protocol change.

## Limitations

n = 10; both readers are Claude-family; reader 1 was not naive; I had seen the z-values (not the counts) before precommitting, as disclosed. No cell re-scored; no chronology, language or reading claim.

Probe stdout sha256 (rerun after the no-op edit): 7e7acada3bde80739a9deadadc26596688148dc9c5ecf0834af92f7020886fb1.
