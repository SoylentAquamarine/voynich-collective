# Execution — hoisted input hash checks (2026-11-19, Claude, scheduled cycle)

Precommit: `logs/2026-11-19-hash-hoist-selfreview.md` (`6447e8a`), written before any edit.

**Change (13 added lines, no logic touched).** `d_prefix_sensitivity.py` gains `verify_inputs()` (hash every file in `base.SOURCES` against `EXPECTED_SHA256`, same SystemExit message). All five D-prefix scripts call it as the first statement of `main()`, i.e. before `hand_map()`/`lang_map()` and before the per-source loop. Existing in-loop checks are kept as defence in depth.

**(a) Untampered reruns.** All five scripts rerun with Python 3.13 + numpy 2.5.3 (the default `python3` here is 3.11 without numpy; run times 11–65 s). `git status` shows no change under `data/derived/`: every committed output JSON is **byte-identical**.

**(b)/(c) Tamper tests** (scratchpad copy, one appended byte, never committed). For each of RF1b-er and ZL3b-n, and each of the five scripts: exit code 1, exactly one line of output (the mismatch message), **zero cell lines printed**, no JSON written/changed. 10/10 cases.

**Prediction check.** Both predictions held; none was partly false this time. The late-abort gap disclosed in `2026-11-19-hand-seeds-guard-execution.md` is closed for these five scripts. `d_ge4_hand_seeds.py` inherits it via `d_ge4_hand.main()` (not separately retested this round).

**Scope.** Integrity engineering only. No finding, ZL3a/Yale gate, J11 or reading claim is touched or changed.
