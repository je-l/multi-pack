#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Tests for burrows-wheelers transform and run-length encoding."""

import unittest
import io

from multipack.bwt import *


class TestBwt(unittest.TestCase):

    def test_bwt_len(self):
        with open("LICENSE", "rb") as f:
            length = len([i for i in bwt_encode(f)])
            self.assertEqual(1065, length)

    def test_bwt_empty(self):
        with io.BytesIO(b"") as stream:
            encoded = b"".join(bwt_encode(stream))
            self.assertEqual(b"\x03\x02", encoded)

    def test_bwt_short(self):
        with io.BytesIO(b"a") as stream:
            encoded = b"".join(bwt_encode(stream))
            self.assertEqual(b"\x03a\x02", encoded)

    def test_bwt_short2(self):
        with io.BytesIO(b"ab") as stream:
            encoded = b"".join(bwt_encode(stream))
            self.assertEqual(b"\x03b\x02a", encoded)

    def test_bwt_decode_empty(self):
        decoded = bwt_decode(b"\x03\x02")
        self.assertEqual(b"", decoded)

    def test_bwt_decode_short(self):
        decoded = bwt_decode(b"\x03ilimo\x02yit k")
        self.assertEqual(b"kyl toimii", decoded)

    def test_bwt_enc_and_decode(self):
        with io.BytesIO(b"kyl toimii") as stream:
            encoded = b"".join(bwt_encode(stream))
            decoded = bwt_decode(encoded)
            self.assertEqual(b"kyl toimii", decoded)

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
        table = [b"fo\x02o", b"bar\x03"]
        self.assertEqual(b"bar\x03", find_decoded(table))

    def test_rle_empty(self):
        with io.BytesIO(b"") as empty_stream:
            encoded = rle_encode(empty_stream)
            self.assertEqual(b"", encoded)

    def test_rle_encoding_one_char(self):
        stream = b"a"
        encoded = rle_encode(bytes([i]) for i in stream)
        self.assertEqual(b"a\x01", encoded)

    def test_rle_encoding_short(self):
        stream = b"abcc"
        encoded = rle_encode(bytes([i]) for i in stream)
        self.assertEqual(b"a\x01b\x01c\x02", encoded)

    def test_rle_encoding_short2(self):
        stream = b"aabbccddeeeee"
        encoded = rle_encode(bytes([i]) for i in stream)
        self.assertEqual(b"a\x02b\x02c\x02d\x02e\x05", encoded)

    def test_rle_encoding_long(self):
        stream = b"a" * 100
        encoded = rle_encode(bytes([i]) for i in stream)
        self.assertEqual(b"a\x64", encoded)

    def test_rle_encoding_long2(self):
        stream = b"a" * 256
        encoded = rle_encode(bytes([i]) for i in stream)
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

    def test_rle_enc_dec(self):
        inp = b"abbcc"
        encoded = rle_encode(bytes([i]) for i in inp)
        with io.BytesIO(encoded) as stream:
            decoded = b"".join(rle_decode(stream))
            self.assertEqual(inp, decoded)

    def test_rle_enc_dec2(self):
        inp = b"abc"
        encoded = rle_encode(bytes([i]) for i in inp)
        with io.BytesIO(encoded) as stream:
            decoded = b"".join(rle_decode(stream))
            self.assertEqual(inp, decoded)

    def test_rle_enc_dec3(self):
        inp = b"a" * 1000 + b"abcnewianwuibvureb"
        encoded = rle_encode(bytes([i]) for i in inp)
        with io.BytesIO(encoded) as stream:
            decoded = b"".join(rle_decode(stream))
            self.assertEqual(inp, decoded)

    def test_bwt_and_rle_short(self):
        inp = b"abc"
        with io.BytesIO(inp) as input_stream:
            bwt_encoded = bwt_encode(input_stream)
            rle_encoded = rle_encode(bwt_encoded)
            with io.BytesIO(rle_encoded) as rle_stream:
                bwt_enc = b"".join(rle_decode(rle_stream))
                bwt_decoded = bwt_decode(bwt_enc)
                self.assertEqual(inp, bwt_decoded)

    def test_bwt_and_rle_empty(self):
        inp = b""
        with io.BytesIO(inp) as input_stream:
            bwt_encoded = bwt_encode(input_stream)
            rle_encoded = rle_encode(bwt_encoded)
            with io.BytesIO(rle_encoded) as rle_stream:
                bwt_enc = b"".join(rle_decode(rle_stream))
                bwt_decoded = bwt_decode(bwt_enc)
                self.assertEqual(inp, bwt_decoded)

    def test_bwt_and_rle_medium(self):
        inp = b"aaaaaaaabbbcifjejiefieeeeeeeeee" + (b"p" * 10)
        with io.BytesIO(inp) as input_stream:
            bwt_encoded = bwt_encode(input_stream)
            rle_encoded = rle_encode(bwt_encoded)
            with io.BytesIO(rle_encoded) as rle_stream:
                bwt_enc = b"".join(rle_decode(rle_stream))
                bwt_decoded = bwt_decode(bwt_enc)
                self.assertEqual(inp, bwt_decoded)
