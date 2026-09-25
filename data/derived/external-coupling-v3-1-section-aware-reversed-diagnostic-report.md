# Reversed-assignment section-aware coupling-v3.1 diagnostic: still negative, and the precommitted expectation was wrong

Design reasoning and honesty precommitment (written before this ran):
`logs/2026-09-25-claude-section-aware-coupling-v3-1-reversed-selfreview.md`.
Script: `data/scripts/external_coupling_v3_1_section_aware_reversed_diagnostic.py`.
Raw output: `data/derived/external-coupling-v3-1-section-aware-reversed-diagnostic-summary.json`.
First attempt (assignment not reversed) for comparison:
`data/derived/external-coupling-v3-1-section-aware-diagnostic-report.md`.

## Headline result

**Still negative, and *more* negative than the first attempt — the precommitted qualitative expectation was wrong.** Swapping which Currier section gets the stronger substitution top-up dosage (`nu_sub_A=0.01`, `nu_sub_B=0.02` — the exact reverse of the first attempt's `nu_sub_A=0.02`, `nu_sub_B=0.01`) produces a mean pooled character-bigram-entropy gap of **-0.0240 bits** across 5 seeds — still the *opposite* sign from the real Voynich Currier A/B gap (+0.278 bits), and now **-8.6%** of its magnitude (vs. -6.4% for the first, non-reversed assignment).

| Seed | A_H2 (bits) | B_H2 (bits) | Gap (A−B) | % of real gap (signed) |
|---:|---:|---:|---:|---:|
| 42 | 2.2262 | 2.2512 | -0.0250 | -9.0% |
| 179 | 2.2143 | 2.2328 | -0.0184 | -6.6% |
| 316 | 2.2268 | 2.2446 | -0.0178 | -6.4% |
| 453 | 2.2100 | 2.2433 | -0.0334 | -12.0% |
| 590 | 2.2121 | 2.2377 | -0.0256 | -9.2% |
| **Mean** | | | **-0.0240** | **-8.6%** |

Comparison across both assignments, same seeds, same everything else:

| Assignment | nu_sub_A | nu_sub_B | Mean gap (bits) | % of real gap |
|---|---:|---:|---:|---:|
| First attempt | 0.02 (stronger) | 0.01 | -0.0178 | -6.4% |
| **Reversed (this test)** | 0.01 | 0.02 (stronger) | **-0.0240** | **-8.6%** |

## Interpretation

The first attempt's report predicted, based on the observed direction of that one result, that reversing the assignment (weaker dosage to A) should push the gap toward the correct sign, because substitution activity was reasoned to lower a section's H2, and A was getting more of it. **This prediction was wrong.** Giving B the stronger dosage instead made B's H2 higher still, and the gap *more* negative, not less — meaning the section that receives more substitution top-up ends up with *lower* generated H2 in both directions tested, and the identity of which section that is (A or B) does not on its own explain the sign of the pooled gap.

This rules out the specific causal story the first report offered (assign more dosage to the wrong section) as the explanation for the wrong-signed result. A better-supported reading of both results together: under this section-varying mechanism, whichever section gets the *larger* `nu_sub` ends up with *lower* generated H2 than the other, essentially regardless of which real section (A or B) it is assigned to — i.e. the effect is dosage-driven, not section-identity-driven, and dosage differences of this size (0.01 vs 0.02) push the gap by roughly the same small amount (~0.018-0.033 bits) in the direction "more dosage = lower H2 for that section," independent of real A/B identity. Since the real gap requires A to have *higher* H2 than B, and there is no dosage assignment in this two-value grid where A receives *less* substitution than B and still comes out with lower H2 than B, this specific mechanism (fixed beta and nu_shift, section-varying nu_sub alone, using only these two already-frozen values) cannot express the correct-signed gap in either configuration.

**What this closes:** the two-value, two-assignment space named as available in the first attempt's own report is now exhausted — both assignments of `{0.01, 0.02}` have been tried, honestly, and both are wrong-signed. Per the precommitment in both self-review logs, this is not retried with a third dosage value or a varied beta without its own fresh precommitment.

**What this does not show:** that no configuration of this mechanism family could ever construct the real gap — a different dosage pair (not reused from an unrelated prior sensitivity grid), or varying beta by section as well, remain untested and would need genuinely new numbers, which this project's non-circularity discipline treats as a materially different, larger design requiring its own justification for why those specific new values are being chosen.

**Does not bear on coupling-v3.1's own already-established result** (six-criterion PASS, pooled, non-section-split — unchanged). **Does not identify a mechanism or bear on the manuscript's actual origin**, per every other constructive-null result in this project's history.

## What remains open

Whether a different dosage pair (not reused from `coupling-v2`'s existing grid, which only offers these two values) or a section-varying `beta` (not attempted in either test so far — both fixed beta at 0.15) could construct the real gap is untested. Both would require introducing genuinely new numbers rather than reusing an already-frozen pair, which is a materially different and larger design than either test run so far — it needs its own justification for why those specific values are chosen, not just a fresh precommitment on the existing two. This is named here as the next candidate but not designed or attempted in this diagnostic.
