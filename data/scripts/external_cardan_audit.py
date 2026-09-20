#!/usr/bin/env python3
"""Execute the preregistered Cardan-grille protocol (methods/cardan-grille-preregistration.md).

Applies the documented one-line import repair to a temporary copy of the pinned
``grille.py`` (never modifies the checked-out external repo), builds the frozen
English-EWT row source from the already-pinned surface-token panel provenance,
generates every frozen-seed replicate for the four primary ``G_seq English``
configurations plus a reduced-N interpretive addendum (negative controls and the
honest independent-word sensitivity), and scores each replicate against the six
frozen project criteria using the project's own established code paths:
``voynich-units``' entropy/BPE/token-order pipeline (the same ``battery()``
function used for the Naibbe audit) and the held-out edge-prediction test from
``external_naibbe_audit.py``.

Usage:
    python data/scripts/external_cardan_audit.py \
        ../paper-audit/currier-signatures ../paper-audit/voynich-units --ewt-dir ../paper-audit/ewt
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
import random
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "data" / "derived" / "external-cardan-audit-summary.json"
OUT_REPORT = ROOT / "data" / "derived" / "external-cardan-audit-report.md"
OUT_CHART = ROOT / "docs" / "assets" / "external-cardan-edge-order.svg"

CARDAN_EXPECTED_COMMIT = "5d50101b57957bc7feaa002cec01d1ce5b2b11d9"
CARDAN_EXPECTED_HASHES = {
    "README.md": "fb1c32c1ea54d6960373a40934f1e6c02837aab021c7418da04dc35b8ce8418c",
    "RF1b-e.txt": "4f8f096eaafb2fa65096e8384ca98599138e9d0b4b57ebc3452a0f45e9544c63",
    "grille.py": "7ccb3b0efa65c34e552cc0d70ed0e08eb6c10cd6a0b304643dbc15bd34ab0686",
    "signatures_A.txt": "d7e754ad7445a0dec17d231b4bc144b7e8f5b8e44748d1be639fa078e8398ae4",
    "signatures_B.txt": "7a16818e6be33ecf20f53a76a06bb73b2b9dd8b3553c4562f0585c148fa0e02f",
    "signatures_v27.py": "af580d8de387281853b2d7d48ad23de7ca9b2b821a17ffddd825ca230c3a4f16",
    "verifier.py": "cc636403279b6415db440b802027d1973bf0e1fe212a7724dd06aadea9d9a471",
}
UNITS_EXPECTED_COMMIT = "956a7c4fc39981f4d116fa3f4edfccce6d065571"
EWT_EXPECTED_HASHES = {
    "en_ewt-ud-train.conllu": "d68e06122a702464c613076523d56740f047e5bbe89dd90ec32737e04d952143",
    "en_ewt-ud-dev.conllu": "39239e0a60db3ae68f4b7036189f11b6692741d10ff8240dd91f74f2760d90f8",
    "en_ewt-ud-test.conllu": "fa024f43dc5da3c5ac02563bc9bd0e974f46cbb1560823976a8f342a37dc494a",
}
EWT_EXPECTED_DOCUMENTS = 1174
EWT_EXPECTED_SURFACE_WORDS = 216654

PRIMARY_SEEDS = [42 + 137 * i for i in range(20)]
SENSITIVITY_SEEDS = PRIMARY_SEEDS[:5]

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


def verify_cardan(repo: Path) -> dict:
    commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if commit != CARDAN_EXPECTED_COMMIT:
        raise RuntimeError(f"cardan-grille repo at {commit}, expected {CARDAN_EXPECTED_COMMIT}")
    statuses = {}
    for relative, expected in CARDAN_EXPECTED_HASHES.items():
        actual = sha256(repo / relative)
        statuses[relative] = {"expected": expected, "actual": actual, "matches": actual == expected}
        if actual != expected:
            raise RuntimeError(f"checksum mismatch for {relative}: {actual}, expected {expected}")
    if (repo / "LICENSE").exists():
        raise RuntimeError("upstream now ships a LICENSE file; re-review redistribution constraints before continuing")
    return {"commit": commit, "files": statuses}


def verify_units(repo: Path) -> str:
    commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if commit != UNITS_EXPECTED_COMMIT:
        raise RuntimeError(f"voynich-units repo at {commit}, expected {UNITS_EXPECTED_COMMIT}")
    return commit


def verify_ewt(ewt_dir: Path) -> dict:
    statuses = {}
    for name, expected in EWT_EXPECTED_HASHES.items():
        actual = sha256(ewt_dir / name)
        statuses[name] = {"expected": expected, "actual": actual, "matches": actual == expected}
        if actual != expected:
            raise RuntimeError(f"checksum mismatch for {name}: {actual}, expected {expected}")
    return statuses


def apply_repair(cardan_repo: Path, workdir: Path) -> dict:
    """Copy the pinned repo into a scratch dir and apply the one documented repair."""
    import shutil

    dest = workdir / "cardan-repaired"
    dest.mkdir()
    for name in CARDAN_EXPECTED_HASHES:
        shutil.copy2(cardan_repo / name, dest / name)
    grille_path = dest / "grille.py"
    before_hash = sha256(grille_path)
    content = grille_path.read_text(encoding="utf-8")
    marker = "import signatures_v26 as ev   # evaluation pipeline"
    if marker not in content:
        raise RuntimeError("expected import line not found; upstream may have changed")
    repaired = content.replace(
        marker, "import signatures_v27 as ev   # evaluation pipeline (repaired: v26 not shipped, see manifest)"
    )
    grille_path.write_text(repaired, encoding="utf-8", newline="\n")
    after_hash = sha256(grille_path)
    return {"path": "grille.py", "before_sha256": before_hash, "after_sha256": after_hash, "repair": marker}


def load_ewt_words(ewt_dir: Path) -> tuple[list[str], int]:
    sys.path.insert(0, str(ROOT / "data" / "scripts"))
    from audit_document_baseline_panel import parse_documents  # type: ignore

    paths = [ewt_dir / "en_ewt-ud-train.conllu", ewt_dir / "en_ewt-ud-dev.conllu", ewt_dir / "en_ewt-ud-test.conllu"]
    documents, unassigned = parse_documents(paths)
    if len(documents) != EWT_EXPECTED_DOCUMENTS:
        raise RuntimeError(f"EWT document count {len(documents)} != {EWT_EXPECTED_DOCUMENTS}")
    if any(unassigned.values()):
        raise RuntimeError(f"EWT parse produced unassigned tokens: {unassigned}")
    words = [w for doc in documents.values() for w in doc["surface"]]
    if len(words) != EWT_EXPECTED_SURFACE_WORDS:
        raise RuntimeError(f"EWT surface word count {len(words)} != {EWT_EXPECTED_SURFACE_WORDS}")
    return words, len(documents)


def edge_rows(lines: list[list[str]]) -> list[tuple[int, str, str]]:
    return [
        (line_index, left[-1], right[0])
        for line_index, line in enumerate(lines)
        for left, right in zip(line, line[1:])
    ]


def edge_crossfit(lines: list[list[str]], alpha: float, blocks: int = 16) -> dict:
    rows = edge_rows(lines)
    total_gain, total_pairs, positive = 0.0, 0, 0
    for fold in range(blocks):
        lower = fold * len(lines) // blocks
        upper = (fold + 1) * len(lines) // blocks
        training = [row for row in rows if not lower <= row[0] < upper]
        testing = [row for row in rows if lower <= row[0] < upper]
        marginal = Counter(right for _, _, right in training)
        context = Counter((left, right) for _, left, right in training)
        left_count = Counter(left for _, left, _ in training)
        alphabet = set(marginal)
        categories = len(alphabet) + 1
        gain = 0.0
        for _, left, observed_right in testing:
            right = observed_right if observed_right in alphabet else "<unknown>"
            conditional = (context[(left, right)] + alpha) / (left_count[left] + alpha * categories)
            baseline = (marginal[right] + alpha) / (len(training) + alpha * categories)
            gain += math.log2(conditional / baseline)
        value = gain / len(testing)
        if value > 0:
            positive += 1
        total_gain += gain
        total_pairs += len(testing)
    return {"gain_bits_per_boundary": total_gain / total_pairs, "positive_blocks": positive, "blocks": blocks}


def evaluate_replicate(tokens: list[str], targets: dict, naibbe_module, scale, args, modules) -> dict:
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


def aggregate(rows: list[dict]) -> dict:
    metrics = ["H1", "H2", "bpe_minimum_checkpoint", "bpe_k64_gap", "token_order_share",
               "hapax_share_of_types", "edge_gain_bits_per_boundary", "edge_positive_blocks"]
    out = {"n": len(rows), "joint_pass": sum(1 for r in rows if r["all_six_pass"])}
    for m in metrics:
        values = [r[m] for r in rows]
        out[m] = {"mean": sum(values) / len(values), "min": min(values), "max": max(values)}
    for c in ("H1", "H2", "learned_units", "token_order_share", "edge", "hapax"):
        out[f"criterion_{c}_passes"] = sum(1 for r in rows if r["criteria_pass"][c])
    return out


def run(cardan_repo: Path, units_repo: Path, ewt_dir: Path, log) -> dict:
    cardan_source = verify_cardan(cardan_repo)
    units_commit = verify_units(units_repo)
    ewt_files = verify_ewt(ewt_dir)
    log(f"verified cardan commit {cardan_source['commit']}, units commit {units_commit}, EWT checksums OK")

    with tempfile.TemporaryDirectory(prefix="cardan-audit-") as workdir:
        repair = apply_repair(cardan_repo, Path(workdir))
        log(f"applied repair: {repair['before_sha256'][:12]} -> {repair['after_sha256'][:12]}")
        sys.path.insert(0, str(Path(workdir) / "cardan-repaired"))
        import grille  # type: ignore

        sys.path.insert(0, str(units_repo / "analysis"))
        naibbe_module = importlib.import_module("reproduce_naibbe_control")
        bundle = units_repo / "voynich_decipherment_repro_bundle"
        modules = naibbe_module.load_modules(bundle)
        _attack_lib, _attack_voynich, unit_probe, headlines, scale, _space, plant = modules

        eng_words, n_docs = load_ewt_words(ewt_dir)
        log(f"EWT: {len(eng_words)} surface words from {n_docs} documents")

        voy_tokens = naibbe_module.voynich_entropy_tokens(bundle, headlines)
        observed, _, _, _ = scale.load_voynich_lines(bundle, plant.LOCUS_RE, plant.collapse, plant.strip_markup)
        line_lengths = [len(line) for line in observed]
        pooled = unit_probe.voynich_lines()
        targets = {
            "entropy_tokens": len(voy_tokens),
            "line_lengths": line_lengths,
            "bpe_glyphs": sum(len(w) for ln in pooled for w in ln),
        }
        log(f"targets: entropy_tokens={targets['entropy_tokens']} lines={len(line_lengths)} "
            f"template_tokens={sum(line_lengths)}")

        rng999 = random.Random(999)
        rand_words = [
            "".join(rng999.choice(grille.ALL_GRAPHEMES) for _ in range(rng999.randint(2, 6)))
            for _ in range(max(37000, len(eng_words)))
        ]
        eng_sents = grille.words_to_sentences(eng_words, rng=random.Random(12345))

        args = SimpleNamespace(skip_attack=True, skip_crossing=True, shuffles=100, extra_k=[])
        replicates: dict[str, dict[str, dict]] = {}

        def run_config(name, seeds, make_cfg):
            bucket = replicates.setdefault(name, {})
            for seed in seeds:
                cfg = make_cfg(seed)
                t = time.time()
                sents = cfg.generate(seed=seed)
                tokens = [w for s in sents for w in s]
                bucket[str(seed)] = evaluate_replicate(tokens, targets, naibbe_module, scale, args, modules)
                log(f"{name} seed={seed}: all_six_pass={bucket[str(seed)]['all_six_pass']} ({time.time()-t:.1f}s)")

        for p_jump, label in [(0.00, "G_seq English p=0.00"), (0.05, "G_seq English p=0.05"),
                               (0.10, "G_seq English p=0.10"), (0.30, "G_seq English p=0.30")]:
            run_config(label, PRIMARY_SEEDS, lambda seed, p_jump=p_jump, label=label: grille.GrilleConfig(
                label, mode="SEQUENTIAL", n_holes=4, n_words=42000, p_jump=p_jump, source_words=eng_words))

        for p_jump, label in [(0.00, "G_seq Random p=0.00"), (1.00, "G_seq Random p=1.00")]:
            run_config(label, SENSITIVITY_SEEDS, lambda seed, p_jump=p_jump, label=label: grille.GrilleConfig(
                label, mode="SEQUENTIAL", n_holes=4, n_words=42000, p_jump=p_jump, source_words=rand_words))

        run_config("G8 LEARNED-ENGLISH+RANDOM", SENSITIVITY_SEEDS, lambda seed: grille.GrilleConfig(
            "G8 LEARNED-ENGLISH+RANDOM [honest]", table_rows=256, table_cols=10, n_holes=4,
            mode="RANDOM", col_skew=0.0, source_corpus=eng_sents, source_tokenizer=lambda w: list(w.lower()),
            n_words=42000))

    primary_names = [f"G_seq English p={p:.2f}" for p in (0.00, 0.05, 0.10, 0.30)]
    primary_joint_passes = {name: aggregate(list(replicates[name].values()))["joint_pass"] for name in primary_names}
    verdict = "PASS" if any(v >= 16 for v in primary_joint_passes.values()) else "FAIL"

    return {
        "source": {"cardan": cardan_source, "units_commit": units_commit, "ewt": ewt_files, "repair": repair},
        "protocol": "methods/cardan-grille-preregistration.md v1",
        "seeds": {"primary": PRIMARY_SEEDS, "sensitivity": SENSITIVITY_SEEDS,
                   "sensitivity_note": "reduced-N interpretive addendum; not part of the primary 16/20 rule"},
        "six_criteria": SIX_CRITERIA,
        "replicates": replicates,
        "aggregate": {name: aggregate(list(bucket.values())) for name, bucket in replicates.items()},
        "primary_verdict": verdict,
        "primary_joint_passes": primary_joint_passes,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cardan_repo", type=Path)
    parser.add_argument("units_repo", type=Path)
    parser.add_argument("--ewt-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=OUT_JSON)
    args = parser.parse_args()

    started = time.time()

    def log(message: str) -> None:
        print(f"[{time.time()-started:7.1f}s] {message}", flush=True)

    summary = run(args.cardan_repo.resolve(), args.units_repo.resolve(), args.ewt_dir.resolve(), log)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {args.output}; primary verdict: {summary['primary_verdict']}")


if __name__ == "__main__":
    main()
