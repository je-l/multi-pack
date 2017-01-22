#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

import unittest
import io
from .. import lzw


class TestLzw(unittest.TestCase):

    def test_lzw_example_empty_dict(self):
        with io.StringIO("") as empty_stream:
            lzw_e = lzw.Lzw(empty_stream)
            self.assertEqual(len(lzw_e.dictionary), 5)

    def test_lzw_small_string(self):
        with io.StringIO("banana bandana") as stream:
            lzw_encoder = lzw.Lzw(stream)
            self.assertEqual(len(lzw_encoder.dictionary), 5)
