#!/usr/bin/env python3
"""Offline regression checks for the Yale retrieval kit's validation gate.

These synthetic bytes are not Yale images. No network request is made.
Run: python3 data/scripts/test_yale_ten_folio_native_fetch_validation.py
"""
import contextlib
import csv
import hashlib
import io
import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

import yale_ten_folio_native_fetch as kit


class ValidationGateTest(unittest.TestCase):
    def run_case(self, failed_check=None):
        small = b"synthetic-1200-image"
        native = bytes.fromhex("ffd8ffc000110800100010") + b"\x00" * 20
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            repo = root / "repo"
            (repo / "research").mkdir(parents=True)
            manifest = repo / "research" / "manifest.csv"
            receipt = repo / "research" / "receipt.csv"
            template = repo / "research" / "template.csv"
            with manifest.open("w", newline="") as fh:
                writer = csv.DictWriter(fh, fieldnames=["folio_ids", "canvas_index",
                                                        "iiif_1200px_url", "sha256"])
                writer.writeheader()
                for index, folio in enumerate(kit.FOLIOS):
                    digest = hashlib.sha256(small).hexdigest()
                    if failed_check == "manifest_1200_hash_match" and index == 9:
                        digest = "0" * 64
                    writer.writerow({"folio_ids": folio, "canvas_index": index,
                                     "iiif_1200px_url":
                                     f"https://collections.library.yale.edu/iiif/2/{1000 + index}/full/1200,/0/default.jpg",
                                     "sha256": digest})

            def fake_get(url, timeout=120):
                if url.endswith("/info.json"):
                    width = 15 if failed_check == "native_dims_match_info" and "/1009/" in url else 16
                    return json.dumps({"width": width, "height": 16}).encode()
                if "/full/full/" in url:
                    return b"not a jpeg" if failed_check == "native_jpeg_ok" and "/1009/" in url else native
                if "/full/1200,/" in url:
                    return small
                raise AssertionError(url)

            with mock.patch.multiple(kit, REPO=str(repo), MANIFEST=str(manifest),
                                     RECEIPT=str(receipt), TEMPLATE=str(template), get=fake_get), \
                 mock.patch.object(kit.time, "sleep", return_value=None), \
                 mock.patch.object(sys, "argv", ["kit", "--image-dir", str(root / "images")]), \
                 contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit) as result:
                    kit.main()
            with receipt.open(newline="") as fh:
                rows = list(csv.DictReader(line for line in fh if not line.startswith("#")))
            self.assertEqual(len(rows), 10)
            self.assertEqual(result.exception.code, 0 if failed_check is None else 1)
            self.assertEqual(template.exists(), failed_check is None)
            if failed_check:
                self.assertIn(failed_check, rows[-1]["error"])
            else:
                self.assertTrue(all(not row["error"] for row in rows))

    def test_valid_rows_create_template(self):
        self.run_case()

    def test_hash_mismatch_blocks_template(self):
        self.run_case("manifest_1200_hash_match")

    def test_dimension_mismatch_blocks_template(self):
        self.run_case("native_dims_match_info")

    def test_non_jpeg_blocks_template(self):
        self.run_case("native_jpeg_ok")

    def test_prior_template_blocks_rerun_before_receipt_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            repo = root / "repo"
            (repo / "research").mkdir(parents=True)
            receipt = repo / "research" / "receipt.csv"
            template = repo / "research" / "template.csv"
            receipt.write_text("old receipt\n")
            template.write_text("old scoring work\n")
            with mock.patch.multiple(kit, REPO=str(repo), RECEIPT=str(receipt),
                                     TEMPLATE=str(template)), \
                 mock.patch.object(sys, "argv", ["kit", "--image-dir", str(root / "images")]), \
                 mock.patch.object(kit, "get", side_effect=AssertionError("fetch must not start")):
                with self.assertRaises(SystemExit) as result:
                    kit.main()
            self.assertNotEqual(result.exception.code, 0)
            self.assertEqual(receipt.read_text(), "old receipt\n")
            self.assertEqual(template.read_text(), "old scoring work\n")


if __name__ == "__main__":
    unittest.main()
