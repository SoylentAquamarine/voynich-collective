# J11 pin verification — 2026-11-22

Pinned repository commit: `32418169d1dd787108f85d2f718ec08901ec89b1`.
External code commit: `lrozanova/voynich-units@956a7c4fc39981f4d116fa3f4edfccce6d065571`.

| Path | Expected Git blob | Observed Git blob | Match |
|---|---|---|---|
| data/scripts/external_damping_ratio_ten_seed_anchors_check.py | 937315f46aee4bf6ea3b1c117dd82268e7ed23f2 | 937315f46aee4bf6ea3b1c117dd82268e7ed23f2 | yes |
| data/scripts/external_coupling_v2_section_aware_preregistered.py | eff4de3867872907a0497e5ffcf113cb26d8a16d | eff4de3867872907a0497e5ffcf113cb26d8a16d | yes |
| data/scripts/external_coupling_v2_section_varying_beta_check.py | 9e0f9cfa7ea00f0b96d223d3a015f97a8cd07022 | 9e0f9cfa7ea00f0b96d223d3a015f97a8cd07022 | yes |
| data/derived/external-coupling-v2-recalibrated-beta-check-summary.json | 30f4aae62300deda5016fe8e322fc08b77e23435 | 30f4aae62300deda5016fe8e322fc08b77e23435 | yes |
| data/derived/external-coupling-only-beta-curvature-check-summary.json | f00aad1691a00f02289aac930b2b74c07626cb3f | f00aad1691a00f02289aac930b2b74c07626cb3f | yes |
| data/derived/external-coupling-v2-limit-point-full-pipeline-more-seeds-check-summary.json | c553cbd3d9464d5545dca0133157567387b234ac | c553cbd3d9464d5545dca0133157567387b234ac | yes |
| data/derived/external-coupling-only-beta-limit-point-more-seeds-check-summary.json | f1fa5fd8481a1a37d68ea9053ceda2a793e3ada3 | f1fa5fd8481a1a37d68ea9053ceda2a793e3 | yes |

## Interpretation and limits
This is a Git-tree pin check, not execution of J11. The job remains QUEUED / NOT DISPATCHED; no laptop endpoint, receipt or output exists. J11 is a numerical damping-anchor check, not a text generator, and cannot establish a source-language reading or English translation. Keep the existing command, seeds, caps, checkpoints, expected outputs and one-retry rule unchanged.
