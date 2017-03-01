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
        decoded = bwt_decode(bytes([i]) for i in b"\x03\x02")
        self.assertEqual(b"", b"".join(decoded))

    def test_bwt_decode_short(self):
        decoded = bwt_decode(bytes([i]) for i in b"\x03ilimo\x02yit k")
        self.assertEqual(b"kyl toimii", b"".join(decoded))

    def test_bwt_enc_and_decode(self):
        string = b"kyl toimii"
        encoded = bwt_encode(io.BytesIO(string))
        self.assertEqual(string, b"".join(bwt_decode(encoded)))

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
        input = b""
        self.assertEqual(b"", rle_enc(input))

    def test_rle_encoding_one_char(self):
        inp = b"a"
        self.assertEqual(b"a\x01", rle_enc(inp))

    def test_rle_encoding_short(self):
        inp = b"abcc"
        self.assertEqual(b"a\x01b\x01c\x02", rle_enc(inp))

    def test_rle_encoding_short2(self):
        inp = b"aabbccddeeeee"
        self.assertEqual(b"a\x02b\x02c\x02d\x02e\x05", rle_enc(inp))

    def test_rle_encoding_long(self):
        inp = b"a" * 100
        self.assertEqual(b"a\x64", rle_enc(inp))

    def test_rle_encoding_long2(self):
        inp = b"a" * 256
        self.assertEqual(b"a\xffa\x01", rle_enc(inp))

    def test_rle_decoding_empty(self):
        input = b""
        expected = b""
        self.assertEqual(expected, rle_dec(input))

    def test_rle_decoding_short(self):
        input = b"a\x01"
        expected = b"a"
        self.assertEqual(expected, rle_dec(input))

    def test_rle_decoding_short2(self):
        input = b"a\x02"
        expected = b"aa"
        self.assertEqual(expected, rle_dec(input))

    def test_rle_decoding_short3(self):
        input = b"a\x02b\x01"
        expected = b"aab"
        self.assertEqual(expected, rle_dec(input))

    def test_rle_decoding_long(self):
        inp = b"a\xffa\xffc\x05"
        expected = b"a" * 510 + b"ccccc"
        self.assertEqual(expected, rle_dec(inp))

    def test_rle_enc_dec(self):
        inp = b"abbcc"
        self.assertEqual(inp, rle_enc_dec(inp))

    def test_rle_enc_dec2(self):
        inp = b"abc"
        self.assertEqual(inp, rle_enc_dec(inp))

    def test_rle_enc_dec3(self):
        inp = b"a" * 1000 + b"abcnewianwuibvureb"
        self.assertEqual(inp, rle_enc_dec(inp))

    def test_bwt_and_rle_short(self):
        inp = b"abc"
        self.assertEqual(inp, bwt_rle_combined(inp))

    def test_bwt_and_rle_empty(self):
        inp = b""
        self.assertEqual(inp, bwt_rle_combined(inp))

    def test_bwt_and_rle_medium(self):
        inp = b"aaaaaaaabbbcifjejiefieeeeeeeeee" + (b"p" * 10)
        self.assertEqual(inp, bwt_rle_combined(inp))


def bwt_rle_combined(bytes_input):
    with io.BytesIO(bytes_input) as input_stream:
        bwt_encoded = bwt_encode(input_stream)
        rle_encoded = rle_encode(bwt_encoded)
        with io.BytesIO(rle_encoded) as rle_stream:
            bwt_enc = b"".join(rle_decode(rle_stream))
            bwt_decoded = bwt_decode(bytes([i]) for i in bwt_enc)
            return b"".join(bwt_decoded)


def rle_enc_dec(bytes_input):
    encoded = rle_encode(bytes([i]) for i in bytes_input)
    with io.BytesIO(encoded) as stream:
        decoded = b"".join(rle_decode(stream))
        return decoded


def rle_dec(bytes_input):
    with io.BytesIO(bytes_input) as stream:
        decoded = b"".join(rle_decode(stream))
        return decoded


def rle_enc(bytes_input):
    return rle_encode(bytes([i]) for i in bytes_input)
