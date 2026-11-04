# 2026-11-05 — Full PR #91 Yale manifest hash re-verification: precommitment self-review

Written by Claude (scheduled cycle, 2026-11-04 evening US / 2026-11-05 UTC) before any code for
this check was run and before any image for it was fetched.

**Known.** `research/2026-10-21-yale-canvas-manifest.csv` (PR #91, ChatGPT, merged) lists 213
canvases: 212 `ok` rows with a sha256, width and height of the 1200-px IIIF rendering, and one
`HTTP 403 (spine)` row (canvas 211). Claude checked its bookkeeping against the pinned folio
index on 2026-10-26 (213/213 order/label/object-id match) but did not re-fetch any bytes. The
ten-folio native kit (Actions run 41657331236) re-fetched the 1200-px rendering for 10 canvases
and all 10 matched. **202 manifest hashes have never been independently re-verified.**

**Authorization.** config/user-authorizations.md, 2026-11-01 02:47 UTC, which names
"verification of the PR #91 manifest hashes" explicitly. Analysis only; no image files are
committed. Same GitHub-runner route as previous Yale runs (the cloud sandbox cannot reach Yale).
Images are hashed in memory and never written to disk or transferred off the runner.

**Design (frozen).** One GitHub Actions run of `data/scripts/yale_manifest_hash_verify.py`:
for each of the 213 manifest rows, GET the row's `iiif_1200px_url` (1 s polite delay, up to
3 attempts on network error/5xx). Record HTTP status, sha256, byte length, JPEG SOF width and
height. Compare with the manifest: `hash_match`, `dims_match`, and for the spine row whether a
403 recurs. Output only `research/2026-11-05-yale-manifest-hash-verification.csv`.
Non-circular: the comparison target (manifest hashes) was produced by ChatGPT on 2026-10-21 in a
different environment; this fetch is independent and its code does not read any earlier receipt.

**Prediction.** ≥ 210/212 hash matches (IIIF 1200-px derivatives looked deterministic in the
10-canvas check), all 212 dims matching, spine still 403.

**Interpretation rules (frozen).** 212/212 → manifest hashes verified as of the run date.
Any mismatch is reported by canvas, with dims; a hash mismatch with matching dims is read as
"server re-encoded or changed derivative", not as a manifest error, unless dims also differ.
Network failures are reported as unverified, not as matches. No retry runs to "fix" mismatches.

**Honesty precommitment.** Report the counts as they come, including a failed prediction.
If the run fails outright, log that and do not reword it as partial success. Append to
state.md; never edit the 2026-10-26 entry.
