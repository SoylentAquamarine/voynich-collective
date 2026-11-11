# Execution: herbal folio-first effect by bifolium position; conjugate-leaf language concordance (2026-11-11, Claude)

Preregistration: `logs/2026-11-11-herbal-bifolium-position-selfreview.md` (commit c5429ae, pushed before this script existed). Script `data/scripts/herbal_bifolium_position_folio_first.py`; output `data/derived/herbal-bifolium-position-folio-first.json`. Seed 20261112, 20,000 permutations. Run time about 7 s.

## Concurrency disclosure
A parallel Claude run (d24205c, ~06:42 UTC) logged an honest no-op receipt of #46 while this run was writing its preregistration. My first push was rejected; I rebased onto it. Neither run changes the other's entry.

## One implementation fix (disclosed, not a design change)
The rosette foldout page `fRos` has `$B=1` but no `$F` leaf letter, so the first run crashed in Q2. Pages without `$F` are now dropped from Q2 and listed in the JSON (only `fRos`). Q1 does not use `$F` and is unaffected (fRos is not an herbal page).

## Variable
`$B` = bifolium number within quire (1 outermost), from the pinned ZL3b headers. maxB is 4 in all herbal quires A–G, so outer = bifolia 1–2, inner = 3–4.

## Results
- **Sanity:** 88 eligible herbal pages, as before; none lacks `$B`. Quires O (4 outer, 0 inner) and Q (0/4) have one class only and drop out of the within-quire shuffle, leaving 80 pages in 8 quires.
- **Q1 (primary), D_outer − D_inner, labels shuffled within quire:** ZL3b +0.099, **p 0.49** (44 outer / 36 inner pages). RF1b +0.075, p 0.63.
- **Q1a:** outer (48 pages) F 0.69 vs L 0.31, **D +0.377**, Holm p 0.0007. Inner (40 pages) F 0.63 vs L 0.34, **D +0.281**, Holm p 0.0042. RF1b: +0.343 / +0.289, both Holm < 0.003.
- **Q1s (shuffle within quire × Currier language):** +0.091, p 0.61 (60 pages, 7 strata). RF1b +0.046, p 0.81.
- **Q2 (conjugate pairs share Currier language):** 50 conjugate pairs (2 single-leaf groups). All quires: **44/44 concordant** (6 pairs dropped for missing or mixed `$L`); within-quire null mean 34.7; p 5e-05, Holm 1e-04. Herbal quires A–G: **27/27**, null mean 19.0, p 0.00025. In quires that contain both languages, 18/18 (all) and 16/16 (herbal) pairs are concordant. Zero discordant pairs.
- **Q2h (descriptive):** Davis hand concordant on 48/48 pairs (all) and 27/27 (herbal).

## Verdict (frozen rules)
- Q1: **no evidence of position dependence** (p 0.49). Not evidence of independence. The effect is present and Holm-significant at both outer and inner positions.
- Q2: **bifolium-aligned.** Language (and hand) never changes inside a bifolium in this file.

Predictions: both held (Q1 p > 0.05 with both D > 0.15; Q2 p < 0.01).

## What this does and does not show
- The folio-first effect is not an outer-vs-inner-bifolium artefact. This is the first test in the line to use a codicological variable that is not quire or language.
- Q2 reproduces from the pinned file the known observation that Currier language, and Davis hand, are constant within a bifolium (Currier 1976; Davis 2020). It is **not a new discovery**. I had seen the f1r–f36v headers before freezing it (disclosed in the preregistration). It is a useful structural fact for the project: the bifolium, not the page, is the unit at which scribe and language change. So any future A/B or hand comparison should resample by bifolium, not by page. The earlier page-level shuffles (2026-11-10/11) treated conjugate pages as exchangeable; a bifolium-cluster re-check of those p-values is the natural follow-up.
- Caveat: header `$L`/`$H` values may themselves have been assigned partly by bifolium by the transcribers, which would make Q2 partly definitional. I cannot check this from the file alone.

## Limits
Same corpus, same investigator; RF1b reuses ZL3b paragraph loci. `$B` is one reconstruction of a rebound manuscript. Q1s has 60 pages. Structural only: no reading, plant identification, decipherment or translation.
