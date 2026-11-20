# Execution — residual Pool hang on worker BaseException in `d_ge4_hand_seeds.py` (2026-11-20, Claude)

Precommit: `logs/2026-11-20-pool-baseexception-selfreview.md` (`af11995`), with Addendum A (`1803c8e`) pushed before the second edit. Integrity only. This makes no linguistic, reading or translation claim and changes no finding.

**Harness** (session scratchpad, never committed). It imports the wrapper and monkeypatches `d_ge4_hand.main` (fork workers inherit the patch) so that seed 20261205 raises (i) `SystemExit(3)` or (ii) a custom `BaseException` subclass. In stub mode the other seeds return an empty result at once and the output path is redirected to the scratchpad. All runs used a separate scratch clone with 2 workers.

| Test | Code | Result |
|---|---|---|
| (a) real compute, both injections, 90 s cap | pre-fix | ran to the cap. Not decisive, since a full run takes ~584 s |
| (a) stub, both injections, 120 s cap | pre-fix | **hang** to the cap; the stub control (no injection) completes in 0.1 s |
| (b) stub, both injections | try/except only | `RuntimeError: seed 20261205: SystemExit: 3` / `Custom: injected` in 0.02 s |
| (b) real compute, both injections, 120 s cap | try/except only | **still running at the cap.** `Pool.map` waits for every chunk before it raises, so this is a late failure, not a fast one. Prediction (b) **false** for real compute |
| (b') real compute, both injections | + `imap_unordered` | nonzero exit with the RuntimeError after 91.4 s / 88.4 s (seed 20261205 starts after four seeds on two workers) |
| stub control | + `imap_unordered` | completes in 0.02 s |
| tamper RF1b-er (one appended byte), real CLI | final | `RF1b-er input SHA-256 mismatch`, 0.13 s (parent preflight unchanged) |
| (c) untampered full CLI rerun | final | 7 m 08 s, rc 0. `d-ge4-hand-seeds.json` is **byte-identical** (`7eff12f2…7405`) |

**Change** (`data/scripts/d_ge4_hand_seeds.py`): `one()` re-raises any `BaseException` as `RuntimeError("seed N: Type: msg")`, and `main()` uses `dict(p.imap_unordered(one, SEEDS))` instead of `p.map`. The output does not depend on result order.

**Verdict.** Prediction (a) held. Prediction (b) held in stub mode but was false with real compute until the precommitted addendum change. (b') and (c) held. The residual hang disclosed on 2026-11-19 and in ChatGPT #122/#123 is closed for this wrapper: a worker `BaseException` now fails within one seed's runtime, instead of hanging until a cap. `KeyboardInterrupt` in a worker is also converted, which is acceptable for a batch script. The J11 command does not use this wrapper, so the J11 pins are unaffected.
