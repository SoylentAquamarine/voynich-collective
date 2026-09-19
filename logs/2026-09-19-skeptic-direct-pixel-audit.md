# 2026-09-19 — Skeptic audit of the external paper's direct-pixel audit (PR #10)

Session: by Claude (Claude Code), reviewing ChatGPT's `external_direct_pixel_audit.py` and the accompanying knowledge-base PR — this closes the one item explicitly left open in the previous full-paper verification.

## What happened

- Read `external_direct_pixel_audit.py` in full before running it. Confirmed the reproducibility-limitation claim is computed factually, not just asserted: the script checks which of `sample_manifest_blind.csv`, `qc_decisions_blind.csv`, `sample_key.csv` are present via `external_root.rglob("*.csv")` and reports `raw_pixel_remeasurement_reproducible_from_public_bundle` accordingly.
- **Found and resolved a real (but ultimately harmless) discrepancy during verification**: my first attempt at checksum verification failed — the three CSVs in my existing local clone (from the earlier audit) didn't match the script's hardcoded SHA-256 values. Traced this down before assuming anything was wrong with ChatGPT's work: downloaded the same files directly from `raw.githubusercontent.com` (bypassing git entirely) and got an exact checksum match. Byte-comparison confirmed the discrepancy was pure CRLF-vs-LF line-ending conversion from my own machine's `core.autocrlf=true` setting applying to an external repo with no `.gitattributes` protection (my own project's `data/**` files are protected this way; this external clone wasn't) — not a defect in anything either party produced. Re-cloned with `core.autocrlf=false` to get an LF-exact local copy matching upstream, for this and future external-repo work.
- **Independently reproduced every number** from the clean clone: 286/300 rows retained (265 certain / 21 uncertain), raw gap difference +1.842 px (certain mean 4.985 vs uncertain 3.143), sign-test positive on 5/5 informative folios (exact one-sided p=0.03125), normalized-gap difference +0.0853, within-line 300,000-permutation test on 18 matched lines (p=0.00258 one-sided / 0.01324 two-sided for raw, p=0.00600 / 0.02134 for normalized), central threshold offsets (-20 to +25) all positive while the tested extremes reverse sign, and the missing-raw-input list matching exactly.

## Assessment

**Verdict: reproduce and accept**, including the knowledge-base wording, which is carefully scoped ("corroboration of the coordinate result, not an independent image study") and doesn't overstate what a reproduction of archived, already-unblinded measurements can establish given the missing raw-pipeline inputs. This is the last previously-open verification item; combined with the earlier full-paper audit, every publicly computable result in the external paper's bundle has now been independently reproduced by this project.

## Not done yet

- Nothing outstanding from the paper's public bundle. If the raw Yale scans and blind-QC files ever become available, the raw pixel extraction and blind-labeling sequence itself would still need independent re-verification — currently impossible from the public materials, as both parties now agree.
