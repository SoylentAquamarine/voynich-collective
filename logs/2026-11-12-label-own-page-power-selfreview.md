# Self-review (precommitment): how strong an own-page label anchor could the frozen test have detected?

Written 2026-11-12 (~18:00 UTC scheduled cycle), before any code for this analysis exists or runs.

## Known
- The frozen label own-page recurrence test (`logs/2026-11-12-label-own-page-recurrence-selfreview.md`, 5637618)
  failed its decision rule under both RF inputs: ZL3b exact 114 vs null 88.4 (p 0.016), RF1b-er p 0.038;
  `$I×$L` p 0.08 / 0.197. Three concordant executions (Claude x2, ChatGPT V8). Verdict: "no own-page anchor at this
  resolution".
- Steering #57/#58: no further same-corpus label subdivisions. What a null *means* is still unquantified: we do not know
  whether a real, modest label↔own-text anchor would have passed this rule on a corpus of this size.

## Not done yet
- Any power / minimum-detectable-effect analysis for this test.

## Design (post-hoc power analysis; does not alter the frozen verdict)
- Inputs: pinned `data/ZL3b-n.txt` and `data/RF1b-er.txt` (the input named in the precommit; recommended official per #58),
  page sets / label words / text sets built by the committed script's own `build()` (imported unchanged).
- Planted-anchor model: for anchoring rate q, each eligible label-word token on page p whose word is NOT already in p's
  text is, independently with probability q, added to p's own text set (as if the scribe had also written that word in
  the page's running text). Nothing else changes; the planted word can then also create off-diagonal hits for other
  pages' labels (the full exact score matrix is recomputed, so the null sees the planting too — non-circular).
  Same q and the same planting draws (keyed on rep, page, token index) are applied to both transcriptions.
- q grid: 0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20. 200 replicates per q.
- Per replicate: the frozen rule on the **exact** statistic H: primary within-`$I` p < 0.01 in both transcriptions AND
  `$I×$L` p < 0.05 in both. To keep compute bounded, 2,000 permutations per null per replicate (p resolution ~0.0005;
  documented deviation from the 20,000 of the original run). Power = share of replicates passing.
- Reported: power curve, the q at which power first reaches ≥ 0.8 (minimum detectable anchoring rate), and the mean number
  of planted extra own-page hits at that q, expressed against the ZL3b baseline of 114 observed / 88.4 null.
- q = 0 is a sanity check: pass rate must be ~0 (it reproduces the real data, which failed).

## Why non-circular / what it can and cannot say
- No meaning, glyph value or language label defines anything; planting is uniform and blind to word identity.
- It answers only: "had ~q of label words also appeared in their own page's text beyond what exists now, would the frozen
  rule have flagged it?" It does not re-test the hypothesis, and the uniform-planting model is a simplification (real
  anchors might concentrate on some pages or classes).

## Prediction
Power reaches 0.8 somewhere in q = 0.04–0.10, i.e. the test would have caught an anchor adding roughly 40–90 own-page hits
(~1.5–2x the null mean). If power80 needs q > 0.15, the null is weak and should be described as low-sensitivity on the
public record.

## Honesty precommitment
Report the curve whatever it shows, including if the prediction fails. The frozen verdict stays "no own-page anchor"
regardless; this only qualifies how informative that null is. Structural only: no label referent, reading or translation.
