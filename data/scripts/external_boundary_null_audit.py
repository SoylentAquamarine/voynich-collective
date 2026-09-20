#!/usr/bin/env python3
"""Execute the preregistered boundary-coupled constructive null (BCCN).

Implements methods/boundary-coupled-null-preregistration.md exactly as frozen
after the solo self-review and implementation-pilot corrections (see
logs/2026-09-20-claude-solo-boundary-null-selfreview.md and the design
document's own inline "Self-review correction" / "Implementation-pilot
correction" notes). No component of the generator is fit to Voynich's own
transition, entropy, or vocabulary-growth statistics; the class partition,
coupling rule, and Latin-to-EVA character mapping are all fixed by
mechanical, alphabetical rules. Scoring reuses the project's existing
entropy/BPE/token-order pipeline (`reproduce_naibbe_control.battery`) and the
held-out edge-prediction test already used for Naibbe, Cardan, and
self-citation.

Usage:
    python data/scripts/external_boundary_null_audit.py \
        ../paper-audit/voynich-units --latin-dir ../paper-audit/latin-ittb
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
import random
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-boundary-null-audit-summary.json"

UNITS_EXPECTED_COMMIT = "956a7c4fc39981f4d116fa3f4edfccce6d065571"
LATIN_EXPECTED_HASHES = {
    "la_ittb-ud-train.conllu": "0f0aded3ec3f697cdb8dc2294d213bdc951b127a5bc3d2114be22cd730cac5b8",
    "la_ittb-ud-dev.conllu": "e750a8b89b2bd23459fe0226d94eafd9bd0401d95531df5618170c48b13ac83f",
    "la_ittb-ud-test.conllu": "b25d8f12a7f483ff6152ce3b3724aabafffc1336103526229c919808f9de5f1e",
}

K_CLASSES = 6
P_REUSE = 0.87  # frozen after implementation-pilot calibration (69.9-70.3% hapax across 3 seeds)
PRIMARY_P_COUPLE = [0.3, 0.5, 0.7, 0.9, 1.0]
NEGATIVE_CONTROL_P_COUPLE = 0.0
SEEDS = [42 + 137 * i for i in range(20)]
N_TOKENS_MIN = 39026

SIX_CRITERIA = {
    "H1_bits": {"center": 3.9763, "tol": 0.15},
    "H2_bits": {"center": 2.6897, "tol": 0.15},
    "learned_units": {"checkpoints": [32, 64], "k64_min": 0.90, "k64_max": 1.20},
    "token_order_share": {"min": 0.0, "max": 0.02},
    "edge": {"gain_min": 0.15, "positive_min": 15, "blocks": 16},
    "hapax": {"min": 0.65},
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_units(repo: Path) -> str:
    import subprocess

    commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if commit != UNITS_EXPECTED_COMMIT:
        raise RuntimeError(f"voynich-units repo at {commit}, expected {UNITS_EXPECTED_COMMIT}")
    return commit


def verify_latin(latin_dir: Path) -> dict:
    statuses = {}
    for name, expected in LATIN_EXPECTED_HASHES.items():
        actual = sha256(latin_dir / name)
        statuses[name] = {"expected": expected, "actual": actual, "matches": actual == expected}
        if actual != expected:
            raise RuntimeError(f"checksum mismatch for {name}: {actual}, expected {expected}")
    return statuses


# --------------------------------------------------------------- BCCN generator

def letters_only(form: str) -> str:
    normalized = unicodedata.normalize("NFKC", form).lower()
    return "".join(c for c in normalized if c.isalpha())


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


def glyph_classes(alphabet: list[str], k: int = K_CLASSES) -> tuple[dict, dict]:
    glyph_to_class, class_to_glyphs = {}, defaultdict(list)
    for i, g in enumerate(alphabet):
        c = i % k
        glyph_to_class[g] = c
        class_to_glyphs[c].append(g)
    return glyph_to_class, dict(class_to_glyphs)


def build_latin_to_eva_map(latin_words: list[str], eva_alphabet: list[str]) -> dict:
    latin_chars = sorted(set("".join(latin_words)))
    return {lc: eva_alphabet[i % len(eva_alphabet)] for i, lc in enumerate(latin_chars)}


def build_order2_model(latin_words: list[str], latin_to_eva: dict):
    order2, order1, unigram = defaultdict(Counter), defaultdict(Counter), Counter()
    for word in latin_words:
        mapped = [latin_to_eva[c] for c in word]
        for i in range(len(mapped)):
            unigram[mapped[i]] += 1
            if i >= 1:
                order1[mapped[i - 1]][mapped[i]] += 1
            if i >= 2:
                order2[(mapped[i - 2], mapped[i - 1])][mapped[i]] += 1
    return order2, order1, unigram


class BCCNModel:
    def __init__(self, eva_letters: list[str], latin_words: list[str], p_reuse: float):
        self.alphabet = sorted(set(eva_letters))
        self.glyph_to_class, self.class_to_glyphs = glyph_classes(self.alphabet)
        self.latin_to_eva = build_latin_to_eva_map(latin_words, self.alphabet)
        self.order2, self.order1, self.unigram = build_order2_model(latin_words, self.latin_to_eva)
        self.p_reuse = p_reuse
        self._memory: dict[int, list[str]] = defaultdict(list)

    def _sample_from_counter(self, counter: Counter, rng: random.Random) -> str:
        items = list(counter.items())
        total = sum(c for _, c in items)
        r = rng.uniform(0, total)
        upto = 0.0
        for glyph, c in items:
            upto += c
            if upto >= r:
                return glyph
        return items[-1][0]

    def _generate_fresh_internal(self, length: int, rng: random.Random) -> list[str]:
        glyphs: list[str] = []
        prev1, prev2 = None, None
        for _ in range(length):
            if prev2 is not None and (prev2, prev1) in self.order2:
                g = self._sample_from_counter(self.order2[(prev2, prev1)], rng)
            elif prev1 is not None and prev1 in self.order1:
                g = self._sample_from_counter(self.order1[prev1], rng)
            else:
                g = self._sample_from_counter(self.unigram, rng)
            glyphs.append(g)
            prev2, prev1 = prev1, g
        return glyphs

    def generate_token(self, prev_last_glyph, length: int, p_couple: float, rng: random.Random):
        if prev_last_glyph is None:
            first_class = rng.randrange(K_CLASSES)
        elif rng.random() < p_couple:
            first_class = (self.glyph_to_class[prev_last_glyph] + 1) % K_CLASSES
        else:
            first_class = rng.randrange(K_CLASSES)
        first_glyph = rng.choice(self.class_to_glyphs[first_class])

        internal_len = max(0, length - 1)
        reused = False
        if internal_len > 0 and self._memory[internal_len] and rng.random() < self.p_reuse:
            internal = list(rng.choice(self._memory[internal_len]))
            reused = True
        else:
            internal = self._generate_fresh_internal(internal_len, rng)
        if internal_len > 0 and not reused:
            self._memory[internal_len].append("".join(internal))

        glyphs = [first_glyph] + internal
        return "".join(glyphs), glyphs[-1]

    def generate_corpus(self, n_tokens_min: int, p_couple: float, seed: int, length_distribution: list[int]) -> list[str]:
        rng = random.Random(seed)
        self._memory = defaultdict(list)
        tokens: list[str] = []
        prev_last = None
        while len(tokens) < n_tokens_min:
            length = max(1, rng.choice(length_distribution))
            tok, last_glyph = self.generate_token(prev_last, length, p_couple, rng)
            tokens.append(tok)
            prev_last = last_glyph
        return tokens


# --------------------------------------------------------------- scoring (shared pipeline)

def edge_rows(lines):
    return [(i, left[-1], right[0]) for i, line in enumerate(lines) for left, right in zip(line, line[1:])]


def edge_crossfit(lines, alpha, blocks=16):
    rows = edge_rows(lines)
    total_gain, total_pairs, positive = 0.0, 0, 0
    for fold in range(blocks):
        lower = fold * len(lines) // blocks
        upper = (fold + 1) * len(lines) // blocks
        training = [r for r in rows if not lower <= r[0] < upper]
        testing = [r for r in rows if lower <= r[0] < upper]
        marginal = Counter(right for _, _, right in training)
        context = Counter((left, right) for _, left, right in training)
        left_count = Counter(left for _, left, _ in training)
        alphabet = set(marginal)
        categories = len(alphabet) + 1
        gain = 0.0
        for _, left, observed in testing:
            right = observed if observed in alphabet else "<unknown>"
            conditional = (context[(left, right)] + alpha) / (left_count[left] + alpha * categories)
            baseline = (marginal[right] + alpha) / (len(training) + alpha * categories)
            gain += math.log2(conditional / baseline)
        value = gain / len(testing)
        if value > 0:
            positive += 1
        total_gain += gain
        total_pairs += len(testing)
    return {"gain_bits_per_boundary": total_gain / total_pairs, "positive_blocks": positive, "blocks": blocks}


def evaluate_replicate(tokens, targets, naibbe_module, scale, args, modules):
    if len(tokens) < sum(targets["line_lengths"]):
        raise RuntimeError(f"{len(tokens)} tokens < {sum(targets['line_lengths'])} required by the line template")
    result = naibbe_module.battery("replicate", tokens, None, set(), targets, args, modules, lambda m: None, [])
    entropy = result["entropy"]["collapsed"]
    bpe = result["bpe"]
    order = result["order"]["order_by_cap"]["2000"]
    vocab = result["order"]["vocabulary"]
    template_lines = scale.wrap_to_lengths(tokens, targets["line_lengths"])
    edge = edge_crossfit(template_lines, alpha=1.0, blocks=16)

    c = SIX_CRITERIA
    passes = {
        "H1": abs(entropy["H1"] - c["H1_bits"]["center"]) <= c["H1_bits"]["tol"],
        "H2": abs(entropy["H2"] - c["H2_bits"]["center"]) <= c["H2_bits"]["tol"],
        "learned_units": (
            bpe["minimum_checkpoint"] in c["learned_units"]["checkpoints"]
            and c["learned_units"]["k64_min"] <= bpe["curve"]["64"]["gap"] <= c["learned_units"]["k64_max"]
        ),
        "token_order_share": c["token_order_share"]["min"] <= order["share"] <= c["token_order_share"]["max"],
        "edge": (
            edge["gain_bits_per_boundary"] >= c["edge"]["gain_min"]
            and edge["positive_blocks"] >= c["edge"]["positive_min"]
        ),
        "hapax": vocab["hapax_share_of_types"] >= c["hapax"]["min"],
    }
    return {
        "n_tokens_generated": len(tokens),
        "H1": entropy["H1"], "H2": entropy["H2"],
        "bpe_minimum_checkpoint": bpe["minimum_checkpoint"], "bpe_k64_gap": bpe["curve"]["64"]["gap"],
        "token_order_share": order["share"], "hapax_share_of_types": vocab["hapax_share_of_types"],
        "vocabulary_types": vocab["types"],
        "edge_gain_bits_per_boundary": edge["gain_bits_per_boundary"], "edge_positive_blocks": edge["positive_blocks"],
        "criteria_pass": passes,
        "all_six_pass": all(passes.values()),
    }


def run(units_repo: Path, latin_dir: Path, log) -> dict:
    units_commit = verify_units(units_repo)
    latin_files = verify_latin(latin_dir)
    log(f"verified units commit {units_commit}, Latin checksums OK")

    sys.path.insert(0, str(units_repo / "analysis"))
    naibbe_module = importlib.import_module("reproduce_naibbe_control")
    bundle = units_repo / "voynich_decipherment_repro_bundle"
    modules = naibbe_module.load_modules(bundle)
    _attack_lib, _attack_voynich, unit_probe, headlines, scale, _space, plant = modules

    voy_tokens = naibbe_module.voynich_entropy_tokens(bundle, headlines)
    observed, _, _, _ = scale.load_voynich_lines(bundle, plant.LOCUS_RE, plant.collapse, plant.strip_markup)
    line_lengths = [len(line) for line in observed]
    pooled = unit_probe.voynich_lines()
    targets = {
        "entropy_tokens": len(voy_tokens),
        "line_lengths": line_lengths,
        "bpe_glyphs": sum(len(w) for ln in pooled for w in ln),
    }
    length_distribution = [len(t) for t in voy_tokens]
    eva_letters = sorted(c for c in set("".join(voy_tokens)) if c.isalpha())
    log(f"targets: entropy_tokens={targets['entropy_tokens']} lines={len(line_lengths)} "
        f"template_tokens={sum(line_lengths)}; alphabet ({len(eva_letters)}): {eva_letters}")

    latin_paths = [latin_dir / name for name in LATIN_EXPECTED_HASHES]
    latin_words = load_conllu_words(latin_paths)
    log(f"Latin words: {len(latin_words)}")

    model = BCCNModel(eva_letters, latin_words, p_reuse=P_REUSE)
    args = SimpleNamespace(skip_attack=True, skip_crossing=True, shuffles=100, extra_k=[])

    replicates: dict[str, dict[str, dict]] = {}

    def run_config(name, p_couple, seeds):
        bucket = replicates.setdefault(name, {})
        for seed in seeds:
            t = time.time()
            tokens = model.generate_corpus(N_TOKENS_MIN, p_couple, seed, length_distribution)
            bucket[str(seed)] = evaluate_replicate(tokens, targets, naibbe_module, scale, args, modules)
            log(f"{name} seed={seed}: all_six_pass={bucket[str(seed)]['all_six_pass']} ({time.time()-t:.1f}s)")

    for p in PRIMARY_P_COUPLE:
        run_config(f"p_couple={p:.2f}", p, SEEDS)
    run_config(f"p_couple={NEGATIVE_CONTROL_P_COUPLE:.2f} [negative control]", NEGATIVE_CONTROL_P_COUPLE, SEEDS)

    # ablation: whichever primary p_couple has the highest mean edge gain, rerun with
    # the order-2 internal model replaced by pure uniform-random internal characters
    def mean_edge(name):
        rows = list(replicates[name].values())
        return sum(r["edge_gain_bits_per_boundary"] for r in rows) / len(rows)

    best_primary = max((f"p_couple={p:.2f}" for p in PRIMARY_P_COUPLE), key=mean_edge)
    log(f"ablation target (highest mean edge gain): {best_primary}")

    class UniformInternalModel(BCCNModel):
        def _generate_fresh_internal(self, length, rng):
            return [rng.choice(self.alphabet) for _ in range(length)]

    ablation_model = UniformInternalModel(eva_letters, latin_words, p_reuse=P_REUSE)
    best_p = float(best_primary.split("=")[1])
    bucket = replicates.setdefault(f"{best_primary} [ablation: uniform internal]", {})
    for seed in SEEDS[:5]:
        t = time.time()
        tokens = ablation_model.generate_corpus(N_TOKENS_MIN, best_p, seed, length_distribution)
        bucket[str(seed)] = evaluate_replicate(tokens, targets, naibbe_module, scale, args, modules)
        log(f"ablation seed={seed}: all_six_pass={bucket[str(seed)]['all_six_pass']} ({time.time()-t:.1f}s)")

    def aggregate(rows):
        metrics = ["H1", "H2", "bpe_minimum_checkpoint", "bpe_k64_gap", "token_order_share",
                   "hapax_share_of_types", "edge_gain_bits_per_boundary", "edge_positive_blocks"]
        out = {"n": len(rows), "joint_pass": sum(1 for r in rows if r["all_six_pass"])}
        for m in metrics:
            values = [r[m] for r in rows]
            out[m] = {"mean": sum(values) / len(values), "min": min(values), "max": max(values)}
        for c in ("H1", "H2", "learned_units", "token_order_share", "edge", "hapax"):
            out[f"criterion_{c}_passes"] = sum(1 for r in rows if r["criteria_pass"][c])
        return out

    primary_names = [f"p_couple={p:.2f}" for p in PRIMARY_P_COUPLE]
    primary_joint_passes = {name: aggregate(list(replicates[name].values()))["joint_pass"] for name in primary_names}
    verdict = "PASS" if any(v >= 16 for v in primary_joint_passes.values()) else "FAIL"

    return {
        "source": {"units_commit": units_commit, "latin_files": latin_files},
        "protocol": "methods/boundary-coupled-null-preregistration.md",
        "p_reuse": P_REUSE,
        "seeds": SEEDS,
        "six_criteria": SIX_CRITERIA,
        "replicates": replicates,
        "aggregate": {name: aggregate(list(bucket.values())) for name, bucket in replicates.items()},
        "primary_verdict": verdict,
        "primary_joint_passes": primary_joint_passes,
        "ablation_target": best_primary,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("units_repo", type=Path)
    parser.add_argument("--latin-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=OUT_JSON)
    args = parser.parse_args()

    started = time.time()

    def log(message: str) -> None:
        print(f"[{time.time()-started:7.1f}s] {message}", flush=True)

    summary = run(args.units_repo.resolve(), args.latin_dir.resolve(), log)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {args.output}; primary verdict: {summary['primary_verdict']}")


if __name__ == "__main__":
    main()
