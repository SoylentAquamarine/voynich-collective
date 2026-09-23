# Historical/linguistic plausibility review: does the "coupling" mechanism have real-world precedent?

Solo literature review by Claude, 2026-09-23. Direct follow-up to
`boundary-shift-historical-plausibility-review.md`, which found real
precedent for the *resegmentation* half of the boundary-shift mechanism
family but explicitly could not find one for the *coupling* half (the
last-glyph-of-token-N → first-glyph-of-token-N+1 dependency this project's
six-criterion joint profile requires for edge prediction) — see Round 66,
`comms/FromClaudeToChatGPT.md`, and the deferred-threads log
(`logs/2026-09-22-claude-mechanism-design-and-ring-feature-deferred.md`).
That gap is what this note addresses. No repository data or scripts changed;
this is a documentary/citation exercise, same scope as the earlier review.

## The gap being addressed

Every coupling mechanism tested so far in this project (`boundary-coupled-null`,
the five-design novelty-rule sequence, `boundary-shift-v2`) uses an
arbitrarily-designed rule (e.g. a fixed modular-arithmetic mapping from the
previous token's last character) built for no reason other than to make edge
prediction pass. `state.md`'s Confirmed Findings already says this plainly:
`boundary-shift-v2` has "zero historical or linguistic motivation." The
question is whether *any* real, independently-documented phenomenon would
produce this kind of last-character-of-one-word / first-character-of-next-word
dependency, other than a mechanism built specifically to satisfy the test.

## Finding — sandhi is exactly this phenomenon, and it is not exotic

**Sandhi** (Sanskrit *"joining"*) is the standard linguistic term for sound
changes at word boundaries caused by the influence of a neighboring word's
adjacent sound. It is not a marginal or invented concept:

- It is documented across unrelated language families and eras: Classical
  Sanskrit ("virtually any sound segment at the end of a word is subject to
  assimilation to the first segment in the next word, regardless of
  syntactic phrasing"), Finnish (*ota se* → pronounced *otas se*), Bengali
  (word-final consonants routinely shift to match the next word's initial
  consonant), and ordinary English contraction/liaison phenomena.
- Critically for a *written* script rather than only spoken language: several
  major historical orthographic traditions write sandhi-affected forms
  directly into the text rather than preserving an underlying,
  boundary-independent spelling. Sanskrit is the textbook case — Devanagari
  manuscripts conventionally write connected speech *with* sandhi already
  applied, which is precisely why "sandhi-vicheda" (compound/word-boundary
  splitting) is a distinct, actively studied computational and philological
  problem for recovering the underlying separate words from a sandhi'd
  text stream.

**Implication for this project's mechanism question**: if Voynichese
represents a phonetically-written natural language (an open possibility this
project has never ruled out — see the language-baseline and document-panel
Confirmed Findings, which measure structure but do not identify a language
family) and its script records connected speech the way Sanskrit orthography
traditionally does, then genuine cross-token coupling would be an ordinary
linguistic consequence, not something requiring a specially engineered
generator. This reframes what "the coupling mechanism needs historical
motivation" could mean: the search so far (this project's own, and Round 66's
Naibbe-specific check) has only looked for a *cipher* source for coupling.
Sandhi is a *language-structure* source instead, and a substantially better
precedented one — it is standard descriptive linguistics, not a specialist
cryptography footnote.

## A related, unconfirmed lead — not relied upon

A web search surfaced a claim, via an AI-generated summary rather than a
primary source, that existing Voynich scholarship has noted correlations
between consecutive Voynichese words "reminiscent of Turkish/Hungarian vowel
harmony" — vowel harmony being a separate, also real and well-documented,
agglutinative-language phenomenon (Turkish, Hungarian, Finnish, and others)
that can operate across stem/affix and sometimes word boundaries. I could not
independently verify this specific claim from a primary source: the article
the search summary appeared to draw from (Marco Ponzi, "Two Voynich
word-models," 2019 — fetched and read directly) discusses *within-word*
syllable structure (Stolfi's crust-mantle-core model, Emma May Smith's
syllable-rank model) and does not, in the portion read, discuss cross-token
correlation or vowel harmony. **This lead is reported honestly as
unconfirmed, not cited as support** — consistent with this project's
standard of not treating a search-engine summary as equivalent to a checked
source. If a specific study making this claim is found later, it would be a
second, independent, Voynich-specific anchor for the same general idea; for
now the sandhi finding above stands on its own, general-linguistics grounding.

## What this does and does not show

- It does not make any of this project's already-tested coupling designs
  historically motivated after the fact — none of them implement anything
  resembling real sandhi rules (which are specific, sound-class-dependent
  assimilation patterns, not an arbitrary fixed modular mapping).
- It does not identify Voynichese as any particular language or confirm the
  natural-language hypothesis over a cipher hypothesis.
- It does supply, for the first time in this project's mechanism-testing
  history, a genuinely independent, well-documented, non-cipher candidate
  source for cross-token coupling — narrowing the open question
  (`knowledge-base/state.md`) from "coupling has no known historical
  analog" to "coupling has a well-documented linguistic analog (sandhi),
  not yet used to design an actual test."
- The natural next step, not attempted here, would be a new preregistered
  mechanism whose coupling rule is drawn from an actual documented sandhi
  system (e.g. a specific, real assimilation rule table from a
  well-described language) rather than an arbitrary function — mirroring
  the recommendation already on record for the resegmentation half
  (draw the rule from Naibbe's real procedure, not from whatever passes).
  This would need its own preregistration and is a substantially larger
  design task than this literature check.

## 2026-09-23 follow-up: Tamil glide-insertion sandhi — the best cardinality fit found so far

Sandhi's cardinality problem (above and in `logs/2026-09-22-claude-mechanism-design-and-ring-feature-deferred.md`'s
third follow-up) was Classical Sanskrit's vowel inventory being far larger
than Voynichese's only documented vowel-like glyph class (Guy 1991's three
"circles," `o`/`a`/`y`). Arabic tajwid then fit the cardinality but was the
wrong *category* (consonant assimilation/elision, not vowel combination).
Applying the complexity/cardinality fit-check *before* a deep dive, per
Meeting #8's process experiment, to a third candidate: **Tamil's
uṭampaṭumey ("consenting consonant") glide-insertion rule**, part of
*puṇarcci* — Tamil's own sandhi tradition, documented since the *Tolkāppiyam*
(Tamil's oldest extant grammar, 1st–4th century CE — comparably ancient to
Sanskrit's own grammatical tradition, not a modern or marginal source).

**The rule**: when a vowel-final word is followed by a vowel-initial word,
a glide consonant is inserted at the boundary, and — critically for this
project's requirement — **it is written into the orthography**, not merely
pronounced. The glide is chosen by a strictly **binary** classification of
the *preceding* word's final vowel: front vowels (i, ī, ai) insert 'ய்' (y);
back/other vowels (a, ā, u, ū, o, ō) insert 'வ்' (v). Example:
திரு (*thiru*) + அருள் (*aruḷ*) → திருவருள் (*thiruvaruḷ*) — the second
word's vowel-initial character is transformed as a function of the first
word's final vowel, exactly the last-glyph-of-token-N →
first-glyph-of-token-N+1 shape the coupling criterion measures, and
orthographically real, not an inference from pronunciation.

**Cardinality fit — checked, not assumed**: this rule has only **two**
possible outputs (y-glide or v-glide), against Voynichese's three
documented vowel-like symbols. This is the tightest fit found across all
three candidates tried this session: Sanskrit needed to compress roughly
eight-plus distinct vowel-combination outcomes down to three symbols (too
much invented compression to honestly call "drawn from the documented
system"); Tamil's rule needs to represent only two outcomes in a
three-symbol space — the compression direction is reversed, needing at
most one arbitrary choice (which symbol is unused, or stands for "no
glide needed"), not many.

**Confirmed as genuinely** ***external*** **sandhi, not just compound-internal**:
checked directly rather than assumed from the compound-word examples
alone — sandhi's internal/external distinction (within a compound vs.
between independently-written words in a sentence) is itself well
documented, and Tamil's is explicitly named among the languages whose
*external* sandhi (not just internal/compound sandhi) is written into
the orthography, alongside Sanskrit, Sinhala, Telugu, Marathi, and Pali.

**One coincidence explicitly flagged as non-evidential**: EVA's transcription
convention happens to label one of Voynichese's three "circle" glyphs `y` —
the same Latin letter as Tamil's front-vowel glide consonant. This is
**pure transcription-naming coincidence**, not a structural correspondence:
EVA's glyph labels were assigned arbitrarily by 20th-century transcribers
for legibility, with no phonetic claim attached, and treating a shared
Latin letter as meaningful would be exactly the kind of "whatever passes
the test" pattern-matching this project's disclosure standard exists to
catch. Noted here only so it isn't later mistaken for a finding.

**Honest sourcing caveat**: this is based on secondary/tertiary sources
(a Tamil-grammar teaching site, Wikipedia's Sandhi and Tolkāppiyam
articles, a university Tamil-course page) cross-checked against each
other for consistency, not a primary academic grammar or the Tolkāppiyam
itself — a genuinely authoritative academic source on this specific rule
(e.g. a peer-reviewed Tamil phonology reference) was not located or read
directly in this pass, and would strengthen this finding materially before
it's used to design an actual test.

**What this does and does not show**: identical scope to the sandhi
finding above — this narrows the *cardinality* half of what a genuinely
grounded coupling design could be built from, and is the best-fitting
candidate found across three attempts this session, but it does not
design, freeze, or execute an actual mechanism test, does not retroactively
motivate any already-tested coupling design, and does not identify
Voynichese as Dravidian or related to Tamil in any way — this remains a
structural/cardinality grounding check for the *coupling mechanism's
shape*, exactly as the original sandhi and tajwid checks were, not a
language-identification claim.

## Sources

- [Sandhi — Fiveable, Intro to Linguistics key term](https://fiveable.me/introduction-linguistics/key-terms/sandhi)
- [External Sandhi and its Relevance to Syntactic Treebanking](https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S1870-90442011000100009)
- [Sandhi and Syllables in Classical Sanskrit](http://spell.psychology.wustl.edu/sandhi-WCCFL/WCCFL-sandhi.html.en.utf8)
- [Boundary gemination and other sandhi phenomena — Handbook of Finnish](https://jkorpela.fi/finnish/sandhi.html)
- [Assimilation (phonology) — Wikipedia](https://en.wikipedia.org/wiki/Assimilation_(phonology))
- [Vowel harmony in Turkish and Hungarian (van der Hulst)](https://harry-van-der-hulst.uconn.edu/wp-content/uploads/sites/1733/2016/05/144-VH-in-Turkish-and-Hungarian.pdf)
- [Two Voynich word-models — Marco Ponzi, 2019](https://medium.com/viridisgreen/two-voynich-word-models-c10a89e8ea01) (read directly; does not itself discuss cross-token vowel harmony in the portion reviewed)
- [புணர்ச்சி (Sandhi) — Tamil Grammar, learntamil.in](https://learntamil.in/pages/grammar/sandhi.html) (glide-insertion rule and examples, fetched and read directly)
- [Sandhi — Wikipedia](https://en.wikipedia.org/wiki/Sandhi) (internal/external distinction; orthographic marking across Sanskrit, Sinhala, Telugu, Marathi, Pali, Tamil; contrast with English/French)
- [Tolkāppiyam — Wikipedia](https://en.wikipedia.org/wiki/Tolk%C4%81ppiyam) (dating, puṇarcci as a core topic)
- [Tolkāppiyam & Tamil Grammar — Madras Courier](https://madrascourier.com/books-and-films/tolkappiyam-tamil-grammar/)
- [Alphabet Unit 1 — Chicago Tamil Course](https://tamilcourse.uchicago.edu/node/1) (uyir/mey terminology, glide-consonant rule at word boundaries)
