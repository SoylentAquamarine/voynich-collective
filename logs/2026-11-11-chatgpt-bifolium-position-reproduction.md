# Independent reproduction: herbal bifolium position and conjugate-leaf concordance

**Date:** 2026-11-11  
**Auditor:** ChatGPT  
**Source commit:** `c4ed3ce2844a99ee48f44b446a04465ee2ea86e6` (PR #104 base)  
**Inputs:** ZL3b Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`; RF1b Git blob `c36d87683de5fcd24b4bb9ed56ddc4da475d8e99`.  
**Independent implementation:** `data/scripts/chatgpt_bifolium_position_reproduction.js`; no Python imports or external packages. It verifies both Git blob IDs before parsing.

## Reproduced counts

- 227 page headers; 5,385 loci in each transcription.
- 247 herbal paragraph-start loci; 88 eligible herbal pages with at least two non-empty paragraph starts.
- Q1 uses 80 pages in eight quires with both outer and inner positions (44 outer, 36 inner). Quires O and Q are excluded because they contain only one position class.
- Q2 finds 52 `($Q,$B)` groups and 50 conjugate pairs; `fRos` is dropped because it lacks `$F`.

## Q1 — outer versus inner bifolium position

Position is reconstructed from `$B`: outer when `$B <= maxB/2` within quire. The statistic is (D_{outer}-D_{inner}), where D is the first paragraph-initial word's whole-corpus hapax rate minus the later paragraph-initial words' hapax rate. The primary label shuffle preserves outer/inner counts within quire. A second shuffle preserves counts within quire × Currier-language strata.

| Reading | Outer D | Inner D | Outer−inner D | Within-quire p | Within-quire × language p |
|---|---:|---:|---:|---:|---:|
| ZL3b | +0.3772 | +0.2807 | +0.0985 | 0.48907 | 0.60675 |
| RF1b | +0.3427 | +0.2893 | +0.0749 | 0.62841 | 0.80360 |

Both outer and inner strata retain a positive first-word effect. The contrast does not meet the preregistered p<0.05 criterion for position dependence. This is **no evidence of position dependence**, not evidence of position independence. The language-stratified sensitivity has 60 pages across seven strata and is also non-significant.

## Q2 — conjugate-leaf language concordance

| Scope | Pairs used | Concordant | Null mean | Independent Monte Carlo p | Mixed-quire pairs concordant |
|---|---:|---:|---:|---:|---:|
| All quires | 44 | 44 | 34.66856 | 0.00004 (3/100,000 exceedances) | 18/18 |
| Herbal quires A–G | 27 | 27 | 19.00136 | 0.00020 (19/100,000 exceedances) | 16/16 |

Davis hand concordance is 48/48 pairs overall and 27/27 in herbal quires A–G. These reproduce the committed file-level result using a separate JavaScript implementation and independent Monte Carlo stream.

## Limits and decision

This reproduces the arithmetic and parsing from the exact pinned transcriptions; it is not an independent transcription or a new physical collation. The `$B` bifolium structure is a reconstruction of a rebound manuscript. Q1 cannot fully separate position from language; Q1s is a partial check. Q2 is a known observation, and may be partly definitional if transcribers assigned `$L` or `$H` at bifolium level. RF1b shares ZL3b's paragraph-start loci. Monte Carlo p-values differ slightly from Claude's Python stream by design; observed D values and counts match.

**Research decision:** accept the independent reproduction of Q1/Q2 as a code-level audit; do not open another same-corpus subdivision. The herbal line remains structural only. The next useful path toward meaning is external evidence: an attended/allow-listed Yale IIIF route for the already-authorized ten-folio image analysis, with hashes recorded and no image bytes committed. J11 remains a separate simulator-only laptop job, QUEUED and unrun; it cannot satisfy the source-language objective.
