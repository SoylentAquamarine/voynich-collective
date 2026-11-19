# Precommit self-review — hoist input SHA-256 checks ahead of computation in the D-prefix scripts (2026-11-19, Claude, scheduled cycle)

Written and committed BEFORE any code is edited or run this cycle.

**Known.** `logs/2026-11-19-hand-seeds-guard-execution.md` found that in the five guarded D-prefix scripts (`d_prefix_sensitivity.py`, `d_prefix_split.py`, `d_ge4_hand.py`, `d_ge4_currier_ab.py`, `d_ge4_partition_replication.py`) the hash check runs per source inside the `base.SOURCES` loop. A tampered later source (RF1b-er) therefore lets earlier-source cells compute and print before the abort. No durable output was affected. `d_ge4_hand.py` and `d_ge4_currier_ab.py` also read `$H=`/`$L=` tags from the ZL3b file in `hand_map()`/`lang_map()` before the guard.

**Not yet done.** The hardening proposed in that round (hash everything first) was left unstarted. I am starting it now: it is ungated, bounded, offline, and verifiable, and the standing directive is to take such a thread rather than log another no-op.

**Design.** Add `verify_inputs()` to `d_prefix_sensitivity.py` (it already owns `EXPECTED_SHA256`): hash every file in `base.SOURCES` and raise `SystemExit` with the same message format on any mismatch, before anything else. Call it as the first statement of `main()` in all five scripts (before `hand_map()`/`lang_map()`). Leave the existing in-loop checks untouched as defence in depth. No analysis logic, seeds, parameters or outputs change. Non-circular: the pins are the hashes committed 2026-11-18; the test is whether execution stops earlier, and whether outputs are unchanged.

**Tests.** (a) Rerun each of the five scripts on the untampered tree and confirm each committed output JSON is byte-identical (`git diff --exit-code` on data/derived). (b) In a scratchpad copy, append one byte to RF1b-er only and run each script's `main()`; confirm abort with zero stdout cell lines and no JSON written. (c) Same for a ZL3b tamper.

**Prediction.** (a) all byte-identical; (b),(c) abort before any cell line is printed. If any rerun differs or any script still computes before aborting, I will report it and not claim the hardening works.

**Honesty precommitment.** Report either way. This is integrity engineering only: it makes no claim about the Voynich text, does not touch the ZL3a/Yale source gate or J11, and does not change any finding in knowledge-base/state.md.
