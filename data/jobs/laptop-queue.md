# Voynich laptop job queue

**Last reviewed:** 2026-11-27 01:58 ET  
**Primary objective:** source-language reading first; English translation only after held-out folio validation and independent review. J11 is a supporting simulator check, not a decipherment.

## Priority 1 — Yale ten-folio native retrieval

**Status:** DONE — independently reconciled 2026-11-23.  
**Authorization:** config/user-authorizations.md, 2026-11-01 02:47 UTC; analysis only, do not commit image bytes, Yale reuse/publication separate. Authorization blob: 843cf8e599b808c22b784facc9bdd93520b363ed.  
**Manifest:** research/2026-10-21-yale-canvas-manifest.csv; blob a9eb65a533521f0d7d797abb56e0503c0eead209.  
**Fetch script:** data/scripts/yale_ten_folio_native_fetch.py; blob b9bba202204b8e6399cd258d1ccfaa4efe5e7799.  
**Offline test:** blob 4448a5c266d3dc9b1f5a7a37142f6f333cdc5048.  
**Receipt:** blob 377547f4dbc1c6afbeace4f6a9df6a40bb53b01f; refetch verification blob 8a675708fec58f3f2b42d5011beb14361189c8e6; blank cell template blob 876a386bd8445405f82578230641eeb1667015bc. Ten folio/canvas/hash rows and completion checks remain in the cited manifest/receipt. Result is retrieval integrity only. A named non-Claude blind second reader is still missing.

No further Yale retrieval is scheduled. Do not commit image bytes or infer reading progress from retrieval integrity.

---

## Priority 2 — J11 ten-seed damping-ratio anchors

**Status:** QUEUED / NOT DISPATCHED. No authenticated laptop endpoint or execution receipt is available. Do not use unpinned cloud compute, GitHub Actions or a reimplementation as a workaround.

**Purpose:** rerun the preregistered simulator damping-anchor check for cipher seeds 0–9, verify committed rows, and bootstrap the ratio(0.4172) minus ratio(0.48). This concerns simulator uncertainty only, not manuscript meaning.

### Exact repository pins

- Voynich checkout commit: 32418169d1dd787108f85d2f718ec08901ec89b1.
- External checkout: lrozanova/voynich-units at commit 956a7c4fc39981f4d116fa3f4edfccce6d065571.
- External pin is carried forward from the precommitted queue; this cycle independently rechecked the local blobs, not the external checkout.

### Local pinned blobs (verified against current main)

| Path | Git blob SHA |
|---|---|
| data/scripts/external_damping_ratio_ten_seed_anchors_check.py | 937315f46aee4bf6ea3b1c117dd82268e7ed23f2 |
| data/scripts/external_coupling_v2_section_aware_preregistered.py | eff4de3867872907a0497e5ffcf113cb26d8a16d |
| data/scripts/external_coupling_v2_section_varying_beta_check.py | 9e0f9cfa7ea00f0b96d223d3a015f97a8cd07022 |
| data/external/reference/boundary-state-null-baseline-edgeonly-reference.json | 70a57718f1056f230bee00040bbec7feaa049ef2 |
| data/external/hybrid-shift-coupling-v2-substitution-novelty-null-manifest-v1.json | 857164baae40d3c09caed52b562a812f472d241a |
| data/derived/external-coupling-v2-recalibrated-beta-check-summary.json | 30f4aae62300deda5016fe8e322fc08b77e23435 |
| data/derived/external-coupling-only-beta-curvature-check-summary.json | f00aad1691a00f02289aac930b2b74c07626cb3f |
| data/derived/external-coupling-v2-limit-point-full-pipeline-more-seeds-check-summary.json | c553cbd3d9464d5545dca0133157567387b234ac |
| data/derived/external-coupling-only-beta-limit-point-more-seeds-check-summary.json | f1fa5fd8481a1a37d68ea9053ceda2a793e3ada3 |

### External pinned files (recorded at external commit; not re-fetched this cycle)

| Path | Git blob SHA |
|---|---|
| analysis/reproduce_naibbe_control.py | 3879c271130c89cbb219a6b051bd4f0e4d9d1c03 |
| analysis/reproduce_space_sensitivity.py | ed8c4e67ae16b0ab56eb9d1d7fe9903eae0489d2 |
| voynich_decipherment_repro_bundle/voynich_calibration_sources/ZL3b.txt | 19149908dac479b4428e709324a197a0760b9e76 |
| data/controls/naibbe/naibbe_tables.json | d62b451069e10856013d87c976d98294b0f9564d |

### Seeds and fixed numerical settings

- Cipher seeds: [42, 179, 316, 453, 590, 727, 864, 1001, 1138, 1275].
- Postprocessor seeds: [7100042, 7100179, 7100316, 7100453, 7100590, 7100727, 7100864, 7101001, 7101138, 7101275].
- Paired bootstrap: 10,000 resamples; RNG seed 20261104.
- Reproduction tolerance: 1e-9.
- Resolve the dip only if the 95% interval for ratio(0.4172) minus ratio(0.48) excludes zero on the positive side.

### Exact checkout and execution command

From the pinned Voynich checkout:

    git clone https://github.com/lrozanova/voynich-units.git ../voynich-units
    git -C ../voynich-units checkout 956a7c4fc39981f4d116fa3f4edfccce6d065571
    test "$(git -C ../voynich-units rev-parse HEAD)" = "956a7c4fc39981f4d116fa3f4edfccce6d065571"
    ulimit -v 8388608
    ulimit -t 7200
    taskset -c 0 python3 data/scripts/external_damping_ratio_ten_seed_anchors_check.py ../voynich-units

Verify the Voynich checkout is at 32418169d1dd787108f85d2f718ec08901ec89b1 before running. Network is allowed only to obtain the two exact pinned checkouts; no network after both are present.

### Resource caps

- One CPU core, pinned to CPU 0; no GPU.
- 8 GiB virtual memory (ulimit -v 8388608).
- 7,200 CPU seconds (ulimit -t 7200).
- No unpinned parallelism.

### Checkpoints and required outputs

Preserve stdout after every emitted seed line and at the reproduction-gate line. Capture:

1. data/derived/external-damping-ratio-ten-seed-anchors-check-summary.json
2. stdout log
3. stderr log
4. wall-time/resource report
5. receipt with both commits and exit status

Record SHA-256 for each output and the receipt. Inspect the JSON, logs, resource report and receipt before any conclusion.

### Retry and stop rule

If interrupted before the durable JSON is written, retry exactly once from seed 0 with identical commits, code, seeds and caps. If the second attempt fails, record it and pause J11. Do not change code, seeds, limits or interpretation. The 2026-11-05 attempt was refused before execution by the session permission layer; nothing ran and no output exists. Do not route around that refusal.

### Research decision

If reproduction fails, stop and report the mismatch. If it passes, apply only the frozen positive-side 95% interval rule. Either outcome concerns simulator damping only; it is not a source-language reading, language identification, decipherment or translation.

---

## Separate source-reading gate — not yet queued

Exact authorized ZL3a source and the separate supplement are still missing, as is a named non-Claude blind reader. Obtain authorization and exact source pins before source-reading work. English translation remains downstream.
