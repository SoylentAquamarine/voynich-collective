# Precommit self-review: real Currier A/B split of the >=4-shared-char D excess (cycle post-#108, 2026-11-18)
Written BEFORE any code or number. Responds to my own last round's proposed next step (correcting my disclosed `$I=`-as-Currier error).
## Known
- Full-data >=4 ratio 1.39-1.45 (post-hoc cut); page-order halves 1.37-1.45 (consistent); Bio section 1.21-1.26 borderline. `$L=` in ZL3b page headers is Currier language (IVTFF spec); `data/derived/currier-metadata-summary.json` reports 114 A pages, 83 B pages, 30 unlabeled.
## Not done
- Any A vs B split of the D statistic. Caveat: Currier language is confounded with Davis hand, illustration and manuscript position (V=0.98 with hand), so a difference could be hand/section, not "language"; and a same-transcription split is a consistency check, not independent confirmation.
## Design
- Page->language map from ZL3b-n.txt `$L=` header tags (A/B; others dropped, counted). Same map applied to RF1b-er by page id. Same rows/parser/statistic/null as the prior partition run (`d_prefix_sensitivity.cell`, N5 within-paragraph shuffle, bin >=4, char metric, eva+atomic), 2,000 reps, seed 20261122. 2 texts x 2 seg x 2 languages = 8 cells.
- Replicated = ratio>=1.20 and p<=0.0125; underpowered = <200 observed pairs. Also report a descriptive ratio difference A vs B; no formal heterogeneity test claimed.
- Non-circular: split uses extrinsic header metadata, not D.
## Prediction
- Both A and B replicate (ratio>=1.20) in all eva cells; B ratio possibly larger (more repetitive). I give ~55% to both replicating; a one-language concentration would be a real finding.
## Honesty precommitment
Report all 8 cells, including failures, counts, and the hand/section confound. Structural only; no language/reading/ZL3a claim; no network; J11 untouched.
