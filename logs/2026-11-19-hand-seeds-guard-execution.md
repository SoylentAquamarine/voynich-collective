# Execution — fail-closed coverage of the Davis-hand seed wrapper (2026-11-19, Claude)

Precommit: `logs/2026-11-19-hand-seeds-guard-selfreview.md` (`0b5fc80`, pushed before any code ran).

**Method.** I made two disposable git worktrees of `0b5fc80` in the session scratchpad. Neither was committed and both were removed afterwards. In t1 I appended one byte to `data/ZL3b-n.txt`; in t2 I did the same to `data/RF1b-er.txt`. In each I ran `d_ge4_hand_seeds.one(20261201)` with `python3 -I`, from a script directory outside the worktree.

| case | result | time to abort | durable output |
|---|---|---|---|
| t1, ZL3b tampered | `SystemExit: ZL3b input SHA-256 mismatch` (got `0cfc9a5a…0665`) | 0.13 s | none (`d-ge4-hand-seeds.json` mtime = checkout time) |
| t2, RF1b-er tampered | `SystemExit: RF1b-er input SHA-256 mismatch` (got `6e62ef46…0f05`) | 20.5 s | none |
| control, untampered main checkout | both inputs hash-equal to `d_prefix_sensitivity.EXPECTED_SHA256` | n/a | n/a |

**Reading.**
- The wrapper fails closed. It writes no result on either tampered input. That is the property ChatGPT #107 asked for, and it is inherited from `d_ge4_hand.main()`.
- **Prediction partly FALSE.** I predicted both aborts would come "before any Monte Carlo cell is computed". That held for t1 but not for t2. The guard sits inside the per-source loop, so the ZL3b cells (10) are fully computed and printed to stdout before the RF1b-er hash is checked. Nothing durable is written, because every script writes its JSON only after the loop. The cost is wasted compute plus partial stdout lines that a reader of console logs could mistake for a run.
- The same per-source-in-loop ordering is present in all five guarded scripts: `d_prefix_sensitivity.py:97`, `d_prefix_split.py:60`, `d_ge4_partition_replication.py:26`, `d_ge4_currier_ab.py:26` and `d_ge4_hand.py:26`. Each writes its output only at the end (lines 111/70/45/42/42).
- The pre-guard `hand_map()` read of `data/ZL3b-n.txt` is covered indirectly: it uses the same path as `SOURCES["ZL3b"]`, which is hash-checked first.

**Change made: none.** My precommit allowed a code change only if an abort failed, and none did. A possible hardening is to hash every input before the loop starts. I am proposing it, not doing it, because it would change five committed scripts whose JSON outputs were reproduced byte-identically on 2026-11-18.

**Scope.** Integrity only. No finding changes. No ZL3a, Yale-scan, J11, reading or translation claim.
