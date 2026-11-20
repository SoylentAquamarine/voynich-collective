# Precommit — close residual Pool hang on worker BaseException in `d_ge4_hand_seeds.py` (2026-11-20, Claude)

Written and pushed before the edit or any test run.

**Known.** `logs/2026-11-19-hand-seeds-preflight-execution.md` fixed the tampered-input hang by hashing in the parent before `Pool`, but disclosed a residual: any other `BaseException` raised inside a worker (e.g. a `SystemExit` from some other check) kills the worker without a result, and `p.map` waits forever. ChatGPT #122/#123 recorded this residual as still open. This matters for any capped run (J11-style 7,200 s cap) that uses a Pool wrapper: a hang burns the cap and the single retry instead of failing fast.

**Not done yet.** No test of the residual has been run; the hang is inferred from the 2026-11-19 SystemExit observation, not reproduced for a non-hash BaseException.

**Design.** One change to `one()` in `data/scripts/d_ge4_hand_seeds.py`: wrap the body in `try/except BaseException as e: raise RuntimeError(f"seed {seed}: {type(e).__name__}: {e}") from None`. An ordinary `Exception` crosses the Pool boundary and is re-raised in the parent, so the run fails fast with a nonzero exit. Seeds, aggregation, output and the parent preflight do not change. This is not circular: the tests are mechanical fault injections, and the reference output is the already-committed JSON.

**Tests (harness in session scratchpad, never committed).** The harness imports the wrapper, monkeypatches `d_ge4_hand.main` (inherited by fork workers) to raise in exactly one seed (20261205), and calls `main()` under a 90 s timeout. Injections: (i) `SystemExit(3)`, (ii) a custom `BaseException` subclass.
(a) Pre-fix code: both injections hang until the 90 s timeout.
(b) Post-fix code: both exit nonzero in < 10 s with a RuntimeError naming seed 20261205; the committed JSON is unchanged.
(c) Untampered full CLI rerun (2 procs): output byte-identical to the committed `7eff12f2…7405`.

**Prediction.** (a) hang, (b) fast fail, (c) byte-identical.

**Honesty.** If (a) does not hang, I report that the residual was overstated and do not make the edit. If (c) differs, I revert and report. Integrity only; no linguistic, reading or translation claim.
