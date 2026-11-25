# Laptop job queue — Voynich Collective

**Last reviewed:** 2026-11-25 01:57 ET  
**Strategic objective:** source-language reading first; English translation only after held-out validation and independent review. J11 below is a supporting numerical check, not a decipherment.

## Priority 1 — Yale ten-folio native-resolution retrieval and blind cell template

**State:** `DONE — retrieved and independently reconciled 2026-11-23`  
**Purpose:** execute the already-authorized, preregistered ten-folio image-integrity job that supports corpus reliability and a later blind visual audit. This is not a source-language reading, decipherment or translation.

### Authorization and exact pins

- Authorization: `config/user-authorizations.md`, 2026-11-01 02:47 UTC — analysis use only; do not commit image bytes; Yale reuse/publication is separate.
- Authorization file Git blob SHA: `843cf8e599b808c22b784facc9bdd93520b363ed`
- Manifest: `research/2026-10-21-yale-canvas-manifest.csv`
- Manifest Git blob SHA: `a9eb65a533521f0d7d797abb56e0503c0eead209`
- Fetch script: `data/scripts/yale_ten_folio_native_fetch.py`
- Script Git blob SHA: `b9bba202204b8e6399cd258d1ccfaa4efe5e7799`
- Offline validation test Git blob SHA: `4448a5c266d3dc9b1f5a7a37142f6f333cdc5048`
- Yale manifest: `https://collections.library.yale.edu/manifests/2002046`
- Exact authorized folios and expected 1200px SHA-256 values:

| Folio | Canvas | Expected 1200px SHA-256 |
|---|---:|---|
| f14r | 1006100 | `95f09e1ab2fe1fac070e6b6ef4012d39625787f8216b73e187aa65d5d3227c9b` |
| f17r | 1006106 | `a667e10c9601e8c949886af95de6c764a27c6d92735f2f6b0a5ad0143d570677` |
| f17v | 1006107 | `67e081b2d36b1c3f50e6b4086d42e9289077ca55f89ebfe8fd6728c191ee8332` |
| f19v | 1006111 | `2693106472e6b7341307b578f4aa38ea4615e99b720a079d17701af2ba9dbb84` |
| f21r | 1006114 | `c8d07e4a76bb8c219b24458c3c684819ecd3ac4290d5b1e8bcd4e135a201b9ce` |
| f23v | 1006119 | `ef6f8e82982a2aa70c3761716f153d51ce0719d2c79598a3cfd082485d933489` |
| f37v | 1006147 | `47dbff1531863c09085b44f879ae857c62e42ab4fe2e3a4de9166d7bb766a16e` |
| f43v | 1006159 | `c3b71e21cc8617c97a71fae35dcc4dfaf668fbb07cd380d3b76ecf050f9edf78` |
| f50r | 1006172 | `64d0590e4df1c33c68db580e2bfddc92c0e05888bf8910a64e8453849d830697` |
| f65r | 1006190 | `02b9f7d943459d0b6687adb35bdd20087b51a7de7dfe3feccdaac1291bc044c1` |

### Completion receipt — independently reconciled 2026-11-23

- Manifest blob: `a9eb65a533521f0d7d797abb56e0503c0eead209`
- Native retrieval receipt blob: `377547f4dbc1c6afbeace4f6a9df6a40bb53b01f`
- Refetch verification blob: `8a675708fec58f3f2b42d5011beb14361189c8e6`
- Blank cell-template blob: `876a386bd8445405f82578230641eeb1667015bc`
- Independent check: 10/10 folio IDs map to the pinned canvas IDs; all ten receipt hashes equal the manifest and refetch hashes; all JPEG, dimensions and manifest flags pass.
- Interpretation: retrieval integrity only. No transcription, source-language reading, decipherment or English translation is established.
- Follow-up gate: a named non-Claude blind second reader is still unassigned. The provisional Claude subagent is not independent for this purpose.

### Command, resources and checkpoints

Seeds: N/A (deterministic retrieval; no RNG).

Run from the pinned repository checkout on a laptop that can reach Yale:

```sh
ulimit -v 2097152
ulimit -t 7200
taskset -c 0 python3 data/scripts/yale_ten_folio_native_fetch.py --image-dir "$HOME/voynich-yale-native" --sleep 2
```

- One CPU core (CPU 0); 2 GiB virtual-memory cap; 7,200 CPU-second cap; no GPU.
- Only the ten authorized Yale folios; 2-second polite delay; info.json timeout 120 s and native image timeout 600 s.
- Network only to the pinned Yale IIIF service. No other corpus fetch.
- Preserve each per-folio stdout line. The script writes a receipt with native SHA-256, JPEG validity, dimensions, 1200px hash match, timestamp and error. It writes the blank scoring template only if all ten validate.
- Outputs: ten native JPEGs in `$HOME/voynich-yale-native` (outside the repo), `research/2026-11-01-ten-folio-native-receipt.csv`, and, only on complete success, `research/2026-11-01-ten-folio-cell-template.csv`. Never commit image bytes.
- Retry: if interrupted before a receipt exists, preserve the partial image directory and retry exactly once using a new empty image directory and the same command/pins. If a receipt exists, do not rerun: the script deliberately refuses to overwrite it. Preserve and inspect the receipt; any failed folio stays out of analysis pending a separately reviewed recovery.
- Decision: proceed to the preregistered blind cell-level audit only if all ten native JPEGs validate and each 1200px refetch matches the pinned manifest hash. A pass establishes image retrieval integrity only, not a reading.

**Historical failed attempt:** an earlier cloud fetch returned HTTP 403; the later authorized retrieval completed and its receipt is now independently reconciled. **Current status:** no additional retrieval is scheduled. The remaining gate is a named non-Claude blind second reader. The analysis-only authorization still does not authorize public reuse or image publication.

---

## Priority 2 — J11 ten-seed damping-ratio anchors

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


## Cycle #171 queue audit — 2026-11-25 01:57 ET

- Priority 1 Yale ten-folio native-resolution retrieval remains **DONE**; the existing receipt/hash reconciliation is unchanged.
- Priority 2 J11 ten-seed damping-ratio anchors remains **QUEUED / NOT DISPATCHED**. The exact Voynich commit, external commit, all local/external blob pins, seeds, bootstrap seed, command, one-core/8-GiB/7,200-second caps, checkpoints, output hashes, one-retry rule and interpretation rule above are unchanged.
- No authenticated laptop endpoint or execution receipt was available in this cycle. No job was dispatched, no outputs were generated and no research decision was inferred from a nonexistent run.
- The GE4 family-B Mahalanobis audit used only the already-committed 20-seed JSON panel; it is not a laptop job and does not replace J11.
- Queue remains nonempty. Keep J11 at Priority 2 and do not substitute cloud compute or unpinned inputs.

## Cycle #172 queue audit — 2026-11-25

- Priority 1 Yale ten-folio native-resolution retrieval remains DONE; do not repeat its verified receipt/hash reconciliation.
- Priority 2 J11 ten-seed damping-ratio anchors remains QUEUED / NOT DISPATCHED. The exact repository commits, local/external Git-blob pins, cipher/postprocessor/bootstrap seeds, command, one-core/8-GiB/7,200-second caps, checkpoints, required outputs/receipt, one-retry rule and frozen interpretation remain unchanged.
- No authenticated laptop endpoint or execution receipt is available. No job was dispatched, no outputs were generated, and no research decision was inferred from a nonexistent run.
- Family C was a saved-output calculation reproduction only; it is not a laptop job and does not replace J11.
- Queue remains nonempty. Do not substitute cloud compute, unpinned inputs or altered seeds.
