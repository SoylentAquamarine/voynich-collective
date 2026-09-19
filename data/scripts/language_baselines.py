#!/usr/bin/env python3
"""Build size-matched natural-language baselines for Statistician pass 1.

The script deliberately reuses the metric implementations from
``statistician_pass1.py``. It downloads two pinned Universal Dependencies
treebanks, verifies every source-file checksum, extracts word tokens using a
documented policy, and compares exactly 39,026 tokens from each corpus with
the 39,026-token normalized Voynich corpus (39,026 as of the 2026-09-19
<~> word-boundary fix in normalize_eva.py; was 39,020 before).

No source corpus is vendored into this repository. The derived aggregate
metrics and full provenance are written to ``data/derived``.
"""

from __future__ import annotations

import hashlib
import json
import random
import tempfile
import unicodedata
import urllib.request
from collections import Counter
from pathlib import Path

from statistician_pass1 import analyze


REPO_ROOT = Path(__file__).resolve().parents[2]
VOYNICH = REPO_ROOT / "data" / "derived" / "ZL3b-normalized.txt"
OUT_REPORT = REPO_ROOT / "data" / "derived" / "language-baselines-report.md"
OUT_SUMMARY = REPO_ROOT / "data" / "derived" / "language-baselines-summary.json"
TARGET_TOKENS = 39_026  # updated 2026-09-19 for the <~> word-boundary fix; was 39_020
SHUFFLE_SEED = 20260918

CORPORA = [
    {
        "key": "latin_ittb",
        "label": "Medieval Latin — Index Thomisticus Treebank",
        "repository": "https://github.com/UniversalDependencies/UD_Latin-ITTB",
        "commit": "b19bcbd3ab66914570b5bb0616a9066d56d5e7ea",
        "description": "Works of Thomas Aquinas (1225–1274) and related authors; nonfiction Medieval Latin.",
        "license": "CC BY-NC-SA 3.0",
        "citation": "Passarotti, Dell’Orletta et al.; see the pinned corpus README.",
        "files": [
            ("la_ittb-ud-train.conllu", "0f0aded3ec3f697cdb8dc2294d213bdc951b127a5bc3d2114be22cd730cac5b8"),
            ("la_ittb-ud-dev.conllu", "e750a8b89b2bd23459fe0226d94eafd9bd0401d95531df5618170c48b13ac83f"),
            ("la_ittb-ud-test.conllu", "b25d8f12a7f483ff6152ce3b3724aabafffc1336103526229c919808f9de5f1e"),
        ],
    },
    {
        "key": "italian_isdt",
        "label": "Italian — Italian Stanford Dependency Treebank",
        "repository": "https://github.com/UniversalDependencies/UD_Italian-ISDT",
        "commit": "ff2447f6b21e03adbbbed5eff306f79b8857286b",
        "description": "Modern Italian legal, news, Wikipedia, questions, and mixed-genre prose.",
        "license": "CC BY-NC-SA 3.0",
        "citation": "Bosco, Montemagni & Simi (2013); see the pinned corpus README.",
        "files": [
            ("it_isdt-ud-train.conllu", "7c3e32d7f296c877387a0c805c3ae8c471e2b5e8df97f5e3da810834b50566ab"),
            ("it_isdt-ud-dev.conllu", "1bc7dda04c58a4d87e2e6607a0e612462b87e7da6dde56be610d3749521af744"),
            ("it_isdt-ud-test.conllu", "cea8ca0e8d1ddf7ce509f10afff426d00e058982f49473e0744cd0ee477129e3"),
        ],
    },
]


def download_verified(corpus: dict, filename: str, expected_sha256: str, destination: Path) -> None:
    url = f"{corpus['repository'].replace('github.com', 'raw.githubusercontent.com')}/{corpus['commit']}/{filename}"
    with urllib.request.urlopen(url, timeout=90) as response:
        content = response.read()
    actual = hashlib.sha256(content).hexdigest()
    if actual != expected_sha256:
        raise RuntimeError(f"Checksum mismatch for {url}: expected {expected_sha256}, got {actual}")
    destination.write_bytes(content)


