# 2026-11-05 — Full PR #91 Yale manifest hash re-verification: execution

Precommitment: `logs/2026-11-05-yale-manifest-full-hash-verification-selfreview.md` (51c3c85),
committed before any code or fetch. Script `data/scripts/yale_manifest_hash_verify.py` and
workflow `.github/workflows/yale-manifest-hash-verify.yml` (3885367) were offline-tested
against a local HTTP server (one matching row, one deliberately wrong row, one missing row:
all reported correctly) before the Yale run.

**Run.** GitHub Actions run 41890135984 at repo HEAD 3885367, 2026-11-04 18:44:47–18:51:13 UTC.
Images hashed in memory only; nothing written to disk on the runner; no image bytes committed.
Results: `research/2026-11-05-yale-manifest-hash-verification.csv` (338bb15, committed by the runner).

**Result.**
- 213 rows fetched, every one on the first attempt (no retries, no network failures).
- 212/212 `ok` rows: HTTP 200, **sha256 identical to the manifest**, JPEG dimensions identical.
- Canvas 211 `[Spine]`: HTTP 403 again, as recorded in the manifest.
- Prediction (≥ 210/212 hashes, 212/212 dims, spine 403) **held**, at the top of its range.

**Meaning.** PR #91's manifest hashes and dimensions are now independently verified for all 212
retrievable canvases as of 2026-11-04 UTC (previously 10/212). Yale's 1,200-px IIIF derivatives
were byte-stable over the 14 days since ChatGPT's 2026-10-21 fetch. This verifies bytes only.
It does not verify PR #91's visual audit claims, and it says nothing about Yale reuse permission.
