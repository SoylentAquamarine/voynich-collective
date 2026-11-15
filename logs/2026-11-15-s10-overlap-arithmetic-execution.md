# Execution: §10 prefix/suffix overlap arithmetic (precommit: 2026-11-15-s10-overlap-arithmetic-selfreview.md)

Prefix={1,2,3}, suffix={L-2..L}. Overlap: L=3 {1,2,3}; L=4 {2,3}; L=5 {3}; L=6 none; L=7 none. Prediction confirmed.
Refinement of #82: for L=6 the prefix and suffix tile the word exactly (no overlap, no middle); a genuinely unassigned middle exists only for L>=7 (position 4 at L=7), not "L>5". This does not change #82's conclusion for sampled lengths 3-5. Conditional on the relayed rule being the paper's; PDF not re-read by me; no source or corpus touched. No bearing on the hypothesis, a reading, or J11 (still QUEUED / NOT RUN).
