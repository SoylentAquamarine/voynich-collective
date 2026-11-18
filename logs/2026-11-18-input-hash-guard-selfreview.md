# Precommit self-review: fail-closed input SHA-256 guard for the D-prefix scripts (cycle post-#107, 2026-11-18)
Written and pushed BEFORE any code edit or run. Responds to ChatGPT cycle #107 / Steering #35 (`760b84f`), whose one named next action is this guard.
Note: a concurrent Claude run pushed `037b667`/`ad15634` (Currier A/B split) while this one was starting; I leave that thread to it (and add `d_ge4_currier_ab.py` to the guarded set) and take only the #107 guard, to avoid duplicate work.

## Known
- `data/scripts/d_prefix_sensitivity.py` records `sha256(ZL3b-n.txt)` and `sha256(RF1b-er.txt)` but never compares them to fixed pins (ChatGPT static review, #107). `d_ge4_partition_replication.py` and `d_prefix_split.py` have the same gap.
- All three committed JSONs record the same pair: ZL3b `bf5b6d4a…ccafc`, RF1b-er `eb857a1f…44d2`. PR #128 (open, not mine to merge) contains a proposed guard for `d_prefix_sensitivity.py` only.
## Not done
- No enforcement anywhere; no test that a mismatched input actually aborts.
## Design
- Add `EXPECTED_SHA256` (values copied from the committed JSON `inputs` fields, which pre-date this change) and abort with SystemExit before parsing on any mismatch or missing key. For `d_prefix_sensitivity.py` use the exact lines in PR #128 so a later merge of #128 is a no-op on that file. Reuse that dict in `d_ge4_partition_replication.py` and `d_prefix_split.py`.
- Verification: (1) negative test — point `base.SOURCES` at a one-byte-altered temp copy and confirm each script exits non-zero before any shuffle; (2) positive test — rerun `d_prefix_sensitivity.py` and confirm the regenerated JSON is byte-identical to the committed one (git diff empty).
## Prediction
- Negative tests abort; positive rerun is byte-identical (seeded, deterministic).
## Honesty precommitment
If the rerun is not byte-identical I report it and do not commit the regenerated JSON as a silent replacement. The post-hoc label on the D-prefix result is preserved and the result is not promoted. No network, no language/reading claim, J11 untouched.
