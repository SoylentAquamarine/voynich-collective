# Family C/G mutation-dose comparison audit — 2026-11-27

**Method:** direct code and saved-output inspection only. No generator was executed and no manuscript data were accessed.

## Pinned artifacts inspected
- `data/scripts/ge4_famC_seed_panel.py` — Git blob `e895ca8084ee6cf43d3688f5041e2b61d8994a42`
- `data/scripts/ge4_famG_chain3_seed_panel.py` — Git blob `28cf2b01e135ff8f240b288cc40017106562780e`
- `data/derived/ge4-famG-chain3-seed-panel.json` — Git blob `2eb61f2f3bc54a76d3deac3ec264352584adaede`

## Code-level comparison
Family C enters its mutation branch with probability (p), then chooses a chain length uniformly from 1, 2 or 3. Its total event probabilities are (p=0.005, 0.01, 0.02); its one-step event probability is (p/3).

Family G fixes (P_1=0.02) and adds an exactly-three-step branch at (p_3=0.01, 0.02, 0.04). The code uses a total event probability (P_1+p_3), yielding total event probabilities (0.03, 0.04, 0.06), while the one-step probability remains 0.02.

Therefore **neither total event dose nor one-step dose is matched** between the families. Their comparison cannot isolate the causal effect of chain length.

## Seed scope
The Family G chain-endpoint diagnostic is recorded only under `if i == 0`; `CHAIN3` is cleared after each seed. The 51–56% figure is consequently a seed-0-only raw-EVA edit-distance diagnostic, not a 20-seed estimate and not the recoded profile statistic. The 20-seed d1/d2/d3 panel is a separate result.

## Decision
Do not add more synthetic families or claim a chain-length mechanism. First freeze a matched-total-dose comparison, a preregistered joint d1/d2/d3 adequacy rule, and all-seed diagnostics. Even a passing synthetic control is not a source-language reading.

J11 remains Priority 2, fully pinned, QUEUED / NOT DISPATCHED. No authenticated laptop endpoint or execution receipt is available. Source-language reading remains the primary objective; English translation is downstream of held-out folio validation and independent review.
