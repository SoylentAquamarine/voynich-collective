# Independent recomputation — GE4 minim-atom saved-output margins
Date: 2026-11-26. This audit recomputes the published R3/R4 arithmetic from the saved JSON; it does not rerun the generator.

## Pinned inputs
- Script: data/scripts/ge4_levenshtein_minim_atoms.py, Git blob SHA 73d515b74a1b5e0d583065d972a0a080c2418020.
- Saved output: data/derived/ge4-levenshtein-minim-atoms.json, Git blob SHA d5099a1fb1b2413def4a860916aabdbf10dacb68.
- Saved design: seed 20261123, three toy seeds per rule family, 500 within-paragraph shuffles per profile, tolerance 0.10.

## Independent arithmetic
For each rule family and unit, I independently recalculated the d1 band as [min(seed ratios) − 0.10, max(seed ratios) + 0.10] and compared the saved Voynich ratio with that interval.

Family B, extended atoms:
- Seed d1 ratios: 1.3880704511, 1.4221839845, 1.3710013553.
- Extended band: [1.2710013553, 1.5221839845].
- Voynich d1: 1.2681341388.
- Outside margin: 0.0028672165.
- Observed three-seed range: 0.0511826292.

The saved binary rule therefore says “inconsistent,” but the miss is only about 5.6% of the observed three-seed range. This is a threshold-edge result, not a robust rejection of Family B on this statistic.

Family A, extended atoms:
- Seed d1 ratios: 1.4709513457, 1.4646445328, 1.5139537084.
- Extended band: [1.3646445328, 1.6139537084].
- Voynich d1: 1.2681341388.
- Outside margin: 0.0965103940.

R4, RF1b-er primary atoms:
- d1 difference: −0.0289079436.
- d2 difference: −0.0219384887.
- d3 difference: −0.0017508951.
- All are within the 0.10 tolerance; saved d1 p_upper = 0.001996008.

## Interpretation and limits
This reproduces the saved decision arithmetic, not the input generation or 500-shuffle calculation. The toy panel has only three seeds and one extended atom set. It does not establish a manuscript mechanism, source language, reading or English translation. Family B remains formally “inconsistent” under the frozen rule, but its d1 margin is too small relative to the observed seed range to present as a stable rejection.

## Decision
Do not extend synthetic-family enumeration without a preregistered adequacy threshold and a reason it changes the source-language research decision. Prioritize authorized ZL3a plus supplement and a non-Claude blind reader; keep J11 queued, not dispatched.
