# Family C/G mutation-dose and seed-0 diagnostic audit — 2026-11-27

**Scope:** independent source-code and saved-output inspection only. No generator execution and no manuscript access.

## Pinned artifacts
- Family G generator: data/scripts/ge4_famG_chain3_seed_panel.py — Git blob 28cf2b01e135ff8f240b288cc40017106562780e.
- Family G saved panel: data/derived/ge4-famG-chain3-seed-panel.json — Git blob 2eb61f2f3bc54a76d3deac3ec264352584adaede.
- Family G execution log: logs/2026-11-25-ge4-famG-chain3-mix-execution.md — Git blob 0be307db7115cb17cb28c1a9f70ad896d00f514a.

## Findings
The Family G generator fixes P1=.02 and adds P3 in {.01,.02,.04}; each event uses either one mutation (u<P1) or three mutations (u>=P1 within the event interval). Family C's p is the total event probability and chain length is uniform on {1,2,3}. Therefore the C/G contrast changes both total event dose and the one-step dose; it does not isolate chain length.

The code appends chain endpoints to CHAIN3 for three-step events, but computes the diagnostic only inside if i == 0 in the 20-seed loop, then clears the list each iteration. The saved JSON confirms one diagnostic per P3 cell:
- P3=.01: n=324, exact edit-distance-3 fraction 0.5556
- P3=.02: n=706, fraction 0.5057
- P3=.04: n=1367, fraction 0.5457

These are seed-0-only raw EVA diagnostics, not 20-seed estimates. The profile panel itself contains 20 seed values per P3 cell. No source-language reading, language identification, decipherment or translation follows from this synthetic test.

## Decision
Do not add another family or repeat this diagnostic. Any causal mechanism test must match total event dose, vary only the chain-length mixture, preregister the joint d1/d2/d3 adequacy rule and report every seed. Source-language reading remains the primary goal; English translation is downstream.