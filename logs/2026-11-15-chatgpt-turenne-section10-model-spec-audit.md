# Turenne §10 position-range audit

**Date:** 2026-11-15. **Source:** Nicolas Turenne, “A Generative Grammar Underlying the Voynich Manuscript, the Pastiche Hypothesis,” arXiv:2609.20835v1, main PDF, §10.1–10.5 (pp. 29–32).

## Directly checked definitions

The main PDF says generated word length L is sampled uniformly from {3,4,5}. It then defines:
- prefix positions i=1,2,3;
- suffix positions i=L−2,L−1,L;
- middle positions i=4,…,L−3 only if L>5.

## Mechanical consequence

For every sampled length, prefix and suffix ranges overlap:
- L=3: positions 1,2,3 are all both prefix and suffix;
- L=4: positions 2 and 3 are both prefix and suffix;
- L=5: position 3 is both prefix and suffix.

The stated middle range is never active for L∈{3,4,5}. Therefore, as written in the main PDF, the position-specific probability rule is not uniquely specified at overlapping positions unless a precedence or combination rule is supplied elsewhere. The high-probability middle set H is not used by any generated word under the stated length distribution.

## Limits and next evidence

This is a direct specification audit, not a rerun of Turenne's code or a reproduction of generated frequencies. The main PDF points to a supplementary algorithm on page 46, but that supplement was not available in the 37-page arXiv PDF reviewed here. It may resolve the ambiguity; do not call the model impossible or the pastiche hypothesis falsified until the supplement or executable implementation is checked.

The audit does not establish a source language, a manuscript reading, or an English translation. It does not alter the ZL3a source-version result or J11 queue.

**One next action:** obtain the referenced supplementary algorithm or author-provided executable, then verify how overlapping prefix/suffix positions are handled and whether H actually affects 3–5-character outputs.

Source links:
- https://arxiv.org/pdf/2609.20835
- https://arxiv.org/abs/2609.20835