# 2026-11-25 — Post-hoc independent code audit: Family C/G mutation-rate mismatch

**Scope:** source-code inspection and arithmetic only. This was not precommitted, was not a generator rerun, and is not a manuscript reading.

## Exact inputs
- Family C: `data/scripts/ge4_famC_seed_panel.py`, Git blob `e895ca8084ee6cf43d3688f5041e2b61d8994a42`.
- Family G: `data/scripts/ge4_famG_chain3_seed_panel.py`, Git blob `28cf2b01e135ff8f240b288cc40017106562780e`.
- Family G saved panel: `data/derived/ge4-famG-chain3-seed-panel.json`, Git blob `2eb61f2f3bc54a76d3deac3ec264352584adaede`.
- Family G execution: `logs/2026-11-25-ge4-famG-chain3-mix-execution.md`.

## Reproduction
Family C draws one uniform u for each next word. If u < p, it mutates the predecessor and then chooses a chain length uniformly from {1,2,3}; otherwise it draws an unrestricted vocabulary word. Therefore p is the total mutation-event probability, and each chain length receives approximately p/3.

Family G instead fixes P1=0.02 and uses a separate p3 in {0.01,0.02,0.04}; if u < P1+p3, it mutates the predecessor, with one step when u < P1 and exactly three steps otherwise. The resulting total mutation-event probabilities are 0.03, 0.04 and 0.06.

| Family C total p | C single-step component | Family G total P1+p3 | G single-step component |
|---:|---:|---:|---:|
| 0.005 | 0.00167 | 0.03 | 0.02 |
| 0.010 | 0.00333 | 0.04 | 0.02 |
| 0.020 | 0.00667 | 0.06 | 0.02 |

At the closest cited C setting (p=.02), G's single-step rate is three times larger, and its total event rate is three times larger at p3=.04. At the lower G p3 settings the total rate is 1.5× or 2× C's maximum p, respectively. The comparison therefore changes mutation dose as well as chain-length mechanism.

## Decision and limits
The reported d1 overshoot is consistent with this rate mismatch; it cannot be attributed to the dedicated three-step mechanism alone. The saved G panel and Mahalanobis arithmetic are not invalidated, but the causal comparison is not dose-matched. The 51–56% chain-endpoint diagnostic in the execution log is explicitly seed-0-only, not a 20-seed estimate.

No script was executed, no seed was generated, no source image or ZL3a material was accessed, and no language or translation claim follows. Next experiment, if justified after source access: preregister a dose-matched control that holds total event rate constant while varying the chain-length mixture.