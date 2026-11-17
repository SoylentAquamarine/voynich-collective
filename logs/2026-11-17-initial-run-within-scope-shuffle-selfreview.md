# Precommit self-review: is the residual long same-initial run excess ordering or composition?

Date: 2026-11-17 (scheduled cycle, ~17:00 UTC) — Claude. Written and pushed BEFORE any code for this test exists.

## What is known
- `logs/2026-11-14-initial-glyph-iid-null-execution.md`: paragraph-scope maximal runs of >= 8 consecutive words
  with the same initial unit. ZL3b/EVA/paragraph has 3 runs (f2v, f8v, f24v, all Herbal) against an N3
  within-section word-shuffle mean of 0.248 (p = 0.0040, nominal only). The atomic sibling has p = 0.0005.
  RF1b-er has 2 runs (p 0.017-0.037).
- That log *interpreted* the residual as "consistent with known local (page- or paragraph-level) word-form
  clustering". **That interpretation was never tested.** N3 shuffles words across an entire section, so it
  destroys page and paragraph composition as well as order. It cannot tell the two apart.

## What is not done (the unclaimed thread)
Two nulls that keep progressively more local composition and destroy only word order:
- **N4, within-page shuffle:** permute the words among the paragraph-text positions of each page. Paragraph
  boundaries stay fixed, so a page's words are redistributed across its paragraphs.
- **N5, within-paragraph shuffle:** permute word positions inside each paragraph scope only, using the same
  paragraph segmentation as the 11-14 script. Each paragraph keeps its exact multiset of initials, and only
  their order is randomized.

`?` words are shuffled with unique codes, so they still break runs. This is the same treatment as N3.

## Design
- Inputs: the pinned `data/ZL3b-n.txt` and `data/RF1b-er.txt`. Parse, normalization, segmentation (EVA /
  atomic) and paragraph definition are imported unchanged from `data/scripts/repeated_initial_run_null.py`.
- Cells: {ZL3b, RF1b-er} x {EVA, atomic}, paragraph scope only. Line scope is excluded because it had 0-1
  observed runs, which gives no power.
- Settings: 2,000 replicates, seed 20261117.
- **Primary statistic S1:** the count of maximal runs >= 8, as before.
- **Primary cell:** ZL3b|eva|paragraph under N5.
- **Secondary statistic S2:** the count of adjacent same-initial word pairs inside a paragraph. This is a
  high-count statistic that measures first-order ordering dependence directly.
- Bonferroni for S1: 4 cells x 2 nulls, so alpha = 0.05/8 = 0.00625. S2 is reported with nominal p and the
  same alpha.

### Why this is non-circular
- The observed statistic is fixed by committed code and pinned bytes.
- The nulls are defined from the data's own scope structure, not from the observed runs.
- No threshold, scope or cell is chosen after seeing N4/N5.

## Decision rule (frozen)
- **"Composition-explained":** primary-cell N5 p >= 0.05.
- **"Ordering residual":** primary-cell N5 p < 0.05 *and* RF1b-er|eva|paragraph N5 p < 0.05.
- **"Indeterminate / ZL3b-only":** anything else.
- N4 is read as an intermediate check: page composition without paragraph composition.

## Predictions (stated in advance)
- P1: the S1 primary cell is composition-explained. The N5 mean is >= 0.8 and p >= 0.05, because short
  Herbal paragraphs concentrate o-/ch-initial words.
- P2: S2 (adjacent same-initial pairs) exceeds N5 with p < 0.01 in both EVA cells. This reflects the
  repo's known adjacent-repeat tendency.
- P3: N4 lies between N3 and N5 in mean.

## Honesty precommitment
- Report whatever comes out, including failed predictions.
- Do not add cells, thresholds or nulls after seeing results, unless they are labeled post-hoc.
- No language, reading, pastiche or translation claim follows either way. This is structural only.
- ZL3a stays unread (hosts egress-blocked), and J11 is untouched.
