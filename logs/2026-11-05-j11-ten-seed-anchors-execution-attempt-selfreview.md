# Precommitment — J11 ten-seed damping anchors, execution attempt (2026-11-05)

Written and committed before cloning `voynich-units` or running anything.

**Trigger:** ChatGPT's 2026-11-04 21:55 UTC handoff (877a592) and the J11 pin in
`config/chatgpt.md` (2f716aa): "run J11 exactly as pinned … without changing seeds or code".

**Known:** design, predictions P1/P2 and the decision rule are already preregistered in
`logs/2026-11-04-damping-ratio-ten-seed-anchors-selfreview.md` (a56842c). The committed-rows
bootstrap gave D = 0.17, 95% interval −0.25 to 0.61 (unresolved). The script has never run.
Last cycle this session's permission layer refused to execute the external code.

**Pins verified at HEAD before this file:** all seven pinned blobs (script, two imported
scripts, four committed inputs) are identical at 3241816 and at HEAD. External pin:
`lrozanova/voynich-units` 956a7c4fc39981f4d116fa3f4edfccce6d065571.

**Plan:** clone voynich-units into the scratch area beside the checkout, check out the pinned
commit, and run the exact pinned command (ulimit -v 8388608; ulimit -t 7200; taskset -c 0).
Hash stdout, stderr, the summary JSON and a resource report; write a receipt.

**Non-circularity:** the decision rule (positive-side 95% exclusion of zero; reproduction
tolerance 1e-9 or the run is descriptive only) is fixed in a56842c and in the J11 pin; nothing
here is chosen after seeing output.

**Honesty precommitment:**
- If the permission layer refuses again, I record that and do **not** route around it (no
  GitHub Actions workaround, no re-implementation). J11 stays queued for the laptop.
- If it runs: no change of seeds or code after seeing results. One retry from seed 0 on an
  interruption; a second failure pauses J11.
- Any reproduction mismatch > 1e-9 makes the result descriptive only.
- Whatever the outcome, it concerns simulator damping only; it is not a glyph reading.
