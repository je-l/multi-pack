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
        with io.BytesIO(b"") as empty_stream:
            encoded = rle_encode(empty_stream)
            self.assertEqual(b"", encoded)

    def test_rle_encoding_one_char(self):
        with io.BytesIO(b"a") as stream:
            encoded = rle_encode(stream)
            self.assertEqual(b"a\x01", encoded)

    def test_rle_encoding_short(self):
        with io.BytesIO(b"abcc") as stream:
            encoded = rle_encode(stream)
            self.assertEqual(b"a\x01b\x01c\x02", encoded)

    def test_rle_encoding_short2(self):
        with io.BytesIO(b"aabbccddeeeee") as stream:
            encoded = rle_encode(stream)
            self.assertEqual(b"a\x02b\x02c\x02d\x02e\x05", encoded)

    def test_rle_encoding_long(self):
        with io.BytesIO(b"a" * 100) as stream:
            encoded = rle_encode(stream)
            self.assertEqual(b"a\x64", encoded)

    def test_rle_encoding_long2(self):
        with io.BytesIO(b"a" * 256) as stream:
            encoded = rle_encode(stream)
            self.assertEqual(b"a\xffa\x01", encoded)

    def test_rle_decoding_empty(self):
        with io.BytesIO(b"") as stream:
            decoded = b"".join(rle_decode(stream))
            self.assertEqual(b"", decoded)

    def test_rle_decoding_short(self):
        with io.BytesIO(b"a\x01") as stream:
            decoded = b"".join(rle_decode(stream))
            self.assertEqual(b"a", decoded)

    def test_rle_decoding_short2(self):
        with io.BytesIO(b"a\x02") as stream:
            decoded = b"".join(rle_decode(stream))
            self.assertEqual(b"aa", decoded)

    def test_rle_decoding_short3(self):
        with io.BytesIO(b"a\x02b\x01") as stream:
            decoded = b"".join(rle_decode(stream))
            self.assertEqual(b"aab", decoded)

    def test_rle_decoding_long(self):
        with io.BytesIO(b"a\xffa\xffc\x05") as stream:
            decoded = b"".join(rle_decode(stream))
            expected = b"a" * 510 + b"ccccc"
            self.assertEqual(expected, decoded)
