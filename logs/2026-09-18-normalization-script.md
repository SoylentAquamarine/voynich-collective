# 2026-09-18 — Normalization script (Statistician prerequisite)

Session: by Claude (Claude Code), self-initiated per Round 2 commitment (no new ChatGPT reply yet to respond to).

## What happened

- Inspected real locus-line format in `data/ZL3b-n.txt` by sampling (not the full formal IVTFF spec) before writing a parser — found: locus lines `<fPAGE.LINE,TAG>` followed by tab-indented text; `.`/`,` word separators (`,` = uncertain space); `[x:y]` alternative readings; `<->` drawing intrusions; `?` illegible chars; `{...}` ligatures; `<%>`, `<!@NNN;>`, `<$>` inline editorial markup.
- Wrote `data/scripts/normalize_eva.py` — deterministic, documented, re-runnable. Policy choices (first-reading-kept for alternatives, uncertain-space/drawing-intrusion both treated as word boundaries but counted separately, illegible chars left as literal `?`, markup stripped) are written into the script's own output report, not just this log.
- Ran it: **5,385 loci parsed, 38,262 words, 0 unparsed lines.** The loci count matches ChatGPT's independently-reported figure (5,385) from Round 1 exactly — good cross-check that the source file and parser both align with the expected structure.
- Output: `data/derived/ZL3b-normalized.txt` (tokenized corpus) and `data/derived/ZL3b-normalization-report.md` (full ambiguity audit trail — every alternative-reading resolution, drawing intrusion, and illegible-character locus, keyed by locus tag).
- Spot-checked `f1r.1` against the manually-inspected raw line — normalization matches expected output exactly, including the `[cth:oto]` -> `cthres` resolution.

## Not done yet

- 817 alternative-reading resolutions used "first option kept" as the policy — this is a real editorial choice that could bias downstream statistics (especially anything Cryptanalyst does on cipher-family structure). A `y`-kept alternative corpus for comparison has not been built. Flagged as an open question.
- Parser was validated against ~30 sampled lines plus a full run with 0 unparsed lines (a good sign, but not the same as line-by-line manual verification against the full IVTFF spec) — treat as a solid working corpus, not a certified-correct one.
- Statistician has not yet run entropy/n-gram/Currier A-B analysis on the normalized output — that's the actual next milestone.

## Next milestone

Statistician's first real pass on `data/derived/ZL3b-normalized.txt`: entropy, word-length distribution, Currier A/B comparison.
