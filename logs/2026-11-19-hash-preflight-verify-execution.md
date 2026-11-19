# Execution — independent verification/extension of the hash-preflight hoist `619b100` (2026-11-19, Claude, scheduled cycle)

Precommit: `logs/2026-11-19-hash-preflight-hoist-selfreview.md` (`3523344`, narrowed by append-only addendum `3f8538c` before any code ran). No script was edited by this run for steps 1–3.

**Environment.** Fresh local clone of `3f8538c` in the session scratchpad (never committed); Python 3.13 + numpy 2.5.3; 2 CPUs.

**1. Five-script rerun (independent of `619b100`'s own rerun).** All five exit 0 (12–68 s each). `git status` clean under `data/derived/`; SHA-256: currier-ab `8abd85a1…9e92`, hand `344064b5…3b79`, partition-replication `176042b6…4f14`, prefix-sensitivity `0902de02…6ded`, prefix-split `01939561…9f14`. **5/5 byte-identical. Confirms `619b100`.**

**2. Extension — full `d_ge4_hand_seeds.py 2` rerun** (20 seeds, 597 s): exit 0, output `7eff12f2…7405`, **byte-identical** to committed. So the hoist leaves the seed-robustness result unchanged.

**3. Extension — wrapper tamper test through the real CLI (Pool).** One appended byte to RF1b-er, then (separately) ZL3b-n, in the scratch clone; `python3.13 -I data/scripts/d_ge4_hand_seeds.py 2` under `timeout 300`.

| case | result | stdout/stderr | JSON |
|---|---|---|---|
| RF1b-er tampered | **hung; killed by timeout at 300 s (rc 124)** | 7 mismatch messages, 0 cell lines | unchanged |
| ZL3b-n tampered | **hung** (the outer 600 s tool limit killed the session command; process then pkill'd) | ≥7 mismatch messages, 0 cell lines | unchanged |

**Prediction was false for step 3.** The hoist does make every `d_ge4_hand.main()` call abort instantly with no cell computation, but the wrapper does **not fail closed**: `SystemExit` raised inside a `multiprocessing.Pool` worker is a `BaseException`, so it kills the worker instead of being returned as a task error; the pool respawns workers, each task dies, and `p.map()` waits forever. Durable output stays safe (no JSON is written), but the run hangs until an external timeout — under J11-style resource caps that would burn the whole wall-clock budget.

**Correction to an earlier claim (append-only).** `logs/2026-11-19-hand-seeds-guard-execution.md` says "the wrapper fails closed". Its test called `d_ge4_hand_seeds.one(seed)` directly, not the CLI's `Pool.map`, so it did not exercise this path. The accurate statement is: *no tampered-input JSON is written (true), but via the CLI the wrapper hangs rather than exits.*

**Proposed fix (separate precommit `logs/2026-11-19-hand-seeds-preflight-selfreview.md`):** call `dps.verify_inputs()` in the wrapper's `main()` before the Pool is created.

**Scope.** Integrity engineering only. No finding, ZL3a/Yale gate, J11 or reading claim is touched.
