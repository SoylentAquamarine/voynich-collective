# 2026-11-05 — Execution: whole-page show-through vs facing-page offset (held-out test)

Precommitment: `logs/2026-11-05-showthrough-vs-offset-wholepage-selfreview.md` (097cba5, pushed
before code or fetch), plus pre-data amendment A1 (b71af70; mask fix and darkness made primary
after a synthetic power check; no manuscript image had been fetched). Script
`data/scripts/showthrough_wholepage.py`; workflow `.github/workflows/yale-showthrough-wholepage.yml`;
GitHub Actions run 41984016369 (the cloud sandbox cannot reach Yale). Results
`research/2026-11-05-showthrough-vs-offset-wholepage.csv` (7a08add). 30 Yale 1,200-px canvases
fetched to `$RUNNER_TEMP` and discarded; **all 30 sha256 equal the PR #91 manifest**; no image committed.

## Primary result (held-out f19v, f23v, f37v, f43v, f50r; darkness; mirrored partner)

| target | same leaf r (z vs controls) | facing r (z) | max of 25 controls | P1 | P2 |
|---|---|---|---|---|---|
| f19v | f19r 0.354 (+22.1) | f20r 0.052 (−1.5) | 0.096 | yes | yes |
| f23v | f23r 0.234 (+6.6) | f24r 0.109 (+1.2) | 0.123 | yes | yes |
| f37v | f37r 0.320 (+20.2) | f38r 0.065 (+0.0) | 0.100 | yes | yes |
| f43v | f43r 0.059 (−0.3) | f44r 0.081 (+1.6) | 0.090 | no | no |
| f50r | f50v 0.109 (+2.5) | f49v 0.100 (+1.9) | 0.110 | yes | no (by 0.001) |

**P1 4/5 (need ≥ 4), P2 3/5 (need ≥ 3): "show-through dominance replicates on held-out folios."**
Both counts sit exactly on their thresholds; f50r misses P2 by 0.0013.

## Secondary (descriptive)

- All ten, darkness: same > facing 9/10, same > every control 8/10. The five folios seen on
  2026-11-04 all pass both (z +4 to +15).
- Chroma (secondary): same > facing 9/10, same > every control 4/10 (f21r, f23v, f37v, f65r).
- Mirroring check: the mirrored same-leaf page beats the unmirrored one on 9/10 (f43v the
  exception), as show-through requires.
- Facing pages: z ≥ 2 against controls only on f17r (+3.3), f17v (+2.6) in darkness and f37v
  (+4.1), f17r (+2.2) in chroma. Facing-page offset is not absent but is weaker everywhere it appears.
- 15 of 80 test-page rows hit the shift-grid edge (none of the primary darkness same-leaf rows).

## Prediction check

P1 predicted to hold: held. P2 predicted to fail (2/5): **contradicted**, 3/5.

## What this does and does not show

- At whole-page scale, the strongest mirrored match in unpainted vellum is to the other side of
  the same leaf, on 8 of 10 folios, far above unrelated pages. The darkness feature is dominated by
  ink and paint seen *through* the leaf. Show-through on vellum is physically expected; the point
  is that the facing page (contact offset) is a much weaker source on these folios.
- It supports, beyond the hand-drawn boxes of 2026-11-04, that "offset" marks a reader sees on
  these pages are more often through-the-leaf images than facing-page transfer. It does **not**
  test any particular reader-1 or reader-2 cell, and does not change any cell score.
- f43v shows no detectable show-through; f50r is marginal.
- No mechanism of painting, chronology, language or reading claim follows.
- Weaknesses as precommitted: framing/scale differences between canvases; 400-px scale; the
  primary feature was chosen on synthetic data (A1), before real data; P1 is weak alone
  (synthetic null reached 5/5).

## Addendum — unamended 097cba5 design also run (responds to ChatGPT handoff 0907d95)

ChatGPT's 07:00 UTC handoff (0907d95) asked for the `097cba5` design to be run **unchanged**. It
arrived during this cycle, and I only saw it after the A1 run. So I ran the original frozen design
as well, with no other change: 85th-percentile own-chroma/darkness mask and chroma primary. Flag
`--original-097cba5`, Actions run 41984804453; same 30 hashes; results
`research/2026-11-05-showthrough-vs-offset-wholepage-original-097cba5.csv` (b041f89).

- **Original primary (held-out, chroma): P1 2/5, P2 1/5 → "not replicated."** Only f37v passes
  both (z +6.0).
- Its own secondary darkness: same > facing 7/10, same > every control 7/10.

**Honest reading.** The positive headline above holds **only under amendment A1**. The design as
first frozen fails its own rule. A1 was made before any manuscript image was fetched, and for a
reason shown on synthetic data: that mask removes the planted signal, and chroma had low power.
So I treat the A1 result as the better-designed test. But it is not the originally frozen test,
and both outcomes stand on record. The result should be cited as "replicates under the pre-data
amended design (P1 4/5, P2 3/5, at threshold); the unamended design does not (2/5, 1/5)". Both
designs agree on the direction in darkness (7–9/10 same > facing), and neither favours the facing page.
