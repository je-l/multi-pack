#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Test for burrows-wheeler transform."""

import unittest
import io

from multipack.bwt import *


class TestBwt(unittest.TestCase):

    def test_transformed_len(self):
        with open("LICENSE") as f:
            length = len([i for i in bwt_encode(f)])
            self.assertEqual(1065, length)

    def test_create_table_empty(self):
        table = create_table("")
        self.assertEqual([], table)

    def test_create_table_short(self):
        table = create_table("a")
        self.assertEqual(["a"], table)

    def test_create_table_short_2(self):
        table = create_table("abcde")
        self.assertEqual(["abcde", "bcdea", "cdeab", "deabc", "eabcd"], table)

    def test_find_etx(self):
        table = ["fo\003o", "bar\003"]
        self.assertEqual("bar\003", find_decoded(table))

    def test_rle_empty(self):
        with io.StringIO("") as empty_stream:
            encoded = rle_encode(empty_stream)
            self.assertEqual("", encoded)

    def test_rle_one_char(self):
            with io.StringIO("a") as empty_stream:
                encoded = rle_encode(empty_stream)
                self.assertEqual("a1", encoded)

    def test_rle_short(self):
            with io.StringIO("abcc") as empty_stream:
                encoded = rle_encode(empty_stream)
                self.assertEqual("a1b1c2", encoded)

    def test_rle_short2(self):
            with io.StringIO("aabbccddeeeee") as empty_stream:
                encoded = rle_encode(empty_stream)
                self.assertEqual("a2b2c2d2e5", encoded)

    def test_rle_long(self):
            with io.StringIO("a" * 100) as empty_stream:
                encoded = rle_encode(empty_stream)
                self.assertEqual("a100", encoded)

    def test_rle_long2(self):
            with io.StringIO("a" * 257) as empty_stream:
                encoded = rle_encode(empty_stream)
                self.assertEqual("a256a1", encoded)
