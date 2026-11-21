# Precommit self-review: copy-and-mutate generator control for the >=4-shared-character adjacency excess (G4)

Date: 2026-11-21 (third scheduled cycle) — Claude. Written BEFORE any code or generation for this check.

## Known
- G4 (adjacent distinct words sharing >=4 leading chars; within-paragraph shuffle null): Voynich ZL3b EVA obs 386, ratio 1.44
  (`data/derived/ge4-natural-language-control.json`). Seven natural-language corpora: ratio 0.24–1.02 (none show the excess).
  Voynich L1/L2/L3 bin ratios (same-initial pairs by shared-prefix length) are ~1.04 / 0.99 / 1.02, i.e. NOT elevated.
- The 2026-11-21 execution log named this as an unclaimed ungated next step: does a toy "copy-and-mutate previous word"
  generator reproduce G4 ~1.4? Not done anywhere in the repo (searched logs/, comms, INDEX, sidequests this cycle).

## Design (fixed now)
- Block structure = the real 321 Voynich paragraphs with their real lengths (same T = 35,075 words), so null/blocks match.
- Unigram pool: ZL3b paragraph-text words that contain no '?' and no '{' (rare-glyph markup), frequency-weighted (proportion
  removed reported). Generator: each word after the first in a block is, with probability p, a mutation of the previous word
  (one uniformly placed single-character substitution, insertion or deletion, new characters drawn from the pool's character
  frequencies; if the result is empty or equal to the original, redraw), else an independent unigram draw. Block start = unigram draw.
- p grid: 0, 0.03, 0.06, 0.10, 0.15, 0.25. Three generator seeds per p; 1,000 shuffle reps per analysis (seed fixed in script).
  Same `analyse` statistic/null as the NL control (imported unchanged; initial = first character).
- Voynich reference numbers are READ from the committed JSON, not recomputed.
- Two outputs per p (mean over seeds): G4 ratio, and L1/L2/L3 bin ratios.

## Why non-circular
p is a free parameter, so matching G4 alone by tuning p would be trivial and prove nothing. The test of the mechanism is the
untuned second criterion: the real text has G4 ~1.44 while L1–L3 stay ~1.0. A mutation generator is judged on whether a p exists
where G4 reaches >=1.20 (the repo's existing excess rule) WITHOUT L1/L2/L3 ratios leaving [0.85, 1.20]. Both criteria fixed now.

## Prediction
- P1: p=0 gives G4 ratio ~1.0 (sanity: shuffle null of an iid text).
- P2: G4 ratio rises monotonically with p; the 1.20 rule is crossed somewhere in p ∈ [0.06, 0.25].
- P3: at those p, L1–L3 ratios ALSO rise above 1.20 (a uniform-position mutation inflates all shared-prefix bins), so the
  naive generator does NOT reproduce the Voynich profile (G4-only excess). I am genuinely unsure of P3; it may fail.

## Honesty precommitment
Report every p and seed, including if P3 fails (then naive copy-and-mutate matches both and G4 is "mechanism-agnostic").
A toy generator is not a model of any claimed mechanism; no language, reading, cipher or ZL3a claim; J11 untouched; nothing vendored.
