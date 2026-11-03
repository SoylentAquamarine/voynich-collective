# 2026-11-03 — f21r/f21v native-resolution registration: precommitment self-review

Written by Claude (scheduled cycle, ~18:50 UTC) before any code for this test was run and
before any native f21v or control image was fetched.

**Known.** The 1,200-px post-hoc, nonblind check in
`research/2026-10-21-outline-first-image-audit.md` (ChatGPT) found that a green-excess map of
the f21r left-margin region (x=65:245, y=960:1280 in a 1200x1696 frame) correlates r=0.878
with horizontally flipped f21v (dx=0, dy=10), 0.190 unflipped, and at most 0.340 flipped for
four controls (f20v, f22v, f23v, f37v). The 15:30 UTC entry in comms/FromClaudeToChatGPT.md
names the open step: "f21v is not in this retrieval, so the f21r/f21v registration needs a
separate preregistered fetch". The f21r native image (2649x3743, sha256 0d28a9ed...) is in the
ten-folio receipt; f21v and the controls have never been fetched at native resolution.

**Authorization.** config/user-authorizations.md, 2026-11-01 02:47 UTC: retrieving any of the
213 Yale canvases, including native resolution, for analysis; no image files committed. This
test fetches 11 native canvases plus their 1,200-px versions on a GitHub-hosted runner (the
route used by Actions run 41657331236), computes numbers there, and commits only a CSV of
correlations and input hashes. No images leave the runner; no transfer branch is used.

**Not done yet.** No native registration; no reproduction of the 1,200-px numbers by a second
implementation; only four controls.

**Design (frozen here).**
1. Reproduction check: an independent re-implementation (`data/scripts/f21_native_registration.py`)
   runs the published 1,200-px method on the 1,200-px Yale JPEGs (hashes must match the
   manifest). Resize to 1200x1696 (PIL bilinear), optional horizontal flip, green excess
   G-(R+B)/2, Gaussian sigma 3 px, f21r target x=65:245, y=960:1280, every 3rd pixel; for each
   comparison, dx in -60..80 and dy in -100..100 in 10-px steps, per-region z-normalisation,
   maximum Pearson r. Pass if f21v flipped is within 0.03 of 0.878 and unflipped within 0.03
   of 0.190. A fail is reported, and the native result is then labelled "different
   implementation", not a replication.
2. Native test: identical method with every pixel parameter multiplied by s = 2649/1200 (f21r
   native width / 1200); all images resized to f21r's native frame 2649x3743; sigma 3s,
   step round(3s), offsets round(-60s)..round(80s) and round(-100s)..round(100s) in steps of
   round(10s).
3. Controls, expanded and fixed now (nine versos, both orientations): f17v, f18v, f19v, f20v,
   f22v, f23v, f24v, f25v, f37v. Plus f21v unflipped. Nothing is added or dropped after results.
4. Decision rule: "replicates at native" iff f21v-flipped r >= 0.60 AND exceeds every control
   score (any orientation) by >= 0.20. Otherwise "does not replicate".

**Why non-circular (and its limits).** Region, method and decision thresholds come from the
earlier note and are frozen here before native data. It is still the same physical pages, and
the f21r region was chosen after someone looked at it, so this tests robustness to resolution
and to a wider control set; it is not independent discovery evidence. Interpretation limit:
f21v and f21r are the two sides of one leaf, while f20v is the facing page in the current
binding. A flipped-f21v match well above flipped-f20v favours a through-the-leaf image
(show-through / strike-through) over contact offset from the present facing page. It does not
settle mechanism, rebinding history, or chronology.

**Prediction.** Reproduction passes; native f21v flipped >= 0.80; maximum control <= 0.45;
"replicates at native".

**Honesty precommitment.** Report every number, including a failed reproduction or a failed
prediction. Make no claim about painter, paint date, plant identity, language or translation.
This is not a reader-2 score and does not touch the ten-folio cell template.
