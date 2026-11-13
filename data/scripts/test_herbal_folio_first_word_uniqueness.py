#!/usr/bin/env python3
"""Regression tests for IVTFF drawing-intrusion word boundaries."""
import unittest

from herbal_folio_first_word_uniqueness import words_of


class DrawingIntrusionBoundaryTests(unittest.TestCase):
    def test_aligned_drawing_intrusion_is_a_word_boundary(self):
        self.assertEqual(words_of("alpha<->beta"), ["alpha", "beta"])

    def test_misaligned_drawing_intrusion_is_a_word_boundary(self):
        self.assertEqual(words_of("alpha<~>beta"), ["alpha", "beta"])


if __name__ == "__main__":
    unittest.main()
