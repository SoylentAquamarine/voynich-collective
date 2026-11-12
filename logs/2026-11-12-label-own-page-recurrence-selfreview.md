# Self-review (precommitment): do label words recur in their own page's text?

Written 2026-11-12 (~07:00 UTC scheduled cycle), before any code for this test
exists or has run. Responds to Steering #53/#54's direction: move toward
semantic anchors; "a label-free, held-out semantic anchor must beat
frequency-matched and shuffled controls before it can constrain meaning";
stop adding same-corpus herbal subdivisions.

## What is known
- Image-linked anchors (ten-folio table) remain blocked: Yale IIIF hosts still
  return proxy CONNECT 403 this cycle (re-probed ~06:42 UTC).
- Prior label work (state.md, "Three independent representations of
  label-word recurrence...") tested whether a recurring label word predicts
  its clock position, its within-folio rank, or its page's illustration class.
  All three were null. None of them asked whether a label word recurs in the
  **running text of the page it labels** — the minimal text-only requirement
  for "label names something the page's text discusses". I found no prior
  log, script or report testing this (grep of logs/, data/scripts/,
  data/derived/ for label-vs-own-page text).
- Label loci in ZL3b (`desc[1] == 'L'`) carry ~1,200 word tokens: zodiac 350,
  pharmaceutical 250, cosmological 220, astronomical 150, biological 127,
  text-only 65, herbal 37 (counted this cycle with the existing tokenizer,
  only to size the design; no hit counts were looked at).

## Not done yet
- No hit counts, no null, nothing on RF1b.

## Design (frozen)
- Inputs: pinned `data/ZL3b-n.txt` and `data/RF1b-er.txt`; existing tokenizer
  `pr.words_of` with `<~>` as a word break (as in the conjugate-language
  script). Page headers (`$I`, `$L`) from ZL3b.
- Label words: word tokens from loci whose type letter is `L` (any of `@ + * = &`
  prefixes), length ≥ 3 characters, containing no `?` or `*`.
- Page text: all word tokens from the page's non-label loci (P, C, R ...).
- Eligible page: ≥ 1 label word and ≥ 20 text tokens.
- Statistic H = number of eligible label-word tokens whose exact word occurs
  at least once in their own page's text.
- Null (primary): the whole label-word multiset of each eligible page is moved
  as a block to a random eligible page of the **same illustration class `$I`**
  (permutation of label sets among same-class pages). This holds each label
  word's identity/frequency fixed and controls section-level shared
  vocabulary; only the page link is broken. 20,000 permutations, seed 20261112.
  One-sided p = (#null ≥ obs + 1)/(N + 1). Enrichment E = obs / null mean.
- Null (secondary): same, within `$I × $L` (Currier language) where `$L`
  exists; pages without `$L` permuted within `$I` among themselves.
- Secondary statistic: near-match H1 — label word (length ≥ 4) matches some own-page
  text word at Levenshtein distance ≤ 1 (exact counts too). Same nulls.
- Descriptive: per-class obs/null breakdown under the primary null.

## Why non-circular
No meaning, glyph value or language label is used to define a hit; Currier
`$L` only enters as a stricter null stratifier. Label-word identities and
page text are fixed; only the label↔page link is permuted, within section.

## Decision rule (frozen)
"Own-page anchor candidate" only if the primary null gives p < 0.01 in **both**
ZL3b and RF1b **and** the `$I×$L` null gives p < 0.05 in both. Anything else
is reported as "no own-page anchor at this resolution". Even a pass is a
structural label↔text link, not a reading: it identifies candidate word pairs
for later image-linked checking, nothing more.

## Prediction
Modest positive enrichment pooled (E ≈ 1.2–2) passing the rule, driven mainly
by pharmaceutical and biological pages; herbal under-powered (37 words).
Stated so it can fail.

## Honesty precommitment
Report the result whichever way it falls, including a failed prediction; no
redefinition of label/text/eligibility after seeing counts; any extra
analysis added later is labelled post hoc. Append to state.md, never
overwrite.
