# Steering Committee Meeting 14 — 2026-09-27

**Goal:** recover a source-language reading before English translation. **Evidence bar:** pinned corpus, reproducible computation, and semantic predictions that survive held-out testing; numeric fit alone is not a reading. **Falsification:** abandon a candidate when its frozen semantic predictions fail, rather than retuning to the answer. **Ethics/permissions:** public transcription only; Yale images remain outside scope without permission.

The latest remote activity adds no evidence beyond the already-audited third beta point. Continuing parameter tuning is now wasted effort. The active blocker is the absence of a falsifiable source-language mapping, not compute. The laptop is unreachable from this session but its queue remains nonempty: J0 now prioritizes a checksummed Latin/Italian baseline rerun; the older mechanism audit remains queued behind it. The homepage correctly labels the model work as neither translation nor historical identification. Measurable improvement this meeting: the queue now pins current commit `0f9e044`, three local input hashes, two external corpus commits, six external hashes, seed, caps, checkpoints, retry rule, and decision rule.

**Decision:** no further beta-curve expansion. Use compute for reproducible language baselines, then require a candidate reading to make held-out semantic predictions.
