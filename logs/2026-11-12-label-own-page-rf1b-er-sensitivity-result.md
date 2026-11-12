# Result: RF1b-er input sensitivity (precommit: `...rf1b-er-sensitivity-selfreview.md`)

Script `data/scripts/label_own_page_recurrence_rf1b_er.py` (wrapper; committed script untouched), output
`data/derived/label-own-page-recurrence-rf1b-er.json` (sha256 1637ad45...af7f4). Committed output (17ad330c...) unchanged.

- ZL3b half: identical to the committed run (53 pages, 1,054 label words, exact 114/88.4, p 0.016) — sanity check passed.
- RF1b-er: 52 eligible pages (H 3 instead of 4), 1,049 label words (978 len>=4).
  Primary within-$I exact 100 / 78.1 (E 1.28, p 0.038); Lev<=1 334 / 289.5 (p 0.028).
  Secondary $I x $L exact 100 / 94.3 (p 0.197); Lev<=1 334 / 321.2 (p 0.147).
- Frozen rule (primary p<0.01 in both, secondary p<0.05 in both): **not met** with RF1b-er either. Fails more clearly on RF.
- Prediction (same direction as ChatGPT's reproduction, ZL identical) **confirmed**. This exactly matches ChatGPT's independent
  52 / 1,049 figures.

Conclusion: the negative verdict is robust to the RF1b-e vs RF1b-er choice. This does not resolve whether "-er" in the precommit
was a typo; that stays with the Research Director. Nothing here identifies a label referent, plant, language or translation.
