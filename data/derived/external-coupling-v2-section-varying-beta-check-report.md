# Section-varying-beta coupling-v2 check: correct-signed and overshooting, but the manipulation check fails

Design reasoning and honesty precommitment (written before this ran, including the fixed anchor-check
threshold): `logs/2026-09-26-claude-coupling-v2-section-varying-beta-selfreview.md`.
Script: `data/scripts/external_coupling_v2_section_varying_beta_check.py`.
Raw output: `data/derived/external-coupling-v2-section-varying-beta-check-summary.json`.

## Headline result

**Mixed: the design's own edge-gain-gap is correct-signed and overshoots the real target, but the
section-manipulation (anchor) check fails by the pre-fixed threshold — so the design result cannot be
cleanly attributed to the beta manipulation alone.**

Real Voynich edge-gain gap (A − B), computed fresh from `external_currier_ab_real_edge_gain_stats.py`'s
own output: **-0.1312 bits/boundary** (Currier A's real held-out edge gain is lower than B's).

| Config | beta_A | beta_B | Mean edge-gain-gap (A−B) | % of real gap | 3/3 pass six criteria |
|---|---:|---:|---:|---:|:---:|
| Anchor (uniform) | 0.5 | 0.5 | **-0.0557** | 42.5% | yes |
| Design | 0.2245 | 0.5 | -0.3070 | 233.9% | yes |

**Anchor check: FAIL.** The pre-fixed threshold (|gap| < 0.05 bits/boundary) was chosen before any
output existed. The anchor's actual mean gap, -0.0557, falls just outside it (individual seeds: -0.035,
-0.049, -0.083). This means that even at `coupling-v2`'s own unmodified, uniform primary configuration
(`beta_A = beta_B = 0.5`, no section-aware change of any kind), splitting the generated stream by real
Currier label and measuring each section's own held-out edge-gain already shows a non-negligible,
disclosed asymmetry — and, notably, it runs in the *same direction* as the real corpus's own asymmetry
(negative, A lower than B), not a random or opposite-signed artifact.

## Interpretation

Per this design's own precommitted discipline (and this project's standing practice for a failed
manipulation check, e.g. `coupling-v3`'s own `INVALID_CONSTRUCTION` verdict), **a failed anchor check
means the design result cannot be interpreted as a clean demonstration that lowering `beta_A` causes
the edge-gain-gap** — some or all of the observed gap could be inherited from whatever produces the
anchor's own already-nonzero split, not from the deliberate `beta` manipulation. The design result
itself is still reported honestly: correct sign, and overshooting the real magnitude by more than 2x
(233.9%), meaning if the mechanism does have real headroom here, a substantially milder `beta_A`
(between 0.2245 and 0.5) might land near the real target — but this is not claimed as a finding, since
the manipulation check that would let this be attributed to `beta` specifically did not clear.

**What produces the anchor's own bias is not established here.** A plausible candidate, disclosed as
a guess and not investigated further this cycle: Currier A and B differ in real line-length
distribution (already measured last cycle: A's mean line length is 6.82, B's is 9.30) and possibly in
how frequently the *boundary-shift* step (unchanged, uniform `nu_shift=1.0`, applied identically
regardless of section) finds eligible split points near a section boundary — the edge-gain criterion
depends on adjacent-token pairs within the wrapped line template, so differing line lengths alone could
produce a differential split effect even with completely uniform upstream parameters. This has not
been tested and is disclosed as speculation, not a finding.

**What this does and does not show:** this is one disclosed configuration (one beta pair, everything
else at existing primary values), not an exhaustive search, and per the precommitment it is not
retried with a different beta pair without a fresh precommitment that first addresses why the anchor
check fails. It does not show `beta` cannot construct the real edge-gain asymmetry — the correct sign
and overshooting magnitude are genuinely suggestive — only that this specific test cannot yet
attribute that outcome cleanly to `beta` alone, since the split itself is not neutral even without any
section-aware manipulation.

**Does not bear on `coupling-v2`'s own pooled six-criterion PASS**, which is unchanged (all six
criteria pass in every replicate of both configs tested here). **Does not identify a mechanism or bear
on the manuscript's actual origin**, per every other constructive-null result in this project's history.

## What remains open

Before any further `beta`-manipulation design, the anchor bias itself needs a diagnosis: is it a
line-length-driven boundary-shift artifact (testable by running `boundary-shift-v2` alone, uniform
`beta`, and checking whether *it* alone already produces a nonzero split — a cheap, targeted check that
was not run this cycle), or something else? Diagnosing this is a smaller, more targeted next step than
designing a new beta pair, and is the natural place to pick this thread back up.