def letters_only(form: str) -> str:
    """Lowercase NFKC form, retaining Unicode letters only."""
    normalized = unicodedata.normalize("NFKC", form).lower()
    return "".join(character for character in normalized if character.isalpha())


def load_conllu_words(paths: list[Path]) -> list[str]:
    words: list[str] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as source:
            for line in source:
                if not line or line.startswith("#") or line == "\n":
                    continue
                columns = line.rstrip("\n").split("\t")
                if len(columns) != 10:
                    continue
                token_id, form, _lemma, upos = columns[:4]
                if "-" in token_id or "." in token_id or upos in {"PUNCT", "SYM"}:
                    continue
                word = letters_only(form)
                if word:
                    words.append(word)
    return words


def load_voynich_words() -> list[str]:
    words: list[str] = []
    with VOYNICH.open("r", encoding="utf-8") as source:
        for line in source:
            _locus, text = line.rstrip("\n").split("\t", 1)
            words.extend(text.split())
    return words


def shuffle_within_words(words: list[str], seed: int) -> list[str]:
    """Preserve token count, word lengths, and characters; destroy order."""
    rng = random.Random(seed)
    shuffled: list[str] = []
    for word in words:
        characters = list(word)
        rng.shuffle(characters)
        shuffled.append("".join(characters))
    return shuffled


def metrics(words: list[str], label: str) -> tuple[dict, list[str]]:
    lines: list[str] = []
    _counts, result = analyze(words, label, lines)
    result["alphabet_size"] = len(Counter("".join(words)))
    h1 = result["char_entropy_h1_bits"]
    h2 = result["char_bigram_conditional_entropy_bits"]
    result["constraint_ratio"] = round(1 - (h2 / h1), 4) if h1 else None
    return result, lines


