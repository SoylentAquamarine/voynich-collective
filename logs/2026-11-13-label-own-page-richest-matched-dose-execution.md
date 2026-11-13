# Execution: matched-dose (~11.8 hits) cell for anchors on the label-richest pages

Precommit: `logs/2026-11-13-label-own-page-richest-matched-dose-selfreview.md` (571e50b, pushed before code). Responds to steering #62 (b36fc17). This is a **post-hoc, non-confirmatory diagnostic**.

Script: `data/scripts/label_own_page_richest_matched_dose_power.py`. It is a copy of the richest-pages script; only the planting rate and the seed changed. Run with python 3.13 in about 6 s. Output: `data/derived/label-own-page-richest-matched-dose-power.json`, sha256 c515e565…dca1d. A second run reproduced it byte-for-byte.

Setup: 200 reps, 2,000 perms, seed 20261116, frozen joint rule. The pages are the same top-k richest as in the richest-pages run (fRos, f67r2, f72r3, f69r, f72v3, …).

| f | pages | eligible tokens (ZL3b / RF1b-er) | per-token rate | realized hits mean±sd (ZL3b / RF1b-er) | power ± MC SE |
|---|---|---|---|---|---|
| 0.25 | 13 | 478 / 495 | 0.0247 / 0.0238 | 11.90±3.37 / 11.77±3.30 | **0.775 ± 0.030** |
| 0.10 | 5 | 264 / 273 | 0.0447 / 0.0432 | 11.68±3.28 / 11.52±3.17 | **0.44 ± 0.035** |

**Prediction vs. result** (predicted 0.70–0.95 in both cells):
- **f=0.25: held.** Power was 0.775, comparable to random-subset planting (0.77–0.87) and uniform planting (0.90) at the same dose.
- **f=0.10: failed.** Power was 0.44, well below the band and about 9 MC SE below uniform.

At equal dose, putting the anchors on only the five richest pages (fRos and the big astronomical/cosmological foldouts) clearly *reduces* power. A plausible reason is that these pages have the most label and text tokens, so their exact-hit counts vary most under the block permutation, and the same 11–12 added hits stand out less. I did not test this explanation.

**Disclosed corrections to earlier entries** (the earlier text is unchanged):
- The richest-pages entry said "Concentrating on data-rich folios does not reduce power". That holds only at the high doses that run used. At a matched ~11.8 hits it holds for the top 13 pages but not for the top 5.
- The concentrated-power wording "would have detected ≳1–1.5% … on as few as ~5 pages" holds for *randomly chosen* small page sets. It does **not** hold for anchoring confined to the five label-richest foldouts. There, detection at power 0.8 needs a larger dose, between ~12 hits (power 0.44, here) and ~34 hits (power 1.00, earlier). I did not localise it further and will add no more cells.

**Fair public sensitivity sentence:** the test would have detected ≳1–1.5% added own-page anchoring spread across pages or concentrated on a few random pages. It is materially less sensitive to anchoring confined to the five largest label-rich foldouts.

**Limits:** this is conditional power on top of real data. The frozen observed-data verdict is unchanged and is not rescued: there is no own-page anchor. Structural only, with no referent, reading or translation.

Yale: collections.library.yale.edu still returns HTTP 000 from this sandbox, so no image bytes were acquired. J11 is still QUEUED and unrun.
