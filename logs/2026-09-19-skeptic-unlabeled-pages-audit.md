# 2026-09-19 — Skeptic audit of the unlabeled-Currier-pages investigation

Session: by Claude (Claude Code), reviewing ChatGPT's answer to the long-standing "why do 30 pages lack a Currier A/B label" open question — the first image-based (not pure-text-statistics) piece of work in this project.

## What happened

- **Verified the copyright/licensing claim before treating the committed images as safe.** Didn't just trust `docs/assets/manuscript/README.md`'s "public domain" claim — navigated to the actual Wikimedia Commons file page for one of the five images and confirmed the PD-Art tag directly: a faithful photographic reproduction of a public-domain (15th century) work of art, sourced from Beinecke Library. Legitimate to have committed to a public repo.
- Read `data/scripts/unlabeled_currier_pages.py`: reuses `$I`/`$L`/`$H`/`$Q` fields straight from the canonical raw file, counts IVTFF locus-type descriptors (paragraph/label/radial/circular), joins already-canonical normalized token counts — no new external downloads, no inference of a missing `$L` value anywhere in the code.
- **Independently re-ran the script** (no downloads needed, so this was fast): exact structural match on the full JSON summary, including the complete 30-page inventory table. Fifth exact independent reproduction from this project in two days.
- **Spot-checked the image-based claims myself**, since re-running code can't verify a visual description the way it verifies a computation. Looked at two of the five committed scans directly:
  - `f65v`: report claims "intact herbal illustration with two short body-text blocks; neither a foldout nor visibly damaged." Confirmed exactly — full-page plant illustration, two clearly legible text blocks beneath it, no damage or foldout visible.
  - `f70v`: report claims "a zodiac roundel dominated by labels around figures." Confirmed exactly — a central goat/ram figure surrounded by concentric rings of labeled nude figures, no paragraph text block at all, consistent with the inventory's reported "L:30, C:3" locus counts for that page.

## Assessment

The core finding is well-supported and represents genuine progress: the old "likely foldouts/damaged" guess for the 30 unlabeled pages doesn't hold up — 26 of 30 form one continuous hand-4 diagram sequence (92.6% of unlabeled tokens), and the pages are dominated by label/radial/circular loci (12.6% paragraph text) rather than ordinary body text. The `f65v` case is the single strongest piece of evidence against the old guess: an intact, undamaged, non-foldout herbal page that still lacks a Currier label — meaning the omission tracks something about layout/hand convention, not physical condition. Appropriately hedged throughout: explicitly does not claim to resolve whether the unlabeled hand-4 text is linguistically closer to A or B, and flags that the pooled constraint numbers for unlabeled text are layout-sensitive, not a language assignment.

## Not done yet

- Whether Currier's original A/B distinction intentionally excluded diagram-style text, or simply never got around to labeling it, remains unknown and probably unknowable from internal evidence alone.
- No attempt yet to separate hand-4's linguistic profile from its layout — correctly flagged in the report as the next real test, not something this pass should have attempted.
