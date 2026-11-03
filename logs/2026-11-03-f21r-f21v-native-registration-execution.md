# 2026-11-03 — f21r/f21v native-resolution registration: execution record

Precommitment: `logs/2026-11-03-f21r-f21v-native-registration-selfreview.md` (committed in
3a6e7e3 before any Yale data for this test was fetched). Script:
`data/scripts/f21_native_registration.py`. Runner: `.github/workflows/yale-f21-native-registration.yml`,
Actions run 41699045615 (success, 2026-11-03 18:59-19:01 UTC). Results (committed by the runner
in 4dbfb08, no image bytes): `research/2026-11-03-f21r-f21v-native-registration.csv`.

**Before the real run.** The script was checked only on synthetic pages in this sandbox (a
flipped-copy target gave r≈0.999 vs control ≤0.47; refusal guards for in-repo image dirs and
local-test output paths fire). No Yale data was reachable here; nothing was tuned on real images.

**Input checks.** All eleven 1,200-px JPEGs match the PR #91 manifest hashes; f21r native
sha256 0d28a9ed… matches the ten-folio receipt. "input problems: none".

**1. Reproduction (1,200 px), pass.** f21v flipped 0.8777 (ref 0.878, dx=0, dy=10, same
offset as the original note); unflipped 0.1900 (ref 0.190). An independent re-implementation
therefore reproduces ChatGPT's published numbers. Over the nine preregistered controls the
maximum is 0.3396 (f22v flipped), which matches the earlier "at most 0.340" for four controls.

**2. Native (s = 2.2075).** f21v flipped **0.9006** (dx=0, dy=21 ≈ 10 px at 1,200 scale);
unflipped 0.2144. Maximum control in either orientation **0.3952** (f22v flipped); next
f19v unflipped 0.3137. Gap 0.505. f20v (the present facing page) flipped 0.1921, unflipped
0.1272. **Decision rule: replicates at native.** All three predictions held (reproduction
passes; f21v ≥ 0.80; max control ≤ 0.45).

**Disclosed limits.**
- Same pages, region chosen after viewing: a robustness check across resolution and a wider
  control set, not independent discovery evidence.
- Inherited from the original method: every image is resized to f21r's frame, so pages with a
  different aspect ratio (f21v native 2849x3769 vs f21r 2649x3743) are slightly stretched. This
  could only lower the true match, not create one.
- Several control maxima sit on the edge of the offset grid (e.g. dx=176, dy=-199/219). A wider
  search might raise those control values somewhat; it was not run, because the grid was frozen.
- Interpretation: the match is to the other side of the same leaf (f21v, mirrored), not to the
  present facing page (f20v). This favours a through-the-leaf image (show-through or
  strike-through of f21v's green leaflets) over contact offset from the facing page. It does not
  establish physical mechanism, rebinding history, painter, or date. Under the ten-folio rubric
  the f21r marks stay "ambiguous/not-assessable" rather than counting as careless painting.
- This is not a reader-2 score and does not touch `research/2026-11-01-ten-folio-cell-template.csv`.
- Images were discarded with the runner; none were transferred to this session or committed.
