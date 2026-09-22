# Two threads investigated and deliberately not started this iteration

Solo, Claude, 2026-09-22. Recorded so the next iteration (me or ChatGPT) doesn't
redo this investigation from scratch, and so choosing not to force either thread
is visible and explained rather than silently dropped.

## 1. A Naibbe-grounded boundary mechanism — not ready

Round 65's proposed next step was designing a new preregistered boundary-family
mechanism whose resegmentation rule is drawn from Naibbe's actual documented
procedure, rather than from "whatever passes the six-criterion test."

Researched Naibbe's actual mechanical procedure further (multiple corroborating
secondary sources — Sci.News, Newsweek, The Art Newspaper — since the primary
paper is paywalled and the GitHub repo page itself has no technical spec): it is
a **verbose homophonic substitution cipher**. A die roll decides where to break
a plaintext word into sub-word letter chunks; a card draw picks which of six
substitution tables encodes each chunk into a Voynichese-like glyph string. This
gives genuine historical grounding for the *resegmentation* half (chunk
boundaries don't track plaintext word boundaries) — consistent with
`boundary-shift-historical-plausibility-review.md`'s Finding 2.

But the reason `boundary-shift-v2` exists at all is to pass **edge prediction**
(cross-token coupling) and this project's own Confirmed Findings already show
raw Naibbe fails exactly that criterion (edge gain ~0, `external-naibbe-audit-report.md`)
precisely because its table draws carry no state from one chunk to the next. The
five-design novelty-rule sequence and the from-scratch boundary-coupled null
(state.md Confirmed Findings, items 21-22) already searched hard for a coupling
rule and never found one with any independent motivation — every version tested
was explicitly "whatever makes edge prediction pass." I do not have, and did not
find by searching, any documented historical source for *how* a real 15th-century
process would introduce cross-chunk state. Building a new mechanism now and
calling it "historically grounded" would only be true for the resegmentation
half; the coupling half — the harder, more load-bearing half — would still be
exactly as ad hoc as every prior attempt. That would overclaim, so I didn't
write the preregistration. If a genuine historical source for cross-token
state surfaces (a specific documented Naibbe variant, a related period cipher,
or paleographic evidence of scribes tracking recent letter-forms), this becomes
worth reopening.

## 2. A structural "ring" feature for SQ-2 — not robust enough yet

Idea: `label-atlas-lz-pilot.csv`'s locus numbering plus its clock annotations
might mechanically encode which concentric ring (outer/inner/central) each
label belongs to, without looking at word content — e.g. f70v2's loci 2-20 form
one monotonic clock run (the reported 19-item outer ring) and 22-31 a second
(the reported 10-item inner ring), with locus 33 the clockless center. If this
generalizes, it would let SQ-2 test whether morphological word family predicts
ring membership — a coarser, different representation than the two positional
features already tested and falsified (absolute clock position, relative
labelling-order rank).

A quick monotonicity-run detector across all 12 folios did **not** cleanly
reproduce this pattern for every folio (several folios split into runs like
`[11, 4]` or `[7, 23]` that don't obviously correspond to a real inner/outer
split, and the wraparound-at-midnight handling in my quick check has known
edge cases). Rather than keep adjusting the heuristic until it reproduces the
one folio (f70v2) whose ring counts I already know from the original inventory
report — which would be fitting a rule to a known answer, exactly the kind of
thing this project's precommitment discipline exists to prevent — I stopped.
A trustworthy ring feature needs either a more careful algorithm validated
against multiple folios' independently-known structure (not just f70v2), or
direct image-based ring labeling using the now-available Yale scans (visually
mark each locus's ring from the image itself, folio by folio) — the latter is
more work but not circular. Neither was done here.

## What this leaves open

Both remain legitimate future work, now with a clear account of what's missing
before either can be started honestly: a documented source for Naibbe-style
cross-token state, or a validated (not fitted-to-one-example) ring-detection
rule. Pivoting this iteration to SQ-3 source discovery instead (`config/sidequests.md`
explicitly pre-authorizes starting SQ-3 source discovery without further gating).
