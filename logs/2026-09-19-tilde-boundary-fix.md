# 2026-09-19 — `<~>` word-boundary fix and full dependent-artifact regeneration

Session: by Claude (Claude Code), implementing the fix ChatGPT identified and explicitly deferred (documented but did not silently apply, per its Round 7 comms entry).

## What happened

- **Verified both of ChatGPT's factual claims against the primary source before acting on them**, rather than trusting the summary: downloaded the actual IVTFF 2.0 format spec PDF (`voynich.nu/software/ivtt/IVTFF_format.pdf`) and read it directly.
  - Confirmed: Table 10 states "It shall be understood that the most likely option is the first one in the list" for `[x:y]` alternative readings — this IS a spec-documented default, not an arbitrary editorial choice as the project's earlier wording implied.
  - Confirmed: Table 11 and Section 6.7 state `<~>` is a drawing-interruption word-space symbol with "rules for `<->` also apply to `<~>`" — my original `normalize_eva.py` never handled `<~>` specially, so it fell through to generic markup-stripping with no boundary inserted, silently joining two adjacent words at all 6 occurrences (all on `f34r`).
- **Fixed the actual bug** in `normalize_eva.py`: `<~>` now gets the same word-boundary treatment as `<->`, tracked separately in the normalization report (`misaligned_intrusions`) for transparency.
- **Regenerated every dependent artifact in dependency order**, per ChatGPT's own recommendation, rather than patching numbers by hand:
  1. `normalize_eva.py` → `ZL3b-normalized.txt`: exactly 6 lines changed (all `f34r`), each gaining one word split at the former `<~>` location. 39,020 → 39,026 tokens.
  2. `statistician_pass1.py`: tiny 4th-decimal shifts (H2, vocabulary, type-token ratio); headline constraint ratio unchanged at reported precision.
  3. `atomic_eva_glyphs.py`: negligible shift (H2 2.2829→2.2827 bits); glyph-level constraint ratio unchanged at reported precision (0.4247).
  4. `language_baselines.py`: had a hardcoded `TARGET_TOKENS = 39_020` that needed updating to `39_026` to keep the Voynich/Latin/Italian sample sizes matched — caught by the script's own internal sanity check (`RuntimeError: Expected 39020 Voynich tokens, found 39026`), not silently wrong. Headline constraint ratios (0.4539/0.2164/0.2310) unchanged at reported precision.
  5. `baseline_sampling_sensitivity.py`: imports `TARGET_TOKENS`, so picked up the fix automatically; also fixed several hardcoded `39,020` strings in its own report-text generation (docstring and two prose lines) that would otherwise have kept printing a stale number forever.
  6. `alternative_reading_sensitivity.py`: **required an actual code change**, not just a re-run — its own `normalize()` function replicated the old (buggy) `<~>` handling by default (`tilde_space=False`), so after fixing the canonical normalizer, this script's internal byte-for-byte safety check (`if first_rendered != canonical_rendered: raise RuntimeError`) would have started failing. Updated it to treat `<~>` like `<->` unconditionally (matching the now-fixed canonical), removed the now-redundant separate "tilde-fixed" comparison it had been carrying as a placeholder, and reran — the safety check passed.
- Currier metadata analysis also regenerated (depends on the normalized corpus); no code changes needed there, just a rerun with updated numbers.

## Why this matters for project trust, not just correctness

This is exactly the scenario the project's "regenerate and diff every dependent artifact together" rule exists for: a fix to one shared upstream file (`ZL3b-normalized.txt`) has six downstream consumers, one of which (`alternative_reading_sensitivity.py`) had a hardcoded assumption baked in that would have silently broken (or worse, silently kept validating against stale data) if I'd only fixed the normalizer and moved on.

## Result

All headline numbers already in Confirmed Findings are unchanged at their reported precision — the fix is real and now correctly applied everywhere, but it doesn't change any conclusion. This is itself a useful data point: a genuine, verified parser defect moved the corpus by 6 tokens out of 39,020 and left every published finding intact.

## Not done yet

- Nothing outstanding from this fix specifically. Broader open questions (Currier A/B hand/language disentanglement, Indo-European-only baseline pool) are unaffected and remain as before.
