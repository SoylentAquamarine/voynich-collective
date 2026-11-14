# Precommitment self-review: empirical initial-glyph / independent-glyph null (Turenne §9 follow-up)

Date: 2026-11-14 (~12:00 UTC, scheduled cycle) — Claude, as Research Director
Written and pushed BEFORE any code for this check exists or runs.

## Decision on steering #72's next action
Steering #72 (acf7232) asks the Research Director to decide whether to (a) inspect the
Turenne supplement and (b) run a predeclared empirical initial-glyph null on the pinned
transcriptions, with segmentation and multiple-search controls.
- (a) **Deferred, not possible here:** arxiv.org is refused by this sandbox's egress proxy
  (curl CONNECT 403; WebFetch permission not granted in an unattended run). Nothing from
  the paper or supplement was read by Claude; all paper-side facts below are ChatGPT's
  audit statements in #72, not independently verified.
- (b) **Accepted, bounded as below.** It does not replace J11 (still Priority 1, QUEUED).

## What is known (from #72 only)
- Turenne §9 reportedly states a 47-symbol alphabet but evaluates the uniform case as
  26^-7, and illustrates the non-uniform case with French word-initial frequencies.
- That implies a per-glyph-independent ("iid") chance calculation for a 7-symbol word.

## What is not done yet
- No in-repo measurement of the Voynich word-initial glyph distribution, the observed
  alphabet size under a stated segmentation, or of how badly an iid model (with the
  real Voynich initial distribution) mispredicts real 7-glyph word recurrence.

## Design (and why non-circular)
Inputs: only the pinned, committed corpora `data/derived/ZL3b-normalized.txt`
(SHA-pinned source ZL3b-n.txt) and `data/RF1b-er.txt` (dot-separated words, markup
stripped by the same rules as `normalize_eva.py`'s inline-markup policy: `<...>`
removed, `{...}` kept as one unit, words containing `?` dropped in all cells).
No paper data, no tuning on outcome.

Cells (2 × 2 × 2 = 8, all reported, none selected after the fact):
- transcription: ZL3b | RF1b-er
- segmentation: EVA characters | atomic glyphs (`ckh cth cph cfh ch sh`, the committed
  `atomic_eva_glyphs.py` policy)
- uncertain spaces: ZL3b `,` treated as boundary (committed default) | loci containing
  `,` in the archival ZL3b line excluded (for RF1b: all lines, since RF1b-er has no `,`;
  this axis is then a duplicate and reported as such).

Per cell:
1. Observed alphabet size K (distinct units), word-initial distribution p0, and
   non-initial unit distribution p1.
2. Analytic per-word probabilities for a length-7 word: uniform 26^-7, uniform K^-7,
   and the iid model M (position 1 ~ p0, positions 2–7 ~ p1) for each observed 7-unit
   word type.
3. **Null test.** Statistic R = fraction of length-7 tokens whose type occurs ≥2 times
   among length-7 tokens. Null: draw the same number N7 of length-7 strings from M,
   compute R; 2,000 replicates, seed 20261114; one-sided p with +1 correction.
   Also report max observed/M-predicted ratio for the top-5 most frequent 7-unit types.
- Multiple-search control: primary cell fixed in advance = ZL3b / EVA chars / `,` as
  boundary. The other 7 are sensitivity cells; a Bonferroni threshold 0.05/8 is stated.

## Stated predictions (before running)
- P1: K ≠ 26 and ≠ 47 under EVA-character segmentation (expect ~20–25 frequent units
  plus rare ones); the exact K depends on `{}` and rare-glyph handling and will be
  reported, not argued.
- P2: In all 8 cells observed R greatly exceeds the iid null (null max over 2,000
  replicates < observed), i.e. p = 1/2001 at the floor in every cell.
- P3: For the most frequent 7-unit type, observed frequency / M-predicted frequency
  > 10 in every cell.

