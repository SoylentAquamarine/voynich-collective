# SQ-2: label word-family vs. illustration class (held-out, family-3char primary)

Script: [`data/scripts/label_atlas_illustration_class_signal.py`](../scripts/label_atlas_illustration_class_signal.py)
Precommitment: [`logs/2026-09-22-claude-sq2-illustration-class-precommitment.md`](../../logs/2026-09-22-claude-sq2-illustration-class-precommitment.md)
Data: [`label-atlas-illustration-class-signal.json`](label-atlas-illustration-class-signal.json)

## Result: NULL

Implemented exactly as frozen before this script existed. Leave-one-folio-out
prediction: for each eligible label-word occurrence, predict its page's
illustration class from the majority class among same-family (first-N-
character prefix) occurrences on *other* folios, scored as accuracy against
a frequency-matched baseline and a 10,000-permutation folio-class
shuffle null (seed 20260922).

| Metric | Primary (3-char family) | Sensitivity (2-char family) |
|---|---:|---:|
| Distinct families | 263 | 96 |
| Eligible occurrences (any recurrence) | 438 | 438 |
| ...of which cross-class-eligible | 400 | 400 |
| Observed held-out accuracy | 0.3265 | 0.3014 |
| Frequency-matched baseline accuracy | 0.3059 (always predicting `Z`) | 0.3059 (always predicting `Z`) |
| Shuffled-null mean accuracy | 0.1840 | 0.1876 |
| Shuffled-null 95% CI | [0.0936, 0.3014] | [0.0731, 0.3402] |
| One-sided p-value (null ≥ observed) | 0.0102 | 0.0689 |

**Decision rule** (primary/3-char only, frozen in advance): pass requires
observed accuracy to exceed the frequency-matched baseline by a materially
meaningful margin AND the shuffled-null one-sided p-value to be ≤ 0.05.

The mechanical half of that rule (accuracy > baseline, p ≤ 0.05) **passes**:
observed accuracy exceeds the baseline by 0.0205 absolute
(6.7% relative), and p = 0.0102.

## Interpretation — why this is reported as NULL, not a mechanical pass

The precommitment deliberately left "materially meaningful margin" for
judgment once the real N and class balance were known, rather than a
threshold fixed blind to them, specifically to avoid a marginal result being
waved through on a technicality. Applying that judgment here, openly:

1. **The margin is small.** 0.0205 absolute on a ~31%-accuracy base
   (6.7% relative) is not a large effect, especially with
   7 unevenly-sized classes and 438
   eligible occurrences.
2. **The shuffled-null p-value is not testing the comparison that matters
   most.** It tests whether real-label family-vote accuracy beats
   *randomly permuted* folio-class assignment — and it should, because
   real illustration classes are not randomly distributed across folios to
   begin with (the frequency-matched baseline itself, 0.3059,
   is already far above the null mean, 0.1840,
   using no word-family information at all). A low p-value against *that*
   null is compatible with "illustration class correlates with which
   words recur at all" rather than "word-initial family specifically
   carries class information" — the two are not the same claim, and this
   design's null does not cleanly separate them.
3. **The 2-character sensitivity check does not confirm the primary
   result** — this is the most direct evidence against treating the 3-char
   result as real. Sensitivity observed accuracy (0.3014)
   is *below* its own baseline (0.3059),
   and its p-value (0.0689) misses the 0.05
   threshold. A genuine morphological signal at 3 characters would be
   expected to at least partially survive at 2 characters, not flip sign.

None of this was decided after comparing family-length options to find the
best result — both lengths were frozen and run once, per the precommitment,
and this interpretation applies the reserved judgment clause to the primary
length's own result plus its own named sensitivity check, not a search
across alternatives.

**Conclusion: reported as NULL.** This is effectively a third null
result in the SQ-1/SQ-2 label-recurrence line, after absolute clock position
and relative labelling order (both also null). It does not mean recurring
labels carry no information at all — the elevated frequency-matched baseline
shows real, non-random structure in *which* folios share recurring
vocabulary — only that coarse word-initial family specifically does not
predict illustration class under this held-out design, on top of the two
positional representations already ruled out. Per the precommitment, this is
not retried with a different word-family definition without a fresh
precommitment.

## Non-circularity and honesty check

This script was written and run in the same session as, but strictly after,
the frozen precommitment above. No word-family/illustration-class
cross-tabulation was computed before the precommitment was written. The
family-length choice (3 characters primary, 2 as a named sensitivity, not a
free parameter swept for the best result), eligibility rule, tie-break order,
and decision thresholds all match the precommitment text verbatim -- none
were adjusted after seeing this result.
