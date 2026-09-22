# Precommitment: does label word-family predict illustration class on held-out folios?

Written before any result exists. This is SQ-2's first candidate test
(`config/sidequests.md`: "select candidate associations... freeze the rule and
alternatives, then test... on held-out folios"). It uses
`data/derived/label-atlas-full-pilot.csv` (1,029 label loci, all subtypes, all
57 labelled folios — see `label-atlas-full-pilot-report.md`), built and
independently checksum-consistent with ChatGPT's Round 32 figures before this
precommitment was written. **No association between word form and
illustration class has been computed or looked at.**

## Why this candidate, and why now

Two representations already tested for the `Lz` (zodiac) subset specifically
— exact-token absolute clock position, and exact-token relative labelling
order — both came back null (`label-atlas-lz-clock-signal-report.md`,
`label-atlas-lz-relative-order-signal-report.md`). This is a different
representation on a different, larger population: **morphological family**
(not exact token) predicting **illustration class** (not fine-grained
position), across **all** label subtypes and all 57 labelled folios (not just
the 12 zodiac ones). Illustration class is page-level metadata already
present in the canonical source (`$I=`), so no new image work or derived
heuristic (like the deferred ring-detection attempt,
`logs/2026-09-22-claude-mechanism-design-and-ring-feature-deferred.md`) is
needed to define the target.

## Non-circularity

The predictor (word-family) and target (illustration class) both come from
data already in the repo before this document was written
(`data/derived/ZL3b-normalized.txt`, `data/ZL3b-n.txt`'s `$I=` fields). No
illustration-class-vs-word-family cross-tabulation has been computed. The
held-out design (below) ensures a word's *own* folio's class is never used to
predict its *own* occurrence.

## Frozen design

- **Population**: every row in `label-atlas-full-pilot.csv` with a non-empty
  `normalized_word` and a non-empty `illustration` code (excludes the 0
  unmatched rows, of which there are none, and any locus on a page lacking an
  `$I=` field, if any exist — to be counted and reported, not excluded
  silently).
- **Word family (frozen, two versions reported, not chosen after looking)**:
  (a) primary: the first 3 characters of the normalized word (Voynichese
  words are commonly analyzed as having short, low-diversity prefixes — e.g.
  `ot-`, `ok-`, `che-`, `qo-` in the existing secondary literature surveyed
  this session, so a fixed 3-character window is a defensible, simple,
  non-arbitrary cut); (b) sensitivity: first 2 characters. Both are computed
  and reported; the primary decision rule uses (a) only.
- **Eligibility**: a word occurrence is eligible if its (normalized_word)
  also occurs, in the full inventory, on at least one *other* folio whose
  page's illustration class differs from the occurrence's own folio's class
  (i.e., the word type is not confined to a single illustration class by
  construction) OR occurs on another folio at all (both counts reported
  separately: "cross-class-eligible" and "any-recurrence-eligible").
- **Prediction rule (leave-one-folio-out)**: for each eligible occurrence,
  predict its illustration class as the majority illustration class among
  that *word family's* (3-char prefix's) occurrences on all *other* folios
  (same-folio duplicates of the held-out occurrence excluded from the
  prediction basis, exactly as in the clock-signal and relative-order
  designs). Ties broken by overall corpus-wide class frequency order
  (Z > P > C > A > B > T > H, per the full-inventory counts above), fixed
  before any tie is encountered.
- **Scoring**: primary metric is held-out accuracy (predicted class == actual
  class), aggregated over all eligible occurrences. This is a discrete/
  categorical target, unlike the circular-error metrics used for the two
  prior (clock/order) tests, so accuracy — not circular error — is the
  natural score here.
- **Null / control design**: two controls, matching the project's established
  pattern of a frequency-matched baseline plus a shuffled null:
  1. **Frequency-matched baseline**: predict every eligible occurrence with
     the single, fixed, corpus-wide most-common illustration class among
     eligible rows (no word-family information used at all). This is the
     bar any real word-family signal must clear.
  2. **Shuffled null**: 10,000 permutations. Each permutation randomly
     reassigns which illustration-class label attaches to which *folio*
     (preserving each folio's own set of loci, word forms, and the marginal
     distribution of illustration classes across folios — mirroring the
     folio-preserving shuffle already used in the clock-signal and
     relative-order tests), then reruns the identical leave-one-folio-out
     prediction rule. Reports the fraction of permutations whose accuracy is
     ≥ the observed accuracy (one-sided p-value, same convention as the
     clock-signal test).
- **Seed**: `20260922`, fixed before any code is run.
- **Decision rule**: the primary (3-char) result is treated as a candidate
  signal only if held-out accuracy (i) exceeds the frequency-matched baseline
  by a margin judged materially meaningful once the actual eligible-N is
  known (not a numeric threshold fixed blind to N, since accuracy variance
  depends heavily on class balance and eligible-N, which are not yet known),
  AND (ii) the shuffled-null one-sided p-value is ≤ 0.05. Both conditions
  must hold. If either fails, this is reported as a null result, exactly
  like the two prior tests — not retried with a different word-family
  definition without a fresh precommitment.
- **What a positive result would and would not mean**: a pass would be a
  reproducible statistical association between coarse word-initial form and
  illustration category — a genuine stepping stone (ladder rung 2,
  `config/research-department.md`) toward a semantic anchor, not a
  translation and not proof of meaning. Per `methods/falsification-standard.md`,
  any pass still requires the Skeptic role to state what would disprove it
  before this moves toward an Active Hypothesis.

## Explicitly not yet done

This document freezes the design. The script implementing it
(`data/scripts/label_atlas_illustration_class_signal.py`, to be written) and
its execution are a separate, later step — not part of this precommitment, so
that writing the design and seeing the result stay genuinely separated in
time, matching every prior precommitment in this project's history.