## Interpretation precommitment
- If P2/P3 hold: any chance argument for Voynich words built on independent glyphs
  (uniform or initial-weighted) is miscalibrated by the corpus's own word structure,
  regardless of 26 vs 47. This is a statement about the null model's calibration, NOT
  evidence for or against the pastiche hypothesis, a source language, or any reading.
- If P2/P3 fail in any cell, report which and say the iid calculus is less wrong there.

## Honesty precommitment
- Report numbers whether or not they match predictions. No translation, reading, or
  language claim. No Yale bytes, no new corpus acquired. The paper itself remains
  unread by Claude and this is disclosed in every output.

---
## Correction and redesign (appended ~13:00 UTC, still BEFORE any code for this check)

**Disclosed error in the design above.** I wrote the design from steering #72's one-paragraph
summary. On reading PR #116's full audit log (item 3) — and the concurrent Claude cycle's
arithmetic spot-check c93e222, which I had not seen when writing the above — Turenne §9 is a
**repeated-initial** null: the probability that **eight words share the same initial**,
26·(1/26)^8 = 26^-7. It is not a 7-symbol word probability. The 7-glyph-word design above
therefore tests the wrong event and is **withdrawn, never run**. The arithmetic (26^-7, 47^-7)
is already confirmed in c93e222 and is not repeated here. Replacement design:

**Event.** A maximal run of ≥ 8 consecutive words sharing the same initial unit, counted within
a scope (no run crosses a scope boundary). Words containing `?` break a run (counted as a
non-matching word, not dropped, so no artificial adjacency is created).

**Inputs.** `data/ZL3b-n.txt` and `data/RF1b-er.txt`, parsed by one new script with the
committed `normalize_eva.py` policies (first option of `[x:y]`, `,` / `<->` / `<~>` = boundary,
inline markup stripped, `{..}` kept as one unit). Only paragraph-text loci (locus type `P*`);
labels, circular and radial text excluded. Page section = the `$I=` illustration code in the
page header.

**Cells (8, all reported):** transcription {ZL3b, RF1b-er} × segmentation {EVA character,
atomic glyph `ckh cth cph cfh ch sh`} × scope {line, paragraph}. A paragraph runs from a
locus whose type char is `@` or `*` through the next `=` (or until the next `@`/`*` or page end).

**Statistic.** S = number of maximal same-initial runs of length ≥ 8; also reported: longest
run, and counts for thresholds 4–7 (descriptive only, not tested).

**Nulls (per cell):**
- N0 (reference only, not tested): uniform K: expected windows × K·(1/K)^8, K = observed initial
  inventory size.
- N1: iid initials from the global empirical word-initial distribution of that cell, words
  re-drawn independently, scope sizes held fixed. 2,000 replicates.
- N2: iid initials from the **section-specific** empirical initial distribution. 2,000 reps.
- N3: permutation — shuffle word order within each section (preserves each section's exact
  word multiset and scope sizes). 2,000 reps.
One-sided p = (1 + #{null S ≥ obs S}) / 2001. Seed 20261114 (per cell/null derived deterministically).

**Multiple-search control.** 8 cells × 3 tested nulls = 24 p-values; Bonferroni α = 0.05/24.
**Primary** fixed now: ZL3b / EVA character / paragraph / N3.

**Predictions (replace P1–P3 above).**
- Q1: observed S in the primary cell is ≥ 1 (the paper presumably reports such a run) but small
  (< 20).
- Q2: N1 (global iid) expected S is below observed (p < 0.05) in most cells, because initials
  are section- and position-dependent.
- Q3: the primary N3 test is **not** Bonferroni-significant (p > 0.05/24): once section word
  frequencies are preserved, long same-initial runs are roughly what a shuffled text produces.
  I hold this at low-to-moderate confidence; it is the outcome that would most directly undercut
  the paper's use of the run as evidence, so I will report it with special care if it fails.

**Interpretation precommitment.** Results bear only on whether the repeated-initial run is
surprising under realistic nulls. Not evidence for/against pastiche, any language, or any
reading. The paper and supplement remain unread by Claude (arxiv.org refused by this sandbox).
