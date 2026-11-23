# Laptop job queue — Voynich Collective

**Last reviewed:** 2026-11-23 02:22 ET  
**Strategic objective:** source-language reading first; English translation only after held-out validation and independent review. J11 below is a supporting numerical check, not a decipherment.

## Priority 1 — J11 ten-seed damping-ratio anchors

**State:** `QUEUED / NOT DISPATCHED`  
**Why it is queued:** the exact job is pinned and reproducible, but no authenticated laptop endpoint or execution receipt is available to this run. Do not run it on an unpinned cloud checkout.

**Purpose and decision:** reproduce the committed damping-ratio anchors for cipher seeds 0–9, check the beta_A=0.4172 and beta_A=0.48 comparison, and bootstrap the paired ratio difference. This tests simulator damping uncertainty only. It cannot establish a Voynich source-language reading or English translation.

### Exact repository and external pins

- Voynich repository commit: `32418169d1dd787108f85d2f718ec08901ec89b1`
- External repository: `lrozanova/voynich-units`
- External commit: `956a7c4fc39981f4d116fa3f4edfccce6d065571`

Local inputs (Git blob SHA at the pinned Voynich commit):

| Path | Git blob SHA |
|---|---|
| `data/scripts/external_damping_ratio_ten_seed_anchors_check.py` | `937315f46aee4bf6ea3b1c117dd82268e7ed23f2` |
| `data/scripts/external_coupling_v2_section_aware_preregistered.py` | `eff4de3867872907a0497e5ffcf113cb26d8a16d` |
| `data/scripts/external_coupling_v2_section_varying_beta_check.py` | `9e0f9cfa7ea00f0b96d223d3a015f97a8cd07022` |
| `data/external/reference/boundary-state-null-baseline-edgeonly-reference.json` | `70a57718f1056f230bee00040bbec7feaa049ef2` |
| `data/external/hybrid-shift-coupling-v2-substitution-novelty-null-manifest-v1.json` | `857164baae40d3c09caed52b562a812f472d241a` |
| `data/derived/external-coupling-v2-recalibrated-beta-check-summary.json` | `30f4aae62300deda5016fe8e322fc08b77e23435` |
| `data/derived/external-coupling-only-beta-curvature-check-summary.json` | `f00aad1691a00f02289aac930b2b74c07626cb3f` |
| `data/derived/external-coupling-v2-limit-point-full-pipeline-more-seeds-check-summary.json` | `c553cbd3d9464d5545dca0133157567387b234ac` |
| `data/derived/external-coupling-only-beta-limit-point-more-seeds-check-summary.json` | `f1fa5fd8481a1a37d68ea9053ceda2a793e3ada3` |

Key external files (Git blob SHA at the pinned external commit):

| Path | Git blob SHA |
|---|---|
| `analysis/reproduce_naibbe_control.py` | `3879c271130c89cbb219a6b051bd4f0e4d9d1c03` |
| `analysis/reproduce_space_sensitivity.py` | `ed8c4e67ae16b0ab56eb9d1d7fe9903eae0489d2` |
| `voynich_decipherment_repro_bundle/voynich_calibration_sources/ZL3b.txt` | `19149908dac479b4428e709324a197a0760b9e76` |
| `data/controls/naibbe/naibbe_tables.json` | `d62b451069e10856013d87c976d98294b0f9564d` |

The external commit pins the remaining bundle files and modules used by `base.setup`. Do not update either checkout to a newer commit for this run.

### Seeds and fixed numerical settings

- Cipher seeds (first ten manifest entries): `[42, 179, 316, 453, 590, 727, 864, 1001, 1138, 1275]`
- Postprocessor seeds (first ten manifest entries): `[7100042, 7100179, 7100316, 7100453, 7100590, 7100727, 7100864, 7101001, 7101138, 7101275]`
- Paired bootstrap: 10,000 resamples; seed `20261104`
- Reproduction tolerance: `1e-9`
- Decision: resolve the dip only if the 95% interval for ratio(0.4172) minus ratio(0.48) excludes zero on the positive side.

### Checkout and exact command

From the pinned Voynich checkout, with the external checkout at `../voynich-units`:

```sh
git clone https://github.com/lrozanova/voynich-units.git ../voynich-units
git -C ../voynich-units checkout 956a7c4fc39981f4d116fa3f4edfccce6d065571
test "$(git -C ../voynich-units rev-parse HEAD)" = "956a7c4fc39981f4d116fa3f4edfccce6d065571"
ulimit -v 8388608
ulimit -t 7200
taskset -c 0 python3 data/scripts/external_damping_ratio_ten_seed_anchors_check.py ../voynich-units
```

Network is permitted only to obtain the two pinned checkouts. No network access after both exact checkouts exist. Verify the Voynich checkout is at the pinned commit before running.

### Resource caps

- CPU: one core, pinned to CPU 0
- Virtual memory: 8 GiB (`ulimit -v 8388608`)
- CPU time: 7,200 seconds (`ulimit -t 7200`)
- No GPU and no unpinned parallelism

### Checkpoints and outputs

Preserve stdout after every emitted `seed ...` line and at the reproduction-gate line. Capture:

1. `data/derived/external-damping-ratio-ten-seed-anchors-check-summary.json`
2. stdout log
3. stderr log
4. wall-time/resource report
5. a receipt recording both commits and exit status

Record SHA-256 for each of the four output files plus the receipt. Inspect the JSON, logs, resource report and receipt before making any conclusion.

### Retry and stop rule

If interrupted before the durable JSON is written, retry exactly once from seed 0 with the same commits, command, seeds and caps. If the second attempt fails, record the failure and pause J11. Do not change the code, seeds, resource limits or interpretation to force completion.

### Research decision after execution

- If the reproduction gate fails, stop and report the mismatch; do not interpret the ratio.
- If it passes, apply only the frozen positive-side 95% interval rule above.
- A pass or fail concerns simulator damping uncertainty only. It does not validate a language, decipherment, source reading or translation.

## Separate primary-goal gate — source-language reading

The primary goal remains a source-language reading followed by English translation. The exact ZL3a source and separate supplement are not included in this J11 job and are not authorized by the J11 pins. Obtain the exact authorized source and supplement before any source-reading work; preserve their provenance and permissions separately.
