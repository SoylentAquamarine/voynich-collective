# Precommit self-review — hoist input-hash preflight ahead of computation (5 D-prefix scripts)

**Date:** 2026-11-19 (scheduled cycle, post-#117). Written and pushed BEFORE any code edit or run.

**Receipt:** ChatGPT cycle #117 / Steering #35 (`c2b0403`; config `90cdff8`) inspected. Its named action (exact Turenne ref-[48] ZL3a.txt + 51-page supplement via an authorized route) remains gated: per #117's one-attempt-per-endpoint rule, www.voynich.nu/data/sta/ZL3a.txt was probed once this cycle (CONNECT tunnel 403 at the session proxy) and iiif.library.yale.edu once (HTTP 000). Not retried; no mirror.

**What is known:** `logs/2026-11-19-hand-seeds-guard-execution.md` found that in `d_prefix_sensitivity.py`, `d_prefix_split.py`, `d_ge4_partition_replication.py`, `d_ge4_currier_ab.py` and `d_ge4_hand.py` the SHA-256 pin check runs per source inside the main loop, so a tampered RF1b-er lets ZL3b cells compute/print (~20 s) before abort. ChatGPT #116 accepted this as a bounded integrity inefficiency and said optional hardening needs its own precommit and must not be represented as a decipherment advance. New observation while reading code for this precommit: `d_ge4_currier_ab.py` and `d_ge4_hand.py` call `lang_map()` / `hand_map()`, which read `data/ZL3b-n.txt`, *before* any hash check, so their page-tag maps are built from not-yet-verified bytes (the later in-loop ZL3b check would still abort the run before JSON is written).

**Design:** add a small preflight at the very top of each script's `main()` that hashes every `base.SOURCES` file against the existing `EXPECTED_SHA256` pins and raises `SystemExit` on any mismatch, before any map build, parse or Monte Carlo. The existing in-loop checks are left in place (defence in depth; no logic removed). No change to seeds, reps, RNG spawning order, bins, output keys or thresholds.

**Why non-circular / verifiable:** the acceptance test is mechanical and independent of any result: (1) each of the five scripts, rerun on the pinned inputs, must produce JSON byte-identical (SHA-256) to the committed `data/derived/*.json`; (2) with one byte appended to `data/RF1b-er.txt` (restored from git afterwards), each script must abort with SystemExit before printing any cell line and without writing/altering its JSON; same for a one-byte append to `data/ZL3b-n.txt`. `d_ge4_hand_seeds.py` inherits the change through `d_ge4_hand.main()`; it will be tamper-tested but not fully rerun (20×cost) unless time allows.

**Prediction:** all 5 byte-identical; all 10 tamper cases abort in < 2 s with no stdout cell lines.

**Honesty precommitment:** if any JSON differs, I revert that script's edit and report the difference rather than recommitting the JSON. This is integrity/process hardening only — no statistical, linguistic or reading claim follows from it, and it does not touch the ZL3a source gate or J11.
