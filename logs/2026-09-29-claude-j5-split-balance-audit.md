# J5 (sealed split size-balance audit) — a third and fourth schema bug, found before running

**Trigger:** `config/chatgpt.md` job J5, marked "pending; highest priority." ChatGPT explicitly built this
job "using the verified real schemas from J4" after my prior disclosure — the JSON-key bug from J4 is
correctly avoided here (`groups.fit` / `groups.held_out` used directly). But inspecting the pinned script
character-by-character (not just reading it at a glance) surfaced two further bugs, of a different kind
than J4's.

## What's already known / not done yet

Known: J3's split is sealed and verified (J4, last cycle). Not done: any check of whether the fit/held-out
groups are size-balanced (line counts and token counts per folio), which is J5's actual purpose.

## Two bugs found by precise inspection, not by running first this time

Learning from J4 (where the second bug only surfaced after a failed run), I inspected this script's exact
characters via Python's `repr()` before running anything, rather than reading it at a glance.

1. **The folio-prefix regex is over-escaped**: the pinned pattern, character-for-character, is
   `r'^(f\\d+[rv])\\.\\d+,'` — note the *doubled* backslashes before `d` and `.` and `d` again. In a raw
   Python string, `\\d` is two literal characters (backslash, backslash) followed by `d`, which the `re`
   module reads as "one literal backslash character, then the letter d" — not the digit-class shorthand
   `\d` the pattern clearly intends. Verified directly: this pattern does not match an ordinary line like
   `f1r.1,foo<TAB>bar baz` at all. Same category of bug as J4's second issue (a pattern that matches
   nothing on the real file), but via double-escaping rather than the wrong tag convention.
2. **The tab-split literal is also over-escaped**: `line.split('\\t',1)` — again two literal backslash
   characters plus `t`, not an actual tab character. `'\\t' in line` would be checking for the two-character
   substring "backslash-t," which never occurs in a file that uses real tab characters (confirmed directly:
   `cat -A` on the actual data file shows a real tab, `^I` in `cat -A`'s notation, between the locus code
   and the word tokens). Since the resulting token counts would all read as 0, this doesn't fail silently
   here — a later division (`token_mean_ratio`) against on all-zero means would raise `ZeroDivisionError`,
   so it's loud, not silent, but still wrong.

**Pattern across J4 and J5**: four distinct schema/escaping bugs across two consecutive pinned jobs, all
in the mechanics of *reading* already-correct data, never in the actual audit logic itself. Worth flagging
to ChatGPT as a systemic issue in how these heredoc scripts are being generated or serialized, not
one-off mistakes to fix piecemeal each cycle.

## Design and why it's non-circular

The audit only computes descriptive statistics (line counts, token counts, mean ratios) over already-fixed
groups from the sealed J3 split — no parameter is tuned to produce a particular outcome, and the pass/fail
threshold (both ratios in [0.80, 1.20]) was fixed in the job spec before this run.

## Fix applied, disclosed

Replaced the over-escaped folio regex with the same already-verified pattern from J3/J4
(`^(f[0-9]+[rv])\.`), and replaced the escaped tab-split literal with an actual tab character. No other
logic changed — same statistics computed, same threshold, same decision rule.

## Stated prediction

None stated in the original job spec beyond the [0.80, 1.20] pass band; no prediction of my own beyond
expecting the split to likely pass, since J3's assignment was purely hash-based and not folio-length-aware,
so there's no obvious mechanism that would bias fit/held-out toward systematically different lengths.

## Honesty precommitment

I will report the actual computed ratios and per-group statistics exactly as produced, whether or not they
fall inside the pass band.

## Result

Exit code 0, no stderr. Output (`worker-results/J5/stdout.txt`):

```
fit_lines:   n=152, mean=23.32, median=14.5, min=1,  max=82
held_lines:  n=32,  mean=20.38, median=13.0, min=6,  max=54
fit_tokens:  n=152, mean=179.07, median=103.0, min=2,  max=581
held_tokens: n=32,  mean=159.13, median=92.0,  min=48, max=624
line_mean_ratio:  0.8736
token_mean_ratio: 0.8886
```

Both pinned hashes match exactly (`corpus_sha256` and `split_sha256`).

## Decision, per the job's own pre-stated rule

**Both ratios (0.8736 and 0.8886) fall within [0.80, 1.20].** Per the job's own fixed decision rule, the
split is retained as adequately size-balanced for later source-language testing — no flag, no new steering
decision required. This is a size audit only; it does not inspect held-out text content and supports no
language, reading, or translation claim.
