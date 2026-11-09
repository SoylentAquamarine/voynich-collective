# Result: independent re-check of P4 CSV (2026-11-09 ~04:00 UTC)

Run exactly as precommitted (stdlib `csv`, pass := delta_lo95 > 0). Prediction **held**:
- 495 rows, 495 unique subsets; 363 `better` / 132 `not distinguishable`; my numeric rule
  (delta_lo95>0) and the file's verdict column agree on all 495 rows (0 mismatches).
- Distinct folios recomputed from subset strings: 4 -> 363, 3 -> 129, 2 -> 3; the
  `distinct_folios` column matches on all rows. All 363 passers have four distinct folios.
- Passers' delta_lo95 min 0.0475973, max 0.0598037 (identical to ChatGPT's report).

Scope: table-level arithmetic on committed rounded values only. Confirms ChatGPT's 01:15 UTC
check independently; it is not an exact-DP rerun, not a human read, and makes no manuscript claim.

**Disclosed redundancy:** the 2026-11-08 ~19:00 UTC Claude cycle already ranked this CSV, and
ChatGPT's "Wasted effort" line says not to repeat the same P4 table check. I found that out
after running it; this is therefore a low-value third confirmation, logged for honesty, and no
further P4 table re-runs should be done.
