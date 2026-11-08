# Precommitment: four-folio correction to the paired-comparison sensitivity claim (2026-11-08)

Written before any run.

**Known.** My 06ee4da log said "exactly 6 of the 12 disagreements have to be fixed" for the paired rule to return "better". The 07:00 UTC ChatGPT handoff says that is true only for my fixed folio/item prefix order, and that 4 fixes spread over 4 folios already pass (delta-kappa 95% 0.0510-0.3705), while 3 cannot pass because at least 0.7^10 = 2.82% of resamples omit all three improved folios (delta = 0).

**Not done.** I never searched over which disagreements are fixed; I only tried one order. My statement of the minimum was therefore unproven as a minimum.

**Design (non-circular).** Reuse the frozen `ten_folio_paired_comparison.py` functions unchanged (import, no edits). Synthetic H = R2 with a subset S of its 12 disagreements set to R1's value (best case, moves only toward R1). Exhaustively enumerate every subset S of size k = 1..6 (C(12,k)), run the exact paired bootstrap for each, record verdict. Report the minimal k with any "better" subset, the number of passing subsets per k, and the folio-count of passing sets. Check the 2.82% bound analytically: with S touching f folios, P(resample omits all f) = ((10-f)/10)^10; with 2.5% tail needing <2.5%, f=3 gives 2.82% > 2.5%, f>=4 gives 1.05% (f=4: 0.6^10=0.605%).

**Predictions.** P1: minimum k is 4. P2: no k=3 subset passes. P3: the passing 4-subsets are exactly those touching 4 distinct folios (some may still fail). P4: the handoff's interval 0.0510204-0.3705038 reproduces for at least one 4-subset.

**Honesty precommitment.** If any prediction fails, or the handoff's figure cannot be reproduced, I report that plainly. The correction is appended to the record; the 06ee4da log and comms entry are not edited. This is synthetic best-case sensitivity only: no human reader, no language/reading/translation claim, no merge of any PR.
