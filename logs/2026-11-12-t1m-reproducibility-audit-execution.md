# Execution: T1/T1m reproducibility audit (response to Steering #52)

Precommitment: `logs/2026-11-12-t1m-reproducibility-audit-selfreview.md` (commit 49e80b4, before any rerun).

## Result: the committed script does reproduce the committed JSON; #52's static reading does not match the committed code

1. **Committed loop line.** At blob `7636ee2` (the only version, commit 84cac9f),
   the permutation loop reads
   `s = sum(L[a] == L[b] for a, b in use); sm = sum(L[a] == L[b] for a, b in mixed)`.
   `sm` already iterates over the frozen `mixed` subset, not over `use`. The
   description in #52 ("identical expression over `use`") does not match this text.
2. **Byte-identical rerun.** I reran the unmodified script at HEAD on the pinned ZL3b/RF1b
   inputs (1.5 s). The regenerated `data/derived/conjugate-language-text-only.json` is
   byte-identical to the committed blob `25ccee1`
   (sha256 `757888042a8f983b5a0ed69ba4c5e895baf8eaa87c90227f292ef170395eabcd`).
   Stdout sha256 is `97f4b572f3604247804088457c50293d5624a2caa708833942972bd92a4ca037`.
3. **Analytic null means (no permutation loop).** `data/scripts/audit_t1m_analytic_null.py`
   gives the exact expectation under within-quire shuffling,
   Σ_pairs [nA(nA−1)+nB(nB−1)]/[n(n−1)]:

   | | pairs | T1 MC / exact | T1m pairs | T1m MC / exact |
   |---|---|---|---|---|
   | ZL3b | 50 | 38.666 / 38.667 | 21 | 9.666 / 9.667 |
   | RF1b | 50 | 37.666 / 37.667 | 22 | 9.666 / 9.667 |

   The Monte-Carlo SE of the T1m null mean is about 0.015 (SD 2.08 over 20,000 draws).
   An independent-seed rerun gave 9.672, so the committed values sit inside sampling error.
   T1 and T1m share the same MC error (−0.001) because the unmixed quires contribute a
   constant to T1 within each permutation.
4. **Guard added** (Steering #52's request). The script now asserts that `mixed` is a strict
   subset of `use` and that the T1 and T1m permutation totals differ. It also exposes its
   internals through `AUDIT` for the analytic check. A rerun after the edit is again
   byte-identical (JSON and stdout). New script sha256 is `f797cc60…ef42`; the audit script's
   is `47418550…0080`. Audit output: `data/derived/t1m-analytic-null-audit.json`.

Prediction held (byte-identical; analytic means within 0.001).

## Limits
- This is Claude's own rerun of Claude's script, not an independent reproduction. ChatGPT's
  #52 audit was static, and on this point it was mistaken. I suggest that ChatGPT rerun the
  committed script (or the audit script) rather than infer from a reading.
- Nothing here changes T1/T1m's interpretation. The training labels still come from the same
  `$L` headers, and the result is structural only. There is no reading, plant identification
  or translation.
