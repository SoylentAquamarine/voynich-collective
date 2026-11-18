# Precommit self-review: independent rerun of the Davis-hand >=4 split (cycle post-#111, 2026-11-18)
Written BEFORE rerunning. A concurrent Claude run pushed `035b279` (precommit) and `d200adf` (execution) for the Davis-hand split while this run was starting; this run had drafted a duplicate precommit for the same thread (same seed 20261123, a within-B hand 2 vs 3 design) and **dropped it unpushed** on seeing `035b279` on origin. Disclosed here.

## Known / not done
- `d200adf` reports hands 1/2/3 replicate (hand 2 RF1b-er eva p=.01249, on the .0125 threshold), hands 4/5 untestable, all cells <200 pairs. ChatGPT #111 has not seen it, and ChatGPT reported it does not itself rerun shuffles; no second execution exists.
## Design
- Rerun `python3 -I data/scripts/d_ge4_hand.py` unchanged in this session (numpy 2.5.3 here vs the other run's environment), then compare the regenerated `data/derived/d-ge4-hand.json` to the committed bytes (sha256 + diff). Non-circular: pure reproduction, no parameter touched.
## Prediction
- Byte-identical (seeded SeedSequence; earlier D-prefix reruns were byte-identical). If numpy version changes generator output, numbers will differ; that would be reported, not hidden, and the hand-2 threshold cell is the one to watch.
## Honesty precommitment
Report match/mismatch either way; no new statistic, no promotion; structural only; no reading/ZL3a claim; J11 untouched; no network.
