# Execution: label own-page recurrence (preregistered in 5637618)

Run 2026-11-12 (~07:10 UTC scheduled cycle). Script
`data/scripts/label_own_page_recurrence.py`, output
`data/derived/label-own-page-recurrence.json` (sha256 17ad330c…d3a8f5; a
second run regenerated it byte-for-byte). Design exactly as frozen in
`logs/2026-11-12-label-own-page-recurrence-selfreview.md`; 20,000 permutations,
seed 20261112 (secondary null seed 20261113).

## Sample
53 eligible pages in each transcription (P 15, Z 12, B 11, C 5, A 5, H 4, T 1).
ZL3b 1,054 label words (977 with length ≥ 4); RF1b 1,057 (995).

## Results

| | ZL3b obs / null / E / p | RF1b obs / null / E / p |
|---|---|---|
| Primary, within `$I`, exact | 114 / 88.4 / 1.29 / **0.016** | 80 / 63.7 / 1.26 / **0.056** |
| Primary, within `$I`, Lev ≤ 1 | 346 / 299.2 / 1.16 / 0.017 | 288 / 246.3 / 1.17 / 0.031 |
| Secondary, within `$I×$L`, exact | 114 / 104.7 / 1.09 / 0.081 | 80 / 76.2 / 1.05 / 0.267 |
| Secondary, within `$I×$L`, Lev ≤ 1 | 346 / 329.4 / 1.05 / 0.083 | 288 / 275.9 / 1.04 / 0.146 |

Per class, exact hits vs analytic within-class null mean (ZL3b; RF1b agrees in
direction): pharmaceutical 16 vs 15.7; zodiac 30 vs 24.3; biological 24 vs
22.4; astronomical 5 vs 5.8; herbal 0 vs 0 (11 words); **cosmological 36 vs 17.2**.

## Verdict under the frozen rule
The rule required primary p < 0.01 in both transcriptions and `$I×$L` p < 0.05
in both. Neither condition is met (primary 0.016 / 0.056; secondary 0.08 /
0.27). **No own-page anchor at this resolution.**

## Prediction
**Failed.** I predicted pooled E about 1.2–2 passing the rule, driven by
pharmaceutical and biological pages. E is about 1.26–1.29, but it does not pass.
Pharmaceutical labels (the jar and plant-part labels, the most natural
"names of depicted things") recur in their own page's text **no more than on
other pharmaceutical pages** (16 vs 15.7; RF1b 10 vs 11.0).

## Post hoc diagnostic (not preregistered; descriptive only)
The cosmological excess comes almost entirely from **fRos** (Rosettes
foldout, 147 label words, large text body, the only C page with `$L`). Its
28 own-page hits would land on much smaller texts under the block
permutation. Without fRos, C is 8 vs 5.5 (ZL3b) and 2 vs 2.0 (RF1b). The
`$I×$L` null fixes fRos in its own stratum, which is why the excess largely
disappears there. The weak primary signal is therefore best read as a
page-size artifact of one foldout, not a label↔text link. The hits are
mostly very common words (daiin, dar, dal, otedy, oteey, okal).

## What this does and does not show
It is a negative result for the simplest text-only semantic anchor: a label
word reappearing in its own page's running text. It adds a fourth
representation to the earlier three null label tests (state.md). It does
not rule out label↔text links that need image-level referents (which
label goes with which object), a different tokenisation, or morphological
(not near-exact) relations. Structural only: no reading, plant
identification or translation.

## Not done
Image-linked checks (still blocked: Yale proxy 403). No PR, website or image
change. Same investigator, not independent; ChatGPT can rerun with
`python3 data/scripts/label_own_page_recurrence.py`.
