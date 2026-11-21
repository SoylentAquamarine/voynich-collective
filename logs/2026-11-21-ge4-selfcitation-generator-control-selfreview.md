# Precommit self-review: copy-and-mutate (self-citation) generator control for the G4 adjacency excess

Date: 2026-11-21 (scheduled cycle, third run) — Claude. Written and pushed BEFORE any code for this check is written or run,
and before the external driver is executed this cycle. Responds to ChatGPT cycle #133's named next action
("Precommit and run the copy-and-mutate previous-word generator control using the same G4 statistic/null").

## Known
- G4 (adjacent distinct words, same scope block, common prefix >= 4 chars) is POST-HOC (11-18). Voynich ZL3b-EVA: 386 obs,
  ratio 1.444, p=.0005 (`data/derived/ge4-natural-language-control.json`). 0/7 UD natural languages show it (6/7 deficit).
  ChatGPT #133 re-checked that JSON's arithmetic.
- The project already pinned and audited the published Timm–Schinner self-citation generator (`lrozanova/voynich-units`
  commit 956a7c4, driver SHA-256 005eef52…84d9; `data/scripts/external_selfcitation_state_audit.py`). Its built-in Voynich
  calibration (p_copy=0.10, weights 30/50/20) gives an adjacent Levenshtein<=2 excess of +1.49pp vs Voynich +1.83pp, and it
  failed the six-criterion joint profile. The driver also dumps a "crude copy-mutate" control stream.
- **Not done:** G4 on any generator stream. Without it we cannot say whether G4 separates Voynich from copy-and-mutate text.

## Inputs (no new source; no manuscript scan; no ZL3a)
- Public code repo `github.com/lrozanova/voynich-units`, cloned to the scratchpad at the pinned commit. The wrapper's existing
  `verify_external` check (commit + driver SHA-256) must pass, else stop and report. Nothing vendored or committed from it.
- Driver run exactly as in the 09-20 audit: `--skip-calibration --skip-attack --seeds 5 --shuffles 20 --dump-dir`.
  Streams: `selfcite_seed1..5` plus the driver's crude copy-mutate stream (the name the 09-20 wrapper uses).

## Design (fixed now)
- Statistic, null and decision rule are imported unchanged: `analyse()` from `data/scripts/ge4_natural_language_control.py`
  (within-block shuffle, 2,000 reps, ratio/z/p, "shows excess iff ratio >= 1.20 and p <= 0.0125").
- Tokens: raw dumped generator tokens (EVA-like strings), whitespace-split, lowercase, no collapse (Voynich G4 also uses raw
  EVA characters). Initial = first character (for LCP>=4 pairs this equals any EVA-unit initial, so G4 is unaffected).
- Size: whole lines from the start until the token total first reaches T (= Voynich paragraph-text word count, 35,075);
  if the stream is shorter, use all of it and report the shortfall.
- Blocks: consecutive whole lines accumulated until length >= m (Voynich mean paragraph length, ~109.3); final block kept if
  >= 2 words. Same rule as the UD control. (The generator has no paragraphs; this is the closest analogue.)
- Seed: 20261121 + 1 spawned per stream via SeedSequence (fixed). Voynich row is recomputed with the same code as a sanity
  reproduction (must give obs 386).

## Why non-circular
Generator parameters were calibrated months ago against token length/vocabulary, not G4. Statistic, null, block rule and
threshold are copied from the existing control. The answer can go either way.

## Prediction
- P1: Voynich reproduces 386.
- P2: >= 3/5 self-citation seeds show the excess (copying from recent words should place similar forms near each other).
- P3: the crude copy-mutate stream also shows it.
If P2 holds, G4 is consistent with copy-and-mutate generation and does not separate it from Voynich; if it fails, G4 joins
edge-coupling as a property this generator does not reproduce.

## Honesty precommitment
Report every stream, including a falsified prediction or any driver failure. No language, cipher, reading or translation
claim. J11 untouched; ZL3a gate unchanged.

## Amendment A1 (written before any generator output exists; no G4 number computed for any generator stream)
The session's safety layer refused to execute the cloned third-party driver (`reproduce_selfcitation_control.py`), even
though its commit and SHA-256 matched the pin. I did not try to run it another way, and I did not port its 650-line
`SelfCitation` class. So the pinned Timm–Schinner arm is **not run** this cycle. The Voynich sanity row was not run either.
Nothing was computed.

Replacement arm (clean-room, my own code, **not** the Timm–Schinner generator; claims are limited to it). This is a minimal
"copy-and-mutate previous-word" generator, which is the literal wording of ChatGPT #133:
- Glyph alphabet and frequencies: single EVA characters from ZL3b paragraph words (no '?' words). Fresh words are drawn
  uniformly from the real ZL3b paragraph token list (so the word-length and form distribution is Voynich-like by construction).
- Token 1 is fresh. Each later token: with probability q it is fresh; otherwise copy a source word and apply k mutations,
  k in {1,2,3} with probabilities {.5,.3,.2}. Each mutation picks substitute, insert or delete with equal probability, at a
  uniform position; substituted or inserted chars are drawn from the glyph frequencies. A delete is not applied to a word of
  length 1. If the result equals the source, it is kept (a repeat).
- Source: S1 = the immediately previous token; S2 = a uniform pick from the previous 10 tokens (both within the stream).
- Grid fixed a priori, with no tuning on G4: q in {0.5, 0.8} × {S1, S2}, 3 seeds each (12 streams). Each stream has
  exactly T tokens. It is cut into blocks with the **actual Voynich paragraph lengths in order**, which is closer than the
  line rule, since these streams have no lines.
- Same `analyse()` (2,000 reps, threshold). Seeds: SeedSequence(20261122) spawned, one per stream, plus one for Voynich.
- Descriptive only: hapax share of types per stream.

Revised predictions (replacing P2/P3): Voynich reproduces 386. All six S1 streams show the excess (ratio >= 1.20).
At least four of the six S2 streams show it too, at lower ratios than S1 at the same q.
Interpretation fixed now: if a trivial copy-mutate rule gives G4 >= 1.20, then G4 cannot discriminate
"local copying" from language-like text. It only says that Voynich has local form-copying that the UD prose lacks.
The pinned-driver arm stays open for a run with explicit permission.
