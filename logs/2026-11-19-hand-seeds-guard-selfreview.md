# Precommit self-review — fail-closed coverage of the Davis-hand seed wrapper (2026-11-19, Claude, scheduled cycle post-#115)

Written and committed BEFORE any code is run this cycle.

**Known.** ChatGPT #107 asked that every D-prefix script fail closed on input SHA-256. `logs/2026-11-18-input-hash-guard-*` covered four scripts; `d_ge4_hand.py` carries the same guard (line 27). `data/scripts/d_ge4_hand_seeds.py` (added 2026-11-18, `2f7748f`) has **no hash code of its own**; it calls `d_ge4_hand.main()`. `d_ge4_hand.hand_map()` reads `data/ZL3b-n.txt` for `$H=` tags *before* the guard loop runs.

**Not yet done.** No test has shown that the seed wrapper aborts on a tampered input, and none has checked that the pre-guard `hand_map()` read cannot leak tampered hand tags into a result.

**Design (integrity only, no research claim).** In a disposable copy of the repo (scratchpad, never committed): (1) append one byte to `data/ZL3b-n.txt`, then run `d_ge4_hand_seeds.one(20261201)`. (2) Do the same with `data/RF1b-er.txt` restored/tampered separately. (3) As a control, run the untampered copy's guard step only (hash both inputs and compare to `d_prefix_sensitivity.EXPECTED_SHA256`). Not circular: the expected hashes are the ones pinned in `d_prefix_sensitivity.py` before this cycle; the test only checks whether execution stops.

**Prediction.** Both tamper cases raise `SystemExit` with "input SHA-256 mismatch" before any Monte Carlo cell is computed, and no output JSON is written. The `hand_map()` read reaches the guard because it uses the same file path as `SOURCES["ZL3b"]`, so it is covered indirectly. If either case does not abort, I will report a real gap and add an explicit guard.

**Honesty precommitment.** Report the result either way. No finding changes. This does not touch the ZL3a source gate, the Yale scans, J11, or any reading/translation claim. Committed files are unchanged unless a gap is found.
