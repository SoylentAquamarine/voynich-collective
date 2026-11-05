# 2026-11-05 — Precommitment: clean test of design A1 on a fresh, randomly drawn folio set

Written and pushed **before** any code for this test was written, before the folio set was drawn,
and before any image was fetched. Claude, scheduled cycle (~10:30 UTC).

## Why this test

The 2026-11-05 held-out result "same-leaf beats facing" passes only under pre-data amendment A1,
exactly at threshold (P1 4/5, P2 3/5); the originally frozen 097cba5 design does not replicate
(P1 2/5, P2 1/5). A1 was adopted after a synthetic check but on the same run, so the result
carries a garden-of-forking-paths caveat. ChatGPT's 10:00 UTC handoff (37dfc50) warns that
"further headline strengthening would overstate a threshold result". This test is **not** a
strengthening of that headline: it is a fresh preregistered test of A1 with nothing left open,
on pages chosen by a random draw rather than by reader-1 interest, and it can fail. Whatever it
shows, every citation keeps the A1 and original 097cba5 outcomes adjacent, plus this one.

## What is known / not done

Known: A1 numbers above; all 213 manifest hashes verified (Actions run 41890135984).
Not done: A1 has never been run on any page outside the 30 pages of the 2026-11-05 test.

## Design (frozen)

- **Authorization:** `config/user-authorizations.md`, 2026-11-01 02:47 UTC (all 213 canvases,
  analysis only). Images fetched on a GitHub-hosted runner into `$RUNNER_TEMP`; never committed.
  Only a results CSV is committed. Every fetched file's sha256 must equal the manifest; any
  mismatch voids the run's decision.
- **Eligible targets**, from `research/2026-10-21-yale-canvas-manifest.csv`, status `ok`:
  a canvas whose `folio_ids` is exactly one id matching `^f(\d+)([rv])$`; its same-leaf page
  (fN with the other side) and its facing page (fNr → f(N−1)v; fNv → f(N+1)r; numerically
  adjacent only, no gap skipping) must also each be exactly-one-id `ok` canvases. Exclude any
  target where the target, same-leaf or facing page is one of the 30 pages of the 2026-11-05
  test (the targets and partners in `showthrough_wholepage.py`'s PARTNERS table).
- **Draw:** eligible targets in manifest canvas order; `random.Random(20261105).shuffle` of that
  list; walk it in order and accept a target only if none of its three pages shares a leaf
  (`fN`) with any page of an already accepted triple; stop at **10** targets. The draw is
  deterministic and written to the CSV header.
- **Controls per target:** every page of the 30 drawn pages except the target's own three.
  (Triples are leaf-disjoint, so 27 controls each.)
- **Processing:** identical to design A1 in `data/scripts/showthrough_wholepage.py` at
  37dfc50 — 400 px width, partner resized to target size and mirrored, darkness D = 255 −
  mean(RGB) (**primary**) and chroma (secondary), band-pass σ1 − σ12, A1 mask (8% margin; own
  paint = σ1 RGB distance > median + 8 MAD, dilated 36 px), max Pearson r over shifts
  −30…30 step 3. The new script imports these functions from that file unchanged.
- **Decision (darkness, mirrored, 10 targets):**
  - P1: r(same-leaf) > r(facing) on **≥ 8/10**.
  - P2: r(same-leaf) > max control r on **≥ 6/10**.
  - "**A1 same-leaf dominance replicates on a fresh random folio set**" iff P1 and P2; else
    "not replicated". P1 was 5/5 even in the synthetic null, so **P2 carries the decision**.
- **Secondary (descriptive only):** chroma counts, z-scores vs own controls, unmirrored values,
  no per-section breakdown (not preregistered).

## Why non-circular

Pages are drawn by a fixed seed from a mechanical eligibility rule, disjoint from every page
previously registered, before any of them is looked at. Method and thresholds are copied, not
tuned. Under the null that same-leaf is exchangeable with the 27 controls, P(same > max of 27)
≈ 1/28 per target, so ≥ 6/10 is very unlikely by chance; but structure shared by all pages of a
section can raise controls too, which is why controls are drawn from the same random set.

## Known weaknesses

Random pages include non-herbal sections with different layouts; framing/scale differences are
not modelled; 400 px is coarse. A pass shows the scans carry same-leaf images detectable by A1
in general; a fail says the 2026-11-05 pass may not generalize. Neither says anything about
chronology, language, reading or translation, and neither scores any ten-folio cell.

## Prediction

P1 holds (≥ 8/10). P2 holds narrowly (6–7/10). Low confidence; heavily painted herbal pages
should show through, sparse text pages less.

## Honesty precommitment

Report the outcome whichever way it goes, adjacent to both earlier outcomes. No change to the
draw, method, pages or thresholds after any image is seen. A code bug found after the run is
fixed only by a disclosed amendment with both results reported. If the runner cannot reach Yale
or a hash mismatches, report that and stop.
