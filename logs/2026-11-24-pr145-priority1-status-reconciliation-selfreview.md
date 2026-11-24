# Precommitment self-review — PR #145 Priority 1 status reconciliation (2026-11-24, Claude)

Written before running any check.

**What's known.** ChatGPT handoffs #158–#160 and the PR #145 laptop queue
(`data/jobs/laptop-queue.md` on the PR branch, head `26822ff`) list the
ten-folio Yale native retrieval as Priority 1, `QUEUED / NOT DISPATCHED`,
blocked by a Yale 403 and a missing laptop endpoint. Claude's own 24th-run
entry repeated that framing. But main already holds
`research/2026-11-01-ten-folio-native-receipt.csv` (Actions run 41657331236,
fetched 2026-11-03 14:48–14:49 UTC), the blank template, reader-1 cells
(2026-11-03), provisional reader-2 cells (2026-11-05) and the 213-row
manifest hash verification (2026-11-04). state.md lines 173/177/180/182
record these. The route to Yale was a GitHub-hosted Actions runner
(`.github/workflows/yale-ten-folio-fetch.yml`), not the cloud sandbox, which is
still refused (CONNECT 403 again this run).

**Not done yet.** Nobody has checked that the receipt on main is the output of
*exactly* the job PR #145 pins: same ten folios and canvases, and the same
expected 1200px SHA-256 values.

**Design (offline, no network, no images).** A stdlib script reads:
(1) the ten expected hashes from PR #145's queue table (`git show pr145:...`);
(2) the receipt on main; (3) the PR #91 manifest; (4) the 2026-11-04 manifest
hash-verification CSV. For each folio it checks: canvas id equals the receipt's
yale_image_id; PR-pinned hash equals receipt `manifest_1200_sha256`, receipt
`refetch_1200_sha256`, manifest CSV `sha256` and verification CSV `sha256`;
receipt `native_jpeg_ok`, `native_dims_match_info` and `manifest_1200_hash_match`
are True; error is empty. It also checks the PR's pinned blob SHAs for the
authorization file, manifest and fetch script against main and against the
receipt's HEAD-at-fetch commit `8ab27c9`. This is non-circular: the PR table was
typed by ChatGPT from the manifest, the receipt was written by a runner from
live Yale bytes, and the 11-04 verification was a separate run.

**Prediction.** 10/10 folios agree on all checks; the script blob may differ
between `8ab27c9` and the PR pin if the script was edited later.

**Honesty precommitment.** Report any mismatch as found. A pass shows only
that Priority 1 already ran, as pinned; it is not a reading. It does not
settle the open gate: an independent, non-Claude second reader. No workflow is
re-triggered, because the receipt exists and the script refuses to overwrite
it. Only the Director can update or merge PR #145.
