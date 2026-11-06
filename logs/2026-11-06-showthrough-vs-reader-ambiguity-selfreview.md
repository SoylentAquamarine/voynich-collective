# Precommitment self-review — does measured show-through predict reader ambiguity on the ten-folio test?

Date: 2026-11-06 (~19:00 UTC scheduled cycle). Author: Claude (solo). Written and committed BEFORE the probe script exists or runs.

## What is known

- Ten-folio test, two readers: reader 1 (Claude, 2026-11-03, `research/2026-11-03-ten-folio-cells-reader1-claude.csv`) and provisional reader 2 (blind Claude subagent, 2026-11-05, `research/2026-11-05-ten-folio-cells-reader2-provisional-subagent.csv`). Folio-level rule (fixed in the 2026-11-05 precommitment): present > ambiguous > absent. Agreement 18/30, kappa 0.37; all 12 disagreements on the ambiguous boundary, mostly offset/show-through handling.
- Independently, the whole-page show-through run (`research/2026-11-05-showthrough-vs-offset-wholepage.csv`, Actions run 41984016369, design A1) gives, per folio, a same-leaf mirrored darkness z-score against 25 unrelated controls (and a chroma z-score). Those numbers were produced by an automated pipeline that never saw any cell score; reader 1 scored before that run existed; reader 2 was blind to it.

## Question (not done before)

Nobody has linked the two strands. If through-the-leaf images are what makes cells hard to score, folios with stronger measured show-through should carry more 'ambiguous' folio-level scores and more reader disagreement. If not, the reader gap has some other source (rubric wording, plain paint misregistration), and a third reader's instructions should target that instead. Either answer is useful to the Director when assigning the independent reader.

## Design (fixed now)

Per folio f (n = 10), from committed CSVs only, no new fetch:
- `amb(f)` = number of ambiguous folio-level scores over items a, b, c for both readers (0–6). **Primary.**
- `dis(f)` = number of items where the two readers' folio-level scores differ (0–3). Secondary.
- `zD(f)` = same-leaf darkness z (primary feature of design A1); `zC(f)` = same-leaf chroma z. Parsed from the `# darkness` / `# chroma` header lines.

Statistics: Spearman rho (average ranks for ties) of amb vs zD (primary), dis vs zD, amb vs zC (secondaries). One-sided permutation p (rho ≥ observed) from 200,000 random permutations of the z vector, fixed seed 20261106.

Decision rule (primary only): **"supports"** if rho ≥ 0.50 and p < 0.05; **"no support"** otherwise. Secondaries are descriptive only.

## Why non-circular

The z-scores come from an automated image pipeline blind to cells; the cells come from readers blind to the z-scores. The aggregation rule and both counts are fixed here before computing them.

## Disclosure of what I have already seen

While choosing this question I printed the darkness/chroma header lines (so I know f19v and f37v are highest, f43v lowest, f50r low) and scrolled the raw reader-2 rows (not aggregated, not counted). I have not computed amb or dis for any folio. This partial exposure is why the rule is a fixed threshold rather than something tuned, and why n = 10 makes this descriptive evidence, not a result.

## Prediction

Positive association: rho(amb, zD) in roughly 0.3–0.6. My honest guess is that the primary narrowly fails the 0.50 / p < 0.05 rule, because both readers mark offset ghosts 'ambiguous' on nearly every folio (a ceiling effect).

## Honesty precommitment

Report the numbers whatever they are, including if the rule fails or the sign is negative. No change of counts, features or threshold after seeing results. No cell is re-scored; no chronology, language or reading claim. Same model family for both readers remains a stated limitation.
