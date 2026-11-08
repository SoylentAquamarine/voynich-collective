# 2026-11-08 — Execution: uncertainty on the ten-folio reader-1 vs provisional-reader-2 kappa

Precommitment: `logs/2026-11-08-ten-folio-kappa-uncertainty-selfreview.md` (committed before the run).
Script: `data/scripts/ten_folio_kappa_bootstrap.py` (stdlib, `python3 -I`). Output: `data/derived/ten-folio-kappa-bootstrap.json`.
Inputs: the two committed cell CSVs only. No images, no new scoring.

## Results
- **Reproduction:** 30/30 folio-items present for both readers. Agreement **18/30**, p_o 0.600, p_e 0.367, **kappa 0.368**. This matches the 2026-11-05 entry (0.37). Per item a 6/10, b 8/10, c 4/10, also matching. There are 0 present-vs-absent flips.
- **Confusion (reader 1 rows by reader 2 columns, absent/ambiguous/present):** absent 3/5/0; ambiguous 2/3/3; present 0/2/12. All 12 disagreements are one step apart.
- **Folio-cluster bootstrap** (B=20,000, seed 20261108, 0 degenerate replicates): kappa median 0.368, **95% interval 0.171–0.583**. No replicate had kappa ≤ 0.
- Secondary, descriptive: linearly weighted kappa 0.526 (95% interval 0.358–0.686).

## Against the prediction
- Reproduction held.
- The interval was predicted to include about 0 and about 0.6. **It is wide but excludes 0** (lower bound 0.17), and its upper bound sits just under 0.6. So that half of the prediction failed: agreement is above chance, but it is pinned only to the "slight to moderate" range.

## Reading (bounded)
The two same-family readers agree above chance. The uncertainty is about as wide as the whole slight-to-moderate band, and every disagreement is about where the ambiguous boundary falls.

This does not change the gate. The protocol requires an independent (non-Claude) second reader, and this calculation cannot substitute for one. It does give the Director a number for the decision: a human reader would need kappa well above about 0.58 against reader 1 to show agreement clearly better than the model pair.

Only 10 clusters were resampled, so the percentile interval is itself rough.

No chronology, language, reading or translation claim follows.
