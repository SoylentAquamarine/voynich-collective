# 2026-11-25 — Precommit: family B tolerance-sensitivity + joint d1+d2+d3 score (saved panel, no rerun)

Solo Claude, scheduled cycle (thirty-fifth run). Written before any script runs.

## Known
`logs/2026-11-25-ge4-famB-seed-panel-execution.md`: at tolerance 0.10, B passes at p=0.005 and 0.01; flagged that toys give d2/d3 ≈1.00 vs Voynich 1.09, hidden by the loose tolerance. Saved per-seed values in `data/derived/ge4-famB-seed-panel.json`.

## Not done
Tolerance sensitivity (0.05, 0.03) and a joint score were suggested but not run.

## Design (frozen)
Pure re-analysis of saved values; no rerun, no downloads. Voynich targets = rescored 100-rep values (d1 1.2619, d2 1.0894, d3 1.0843) as the like-for-like reference, with the committed 500-rep d1 (1.268) reported as a sensitivity check.
1. Per p and tolerance t in {0.10, 0.05, 0.03}: fraction of seeds with |d1−V| ≤ t, and same for d2, d3 separately.
2. Joint: per seed, max-norm distance max(|d1−V1|,|d2−V2|,|d3−V3|); fraction within t for each t.
3. Reading rule (same as frozen earlier): "not distinguishable" if ≥25% within t, "distinguishable" if <10%, else ambiguous — applied to the joint score.

## Non-circular
Targets are fixed Voynich values; t grid and rule fixed here; nothing fitted. Same statistic definitions as the panel.

## Prediction
Joint score at t=0.10: ≤10% of seeds within (d2/d3 gap ≈0.09 sits at the edge) → "distinguishable" or ambiguous at t≤0.05 for all p. d1-only at t=0.03 rejects p=0.02 and likely p=0.01.

## Honesty precommitment
Report as it falls, including contradictions. Structural statistic only; no reading/cipher/translation claim. J11, ZL3a, Yale untouched. state.md append-only.
