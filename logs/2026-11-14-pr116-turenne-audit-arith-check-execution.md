# Execution: arithmetic spot-check of PR #116 — 2026-11-14

Precommit: logs/2026-11-14-pr116-turenne-audit-arith-check-selfreview.md

Result (double-precision Python): 26*(1/26)^8 = 1.2450e-10 = 26^-7; 47*(1/47)^8 = 1.9739e-12 = 47^-7.
Both match PR #116 item 3 (1.245e-10; 1.974e-12). Prediction held. The audit's *arithmetic* is correct.

Not checked: whether the paper actually states 47 vs 26 as the audit says, the supplement, items 1,2,4,5, any raw corpus. Review-only; no merge of #116 is requested or performed here (merge decision remains the user's). Proposed follow-up (Director call, not started): inspect the supplement, then precommit the empirical initial-glyph null on pinned transcriptions with segmentation, section-specific frequencies and multiple-search correction, as ChatGPT proposed. No Yale access, nothing downloaded.
