# 2026-09-21 — Solo self-review: hybrid shift+substitution novelty null design

Design: `data/external/hybrid-shift-substitution-novelty-null-manifest-v1.json`. First design in this project to combine two previously-independent mechanisms (boundary-shift from PR #34, bigram-conditional substitution from PR #30) into one, deliberately, rather than testing either alone.

## Why combine them, precisely

Boundary-shift alone is provably H1/H2-invariant but structurally capped near 63.8% hapax even at its own maximum dosage — a real, established ceiling (PR #34), not something more dosage can fix. Bigram-conditional substitution alone easily clears the hapax floor but costs H2, with the cost scaling with how much substitution volume is used (established across PRs #29/#30/#31/#32). The hybrid uses shift first to absorb as much hapax gain as its free capacity allows, and substitution only as a small top-up for whatever gap remains — the hope is most of the vocabulary growth costs nothing, and only a sliver needs the costly operation.

## Issues checked

**1. Manipulation-check scope, addressed explicitly rather than glossed over.** Boundary-shift alone is already known to fail its own isolated hapax manipulation check (PR #34). This design does not re-litigate that or pretend otherwise — it tests the *combined* shift+topup operation as a single novelty mechanism against baseline, which is the methodologically correct question for a design that's explicitly built as a combination rather than claiming either component works alone. The manifest states this reasoning directly rather than silently changing what "the novelty manipulation check" tests without comment.

**2. Pass ordering and eligibility, precisely specified.** Boundary-shift runs to completion first (identical mechanics to PR #34, at its own established nu_shift=1.0 ceiling — not re-tested as a free variable here, since that ceiling is already established and re-optimizing it would be redundant). The substitution top-up then scans the shift pass's *finished* output stream left to right, building its own `emitted` set progressively from empty (the same causal, left-to-right convention used in every prior design — never full-stream lookahead) — so its eligibility check ("is this token already a repeat, as far as the substitution pass itself has seen") is well-defined and consistent with established practice.

**3. Independence of frequency statistics.** The substitution pass builds its own unigram/bigram frequency tables fresh, scanning only what it has processed of the *shift pass's output* — it does not reuse or inherit anything from boundary-shift's internal state (which tracks no character-frequency statistics at all, only an emitted-string set). No circularity, no double-counting.

**4. Calibration discipline.** nu_sub is chosen as the *smallest* value landing hapax in the target band, deliberately minimizing use of the costly operation — consistent with the whole design's rationale. H1/H2/order are recorded during the pilot but explicitly not used to select nu_sub.

**5. Honest expectation.** This is not guaranteed to work. Three ways it could still fail, named in the manifest's honesty precommitment: the small substitution top-up could still cost enough H2 to fail; combining the two operations could reintroduce or worsen the order-share problem in a way neither showed alone; or some other interaction could still trip the manipulation check. All three will be reported plainly if they occur.

## Verdict

Accept the design as drafted. Proceeding to implement and pilot-calibrate `nu_sub`.

## Pilot results

3 seeds, `hybrid_novelty_only` config (beta=0, nu_shift=1.0 fixed), swept nu_sub in {0.01, 0.02, 0.03, 0.05, 0.08, 0.1}, selecting on hapax alone:

| nu_sub | hapax mean | H2 mean (recorded, not used for selection) | order mean (recorded, not used for selection) |
|---|---|---|---|
| 0.01 | 0.6467 (below floor) | 2.722 | 0.0219 |
| 0.02 | 0.6543 (in band) | 2.735 | 0.0220 |
| 0.03 | 0.6600 | 2.745 | 0.0206 |
| 0.05 | 0.6740 | 2.768 | 0.0199 |
| 0.08 | 0.6926 | 2.805 | 0.0181 |
| 0.10 | 0.7065 | 2.825 | 0.0181 |

**Frozen: nu_sub=0.02**, the smallest value landing hapax in-band. A visible temptation, disclosed rather than acted on: order looks more favorable (closer to or under the 2.0% ceiling) at higher nu_sub in this pilot's 3-seed sample, but the calibration rule is hapax-only, and selecting nu_sub to make order look better would be exactly the kind of outcome-driven parameter choice this project's discipline exists to prevent. Proceeding with nu_sub=0.02 regardless of how order turns out in the full run — if it fails, that is reported honestly, not fixed by quietly picking a different nu_sub after the fact.
