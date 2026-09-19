#!/usr/bin/env python3
"""Validate the preregistered document-baseline panel without computing results."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unicodedata
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "baselines" / "document-panel-v1.json"


def letters_only(form: str) -> str:
    normalized = unicodedata.normalize("NFKC", form).lower()
    return "".join(character for character in normalized if character.isalpha())


def download(repository: str, commit: str, path: str, expected_sha: str, destination: Path) -> None:
    url = f"{repository.replace('github.com', 'raw.githubusercontent.com')}/{commit}/{path}"
    with urllib.request.urlopen(url, timeout=120) as response:
        content = response.read()
    actual = hashlib.sha256(content).hexdigest()
    if actual != expected_sha:
        raise RuntimeError(f"Checksum mismatch for {url}: expected {expected_sha}, got {actual}")
    destination.write_bytes(content)


def parse_documents(paths: list[Path]) -> tuple[dict[str, dict[str, list[str]]], dict[str, int]]:
    documents: dict[str, dict[str, list[str]]] = {}
    unassigned = {"syntactic": 0, "surface": 0}

    for path in paths:
        current: str | None = None
        covered_ids: set[int] = set()
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# newdoc id"):
                current = line.split("=", 1)[1].strip()
                if current in documents:
                    raise RuntimeError(f"Duplicate document ID {current!r} in {path.name}")
                documents[current] = {"syntactic": [], "surface": []}
                continue
            if not line:
                covered_ids.clear()
                continue
            if line.startswith("#"):
                continue

            columns = line.split("\t")
            if len(columns) != 10:
                continue
            token_id, form, _lemma, upos = columns[:4]

            if "-" in token_id:
                start, end = map(int, token_id.split("-"))
                word = letters_only(form)
                if word:
                    if current is None:
                        unassigned["surface"] += 1
                    else:
                        documents[current]["surface"].append(word)
                covered_ids.update(range(start, end + 1))
                continue
            if "." in token_id or upos in {"PUNCT", "SYM"}:
                continue

            word = letters_only(form)
            if not word:
                continue
            integer_id = int(token_id)
            if current is None:
                unassigned["syntactic"] += 1
                if integer_id not in covered_ids:
                    unassigned["surface"] += 1
                continue

            documents[current]["syntactic"].append(word)
            if integer_id not in covered_ids:
                documents[current]["surface"].append(word)

    return documents, unassigned


def view_audit(documents: dict[str, dict[str, list[str]]], view: str, minimum: int) -> dict[str, int]:
    streams = [document[view] for document in documents.values()]
    words = [word for stream in streams for word in stream]
    return {
        "tokens": len(words),
        "within_token_character_pairs": sum(len(word) - 1 for word in words),
        "single_character_tokens": sum(len(word) == 1 for word in words),
        "documents_ge_100_tokens": sum(len(stream) >= minimum for stream in streams),
    }


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    policy = manifest["document_policy"]

    with tempfile.TemporaryDirectory(prefix="voynich-panel-audit-") as temporary:
        temporary_root = Path(temporary)
        for corpus in manifest["corpora"]:
            corpus_root = temporary_root / corpus["key"]
            corpus_root.mkdir()
            paths: list[Path] = []
            for source in corpus["files"]:
                destination = corpus_root / source["path"]
                download(corpus["repository"], corpus["commit"], source["path"], source["sha256"], destination)
                paths.append(destination)

            documents, unassigned = parse_documents(paths)
            expected = corpus["audit"]
            if len(documents) != expected["explicit_documents"]:
                raise RuntimeError(f"{corpus['key']}: expected {expected['explicit_documents']} documents, got {len(documents)}")
            for view in ("syntactic", "surface"):
                observed = view_audit(documents, view, policy["document_level_minimum_tokens"])
                if observed != expected[view]:
                    raise RuntimeError(f"{corpus['key']} {view}: expected {expected[view]}, got {observed}")
                if unassigned[view] != expected[f"unassigned_{view}_tokens"]:
                    raise RuntimeError(
                        f"{corpus['key']} {view}: expected {expected[f'unassigned_{view}_tokens']} unassigned, got {unassigned[view]}"
                    )

            primary = expected[manifest["primary_token_view"]]
            if expected["explicit_documents"] < policy["minimum_unique_documents"]:
                raise RuntimeError(f"{corpus['key']}: too few explicit documents")
            if primary["documents_ge_100_tokens"] < policy["minimum_documents_with_100_primary_tokens"]:
                raise RuntimeError(f"{corpus['key']}: too few documents with 100 primary tokens")
            if primary["tokens"] < policy["minimum_primary_tokens"]:
                raise RuntimeError(f"{corpus['key']}: too few primary tokens")
            capped_capacity = sum(
                min(len(document[manifest["primary_token_view"]]), policy["maximum_tokens_from_one_document_per_replicate"])
                for document in documents.values()
            )
            if capped_capacity != expected["capped_surface_capacity"]:
                raise RuntimeError(
                    f"{corpus['key']}: expected capped capacity {expected['capped_surface_capacity']}, got {capped_capacity}"
                )
            if capped_capacity < manifest["target_tokens"]:
                raise RuntimeError(f"{corpus['key']}: document cap leaves too few usable primary tokens")
            print(
                f"PASS {corpus['key']}: {expected['explicit_documents']} docs; "
                f"surface={expected['surface']['tokens']:,}; syntactic={expected['syntactic']['tokens']:,}; "
                f"capped capacity={capped_capacity:,}"
            )

    print("Manifest audit passed. No constraint values were computed.")


if __name__ == "__main__":
    main()
