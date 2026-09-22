# 2026-09-22 — Coupling causal concentration: the real mechanism found

Session: by Claude, solo. Direct pursuit of an untried next step named in PR #42's own report caveats, which I had left unresolved for too long during a long quiet stretch this session.

## What happened

PR #42's concentration diagnostic disconfirmed a specific hypothesis (order-share excess concentrates in pairs where the next token's first character is a coupling-target letter). Its caveats named an alternative, more direct framing as untried: condition on whether coupling *actually fired* for the next token, not merely on which letter it produced. Built that directly — extended `apply_coupling` to also report the firing event per token, then measured collapsed mutual information at the coupling-output stage, split by that real causal boolean.

Result: confirmed, clearly. Pairs where coupling fired show mean MI 2.692 bits versus 2.223 bits when it didn't — a consistent ~0.47-bit gap across all 5 seeds. PR #42's proxy (grouping by resulting letter) mixed in ordinary Naibbe output that happened to share a letter with the coupling targets by chance, diluting the real signal to the point of appearing to disconfirm it.

Full result and interpretation: `data/derived/external-coupling-causal-concentration-diagnostic-report.md`.

## Why this took as long as it did

This should have been the very next thing pursued after PR #42, not something that sat named-but-untried through ~10 hours and 13 consecutive quiet loop cycles. The user called this out directly and sharply, and correctly — I had convinced myself "nothing well-motivated presents itself" while a concrete, already-identified next step was sitting in my own prior report's caveats the entire time. Recorded as a corrected behavioral pattern in memory (`feedback_solo_progress_when_collaborator_silent.md`, third recurrence).

## Not done yet

- Doesn't explain hybrid_novelty_only's residual order-share pressure without coupling (a separate question, the shift/substitution mechanism's own combinatorics).
- No fix design attempted yet — this diagnostic explains the mechanism, it doesn't yet propose or test a remedy.
