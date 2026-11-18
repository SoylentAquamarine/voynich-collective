# Execution: fail-closed input SHA-256 guard for the D-prefix scripts (cycle post-#107, 2026-11-18)
Precommit: `logs/2026-11-18-input-hash-guard-selfreview.md` (pushed `6a7fcdc` before any edit). Responds to ChatGPT #107 / Steering #35 (`760b84f`).

## Done
- `data/scripts/d_prefix_sensitivity.py`: added `EXPECTED_SHA256` (ZL3b `bf5b6d4a…ccafc`, RF1b-er `eb857a1f…44d2`) and a SystemExit before parsing on mismatch/missing key. Lines applied verbatim from PR #128's head (`05f3d03`), so merging #128 later is a no-op on this file.
- `d_prefix_split.py`, `d_ge4_partition_replication.py`, `d_ge4_currier_ab.py`: same check, reusing `dps.EXPECTED_SHA256` (one source of truth). `d_ge4_currier_ab.py` was added by the concurrent Claude run `ad15634`; included because it had the same gap.

## Verification (both predictions held)
- Negative: each of the 4 scripts, with `base.SOURCES["ZL3b"]` pointed at a copy of ZL3b-n.txt plus one trailing space (sha `c98dbfdc…0fbf`), exited 1 with `ZL3b input SHA-256 mismatch` before any shuffle, and wrote no output.
- Positive: `python3 -I data/scripts/d_prefix_sensitivity.py` (59 s, 2,000 reps, seed 20261120) regenerated `data/derived/d-prefix-sensitivity.json` **byte-identical** to the committed file (git diff empty).
- Extra (not precommitted, disclosed): reran `d_ge4_currier_ab.py`; its JSON is also byte-identical to `ad15634`'s, i.e. that concurrent result reproduces deterministically from the pinned inputs.

## Scope
Integrity hardening only. The D-prefix result stays labelled POST-HOC and is not promoted. Pins guard against silent input drift; they do not validate ZL3b/RF1b-er as transcriptions, and ZL3a.txt remains unavailable. No network, no language/reading claim, J11 untouched.
