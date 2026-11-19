# Execution — parent-process hash preflight in `d_ge4_hand_seeds.py` (2026-11-19, Claude)

Precommit: `logs/2026-11-19-hand-seeds-preflight-selfreview.md` (pushed in `3238a7c` before the edit).

**Change (2 lines).** `main()` now calls `d_prefix_sensitivity.verify_inputs()` before creating the `Pool`. Nothing else changed.

**(a) Tamper tests** (scratch clone, one appended byte, restored from git; CLI `python3.13 -I data/scripts/d_ge4_hand_seeds.py 2`):

| case | before (this cycle) | after |
|---|---|---|
| RF1b-er tampered | hung, killed at 300 s | rc 1 in 0.17 s, one mismatch line, 0 cell lines, JSON unchanged |
| ZL3b-n tampered | hung | rc 1 in 0.11 s, one mismatch line, 0 cell lines, JSON unchanged |

**(b) Untampered full rerun:** rc 0, 584 s, output sha256 `7eff12f2…7405`, **byte-identical** to committed.

**Prediction check.** Both held.

**Residual (disclosed, not fixed):** any *other* SystemExit/BaseException raised inside a worker would still hang `Pool.map`. Only the input-hash path is covered. Wrapping `one()` to convert BaseException to an ordinary exception would cover it generally. That would need its own precommit and has low value now.

**Scope.** Integrity only. No finding, ZL3a/Yale gate, J11 or reading claim changes.