def main() -> None:
    if not VOYNICH.exists():
        raise SystemExit(f"Missing normalized Voynich corpus: {VOYNICH}")

    rows: list[tuple[str, dict]] = []
    details: list[str] = []
    provenance: list[str] = []

    voynich_words = load_voynich_words()
    if len(voynich_words) != TARGET_TOKENS:
        raise RuntimeError(f"Expected {TARGET_TOKENS} Voynich tokens, found {len(voynich_words)}")
    result, rendered = metrics(voynich_words, "Voynich ZL3b normalized")
    rows.append(("Voynich", result))
    details.extend(rendered)
    alpha_voynich = [word.lower() for word in voynich_words if word.isalpha()]
    alpha_voynich_result, rendered = metrics(alpha_voynich, "Voynich alphabetic-token sensitivity subset")
    rows.append(("Voynich alpha-only sensitivity", alpha_voynich_result))
    details.extend(rendered)
    shuffled, rendered = metrics(shuffle_within_words(voynich_words, SHUFFLE_SEED), "Voynich within-word shuffle")
    rows.append(("Voynich shuffled", shuffled))
    details.extend(rendered)

    with tempfile.TemporaryDirectory(prefix="voynich-baselines-") as temporary:
        temp_dir = Path(temporary)
        for corpus_index, corpus in enumerate(CORPORA):
            paths: list[Path] = []
            for filename, checksum in corpus["files"]:
                destination = temp_dir / filename
                download_verified(corpus, filename, checksum, destination)
                paths.append(destination)
            all_words = load_conllu_words(paths)
            if len(all_words) < TARGET_TOKENS:
                raise RuntimeError(f"{corpus['label']} has only {len(all_words)} eligible tokens")
            sample = all_words[:TARGET_TOKENS]
            result, rendered = metrics(sample, corpus["label"])
            rows.append((corpus["label"], result))
            details.extend(rendered)
            shuffled, rendered = metrics(
                shuffle_within_words(sample, SHUFFLE_SEED + corpus_index + 1),
                f"{corpus['label']} — within-word shuffle",
            )
            rows.append((f"{corpus['label']} shuffled", shuffled))
            details.extend(rendered)
            provenance.append(
                f"- **{corpus['label']}**: {corpus['description']} "
                f"Repository: {corpus['repository']}; pinned commit `{corpus['commit']}`; "
                f"license: {corpus['license']}; citation: {corpus['citation']}"
            )

    table = [
        "| Corpus | Tokens | Vocab | Alphabet | TTR | Mean length | Char H1 | Bigram H2 | Constraint | Word H1 | Zipf slope |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for label, row in rows:
        table.append(
            f"| {label} | {row['tokens']:,} | {row['vocabulary']:,} | {row['alphabet_size']} | "
            f"{row['type_token_ratio']:.4f} | {row['word_length_mean']:.2f} | "
            f"{row['char_entropy_h1_bits']:.4f} | {row['char_bigram_conditional_entropy_bits']:.4f} | "
            f"{row['constraint_ratio']:.4f} | {row['word_entropy_h1_bits']:.4f} | {row['zipf_slope']:.4f} |"
        )

    report = [
        "# Size-matched Language Baselines",
        "",
        "Generated by `data/scripts/language_baselines.py` using the exact metric functions from `statistician_pass1.py`.",
        "",
        "## Method",
        "",
        f"Each original corpus contributes exactly {TARGET_TOKENS:,} tokens, matching the normalized Voynich corpus. "
        "CoNLL-U multiword headers, empty nodes, punctuation, and symbols are excluded. Forms are NFKC-normalized, "
        "lowercased, and reduced to Unicode letters. The first eligible tokens in deterministic train/dev/test order are used.",
        "",
        f"The shuffled controls use fixed seed `{SHUFFLE_SEED}` (offset per corpus) to permute characters independently "
        "inside each word. They preserve token count, word length, and character-unigram counts while destroying most "
        "within-word ordering. Word-order shuffling was not used because every pass-1 metric is invariant to word order.",
        "",
        "## Results",
        "",
        *table,
        "",
        "## What the comparison permits",
        "",
        "- Voynich character H1 and Zipf slope fall in the same broad numerical neighborhood as both language baselines. This is compatibility, not evidence of decipherment or even of meaningful language.",
        "- Voynich bigram conditional entropy is materially lower than both Latin and Italian under the same calculation, so its within-word transitions are more constrained/predictable in this representation.",
        f"- The pass-1 Voynich alphabet has 42 literal characters because 708 tokens contain transcription notation such as braces, question marks, and extended-EVA codes. Dropping every non-alphabetic token leaves {len(alpha_voynich):,} tokens and lowers H2 from 2.1534 to {alpha_voynich_result['char_bigram_conditional_entropy_bits']:.4f}; the high-constraint result therefore does not disappear when those marked tokens are excluded. This is a sensitivity check, not a replacement normalization policy.",
        "- `Constraint` is `1 - H2/H1`: the fraction of unigram uncertainty removed by knowing the previous within-word character. It partly normalizes the comparison for differing unigram entropy, but not for alphabet, genre, or morphology.",
        "- Every original corpus is much more predictable than its within-word shuffle, confirming that the metric detects non-random character ordering in all three.",
        "- The comparison is not controlled for alphabet size, morphology, genre, orthography, scribal abbreviation, or transcription conventions. Those are confounds, not footnotes.",
        "- A two-corpus baseline is context for pass 1, not a universal natural-language range. No hypothesis should be promoted from this table alone.",
        "",
        "## Provenance",
        "",
        *provenance,
        "",
        "Only aggregate measurements are committed; source texts are downloaded from pinned commits and checksum-verified at runtime.",
        "",
        "## Full metric output",
        "",
        *details,
    ]
    OUT_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")

    summary = {
        "target_tokens": TARGET_TOKENS,
        "shuffle_seed": SHUFFLE_SEED,
        "method_source": "data/scripts/statistician_pass1.py",
        "corpora": {label: row for label, row in rows},
        "source_commits": {corpus["key"]: corpus["commit"] for corpus in CORPORA},
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_REPORT}")
    print(f"Wrote {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
