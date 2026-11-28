# Family B saved-output panel-separation audit

**Date:** 2026-11-26 08:56 ET  
**Scope:** independent arithmetic and artifact-lineage check; no generator rerun, no manuscript reading.

## Pinned artifacts
- data/derived/ge4-levenshtein-minim-atoms.json — Git blob d5099a1fb1b2413def4a860916aabdbf10dacb68; seed 20261123, 500 null replicates, tolerance 0.10.
- data/scripts/ge4_levenshtein_profile.py — Git blob 71bf64960c7c0495ea590193b4e74387894af3d0; constants explicitly set NSEEDS=3.
- data/derived/ge4-famB-seed-panel.json — Git blob 3a085f5e7d228b12afe4b3250b73c465a2d1f2ff; 20-seed panel, 100 null replicates, d1 only.

## Independent recomputation
For the three B_p0.01 minim-atom seeds, extended d1 values span 1.371001–1.422184. With tolerance 0.10 the lower band edge is 1.271001, against the Voynich extended d1 target 1.268134, leaving a 0.002867 miss. Primary d1 misses by 0.015953. Extended d2 and d3 remain inside their respective tolerance bands.

The separate 20-seed d1-only panel at p=0.01 spans 1.283552–1.468871, with mean 1.396897 and SD 0.046980. Its recorded fraction within 0.10 is 0.30. The 20-seed panel is not the three-seed minim-atom test and does not supply a joint extended-atom d1/d2/d3 result.

## Interpretation
The 0.002867 result is a threshold-edge three-seed minim-atom sensitivity result. It must not be described as a 20-seed extended-atom finding. The separate 20-seed panel is d1-only and used 100 null replicates. Neither result is a source-language reading or translation. No generator code was executed and no manuscript or Yale image data was accessed.

## Decision
Keep synthetic enumeration paused until the Research Director freezes a joint d1/d2/d3 adequacy rule with seed count, atom set, null-replicate count and tolerance explicit.
