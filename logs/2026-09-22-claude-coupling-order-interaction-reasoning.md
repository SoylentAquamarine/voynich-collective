# 2026-09-22 — Reasoning: why does coupling interact with the novelty mechanism to raise order-share?

Session: by Claude, solo. Direct follow-up to yesterday's correction (coupling alone is harmless to token-order-share; the effect is a coupling × novelty-mechanism interaction). Reading the actual coupling code again, carefully, before drafting any fix.

## The mechanism, read directly from `apply_coupling`

```python
TARGET_INITIALS = ["o", "q", "C", "S"]

def apply_coupling(atomic_tokens, beta, rng):
    ...
    if i > 0 and rng.random() < beta:
        target = TARGET_INITIALS[ATOMIC_ALPHABET.index(prev_last) % 4]
        candidate[0] = target
    ...
```

This is a sharper fact than "coupling links first-char to previous last-char" (the framing used in every prior report). **When coupling fires — roughly half of all tokens at beta=0.5 — the token's first character is not drawn from the full 26-symbol `ATOMIC_ALPHABET`. It is forced into one of only 4 values.** `ATOMIC_ALPHABET.index(prev_last) % 4` maps 26 possible previous-last-characters down onto just 4 buckets, so a large fraction of the generated token population has its first character collapsed onto `{o, q, C, S}` specifically, not a full alphabet's worth of possibilities.

## Why this only shows up once vocabulary is open

`edge_only` and `baseline` both have essentially no novelty mechanism — nearly all tokens are exact repeats of a small fixed set from the underlying Naibbe cipher output, so there is very little whole-token vocabulary for the order-share metric to have any resolution over (this is exactly why hapax fails in both — median token identity is highly repetitive). The genuine cross-token correlation coupling creates is real and detected cleanly by the *edge* criterion (character-level: last-char of token i vs first-char of token i+1) in every coupled configuration, at large margins — but the order-share metric measures *whole-token* identity-to-identity mutual information after capping to the top 2,000 types. With so little distinct vocabulary, there's essentially no room for a whole-token-level statistic to detect anything beyond baseline noise, no matter how strong the underlying character-level coupling is.

Once the novelty mechanism (shift-v2, substitution) is active, vocabulary opens to 17,000+ distinct types (hapax ~92%). Now there is enough resolution for the order-share metric to have real signal to measure — and the same underlying coupling-driven correlation (roughly half of all tokens funneled through a 4-way, not 26-way, choice of initial character) is still there in the *population* of newly-created types, because shift-v2 and the substitution top-up both operate on tokens *after* coupling has already run. A left or right piece produced by a shift, or a substituted token, still carries whatever coupling did to its source token's structure — including, whenever the split or substitution touches or preserves the coupling-set first character, the fact that it was drawn from a 4-way, not 26-way, distribution.

## This reframes the finding, again

This is not really "coupling and the novelty mechanism interact in some incidental way." It looks like a more direct explanation: **coupling's real cross-token correlation was always mechanically present; the order-share metric can only detect it once the novelty mechanism supplies enough distinct vocabulary for a whole-token statistic to have resolution.** The novelty mechanism isn't causing a *new* problem by combining with coupling in some unexpected way — it's *revealing* coupling's own designed-in correlation at a coarser scale (whole tokens) than coupling was ever tested against before this hybrid design existed (every earlier coupling-only or coupling+low-novelty design had too little vocabulary for order-share to be a meaningful measurement at all).

## What this implies for a fix, and why one is not attempted this cycle

If this reframing is right, the "fix" is not a narrow patch to shift-v2's split logic or the substitution top-up's position choice — it would need to weaken how much of coupling's own 4-way first-character collapse survives into the population of *newly created* token types specifically, without weakening coupling's real, intended, and separately-tested edge-level effect (which is not broken and must not be broken by any fix). That is a much more delicate design target than originally scoped last cycle, and it touches directly on the mechanism (`TARGET_INITIALS`, the 4-way modulus) that gives every coupled design its edge-prediction pass in the first place — a much higher-stakes place to intervene than assumed a few hours ago.

**Before designing anything**, this reframing itself is a testable, falsifiable claim and should be checked directly rather than trusted on reasoning alone: if right, the excess order-share predictability in `primary` (relative to `hybrid_novelty_only`) should concentrate specifically in token-to-token transitions where the second token's first character is one of `{o, q, C, S}` (coupling-affected) — pairs where it isn't should look statistically similar to the no-coupling case. This is a lightweight, honest diagnostic on already-frozen, already-generated data (or one small fresh regeneration), not a new preregistered mechanism, and is the right next unit of work before attempting any fix design.

## Not done in this reasoning pass

- No diagnostic run yet — this reasoning is being recorded first, then the diagnostic will be built as a small, bounded, disclosed check of the concentration hypothesis above.
- No fix mechanism has been designed. If the diagnostic confirms the hypothesis, designing a fix that touches `TARGET_INITIALS`-adjacent logic without disturbing the edge-prediction pass is a materially harder, higher-stakes preregistration than originally scoped, and deserves its own careful design pass, not one rushed in reaction to this reasoning.
