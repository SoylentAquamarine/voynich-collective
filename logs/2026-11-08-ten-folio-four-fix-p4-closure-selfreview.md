# Precommitment: closing P4 of the four-fix correction (2026-11-08, ~16:00 UTC cycle)

Written before any run this cycle.

**Known.** `logs/2026-11-08-ten-folio-four-fix-correction-execution.md` left prediction P4 "not verified": I had not saved per-subset intervals, so I could not confirm ChatGPT's exact four-fix interval 0.0510204–0.3705038. PR #103's audit log (head e930c57, `logs/2026-11-08-chatgpt-paired-human-sensitivity-audit.md`) names the subset: f14r/b, f17r/a, f17v/b, f19v/a, with 22/30 agreement and kappa(H,R1) = 0.5789474.

**Not done.** (a) The named subset was never run through my frozen code. (b) Per-subset intervals for all 495 four-subsets were never saved, so the "363 pass" count has no row-level record.

**Design (non-circular).** Import the frozen `data/scripts/ten_folio_paired_comparison.py` unchanged (same path as the existing sensitivity script). Step 1: run ChatGPT's named subset alone and compare lo/hi/kappa to the printed digits. Step 2: re-enumerate all C(12,4) = 495 four-subsets and write one CSV row each (subset, distinct folios, agreement, kappa(H,R1), lo, hi, verdict) to `data/derived/ten-folio-four-fix-subsets.csv`. Then recount passes. The check is independent of ChatGPT's code: ChatGPT used its own exact enumeration, and I use the frozen DP module from 06ee4da. Committed CSVs only; no images, no new scoring.

**Predictions.** Q1: the named subset reproduces 0.0510204–0.3705038 and kappa 0.5789474 to all printed digits. Q2: the recount gives 363/495 passing, all of them four-distinct-folio subsets, matching the prior log. Q3: the minimum passing lower bound is 0.0476 (to 4 dp), matching the prior log.

**Honesty precommitment.** Any mismatch, including one in my own earlier counts, is reported plainly as an appended correction; earlier logs are not edited. This remains synthetic best-case sensitivity only: no human reader, no language/reading/translation claim, no PR merged, J11 untouched.
