# Precommit — parent-process hash preflight in `d_ge4_hand_seeds.py` (2026-11-19, Claude)

Written and pushed before the edit or any test run.

**Known.** `logs/2026-11-19-hash-preflight-verify-execution.md`: with a tampered input the CLI wrapper hangs (SystemExit inside Pool workers; `p.map` never returns). No JSON is written.

**Design.** One change: at the top of `main()` in `data/scripts/d_ge4_hand_seeds.py`, before `Pool(...)`, `import d_prefix_sensitivity as dps; dps.verify_inputs()`. Nothing else (seeds, n_procs handling, aggregation, output) changes. Not circular: the pins are the 2026-11-18 committed hashes; the tests are mechanical.

**Tests (scratch clone, never committed).** (a) RF1b-er and ZL3b-n one-byte tamper: CLI exits nonzero in < 5 s with one mismatch message, no cell line, no JSON change. (b) Untampered full CLI rerun: output byte-identical to committed `7eff12f2…7405`.

**Prediction.** (a) both exit in ~1 s; (b) byte-identical.

**Honesty.** If (b) differs I revert and report. Integrity only; no research claim.
