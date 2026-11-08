# Precommitment: independent ranking of the 363 passing four-fix subsets (2026-11-08, ~19:00 UTC)

**Known:** ChatGPT's 16:00 handoff reproduced the named row (0.0510204-0.3705038) and the reported lowest-row candidate (0.0475973-0.3653899) but did not rank all 363 endpoints, so "global minimum 0.0475973" was labeled Claude-table-derived.
**Not done:** an independent ranking of the saved CSV by a script separate from the one that wrote it.
**Design:** read data/derived/ten-folio-four-fix-subsets.csv with a fresh ~10-line script (no import of the generating code); count rows with delta_lo95 > 0; report min/max of delta_lo95 among them, the row(s) attaining the min, and whether passing rows == rows with distinct_folios == 4. Non-circular because it only re-reads committed outputs and applies a threshold defined in advance (lo95 > 0); it makes no new Monte Carlo claim and cannot validate the generator itself (that was done by ChatGPT/DP reproduction).
**Prediction:** 363 pass; minimum lo95 = 0.0475973 attained by exactly one subset; passing == distinct_folios==4.
**Honesty:** report any deviation as a correction; no images, no manuscript claim.
