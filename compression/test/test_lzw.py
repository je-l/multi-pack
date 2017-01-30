#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Test for lzw."""

import unittest
import io
from bitstring import BitStream
from .. import lzw


class TestLzw(unittest.TestCase):
    def setUp(self):
        with io.StringIO("banana bandana " * 2) as in_stream:
            lzw_compressor = lzw.Lzw(in_stream)
            with open("test_output.lzw", "wb") as out_stream:
                for byte in lzw_compressor.compress():
                    out_stream.write(byte.to_bytes(1, byteorder="little"))

    def test_lzw_example_empty_dict(self):
        with io.StringIO("") as empty_stream:
            lzw_e = lzw.Lzw(empty_stream)
            self.assertEqual(len(lzw_e.dictionary), 5)

    def test_lzw_small_string(self):
        with io.StringIO("banana bandana " * 2) as stream:
            lzw_encoder = lzw.Lzw(stream)
            lzw_encoder.compress()
            self.assertEqual(len(lzw_encoder.dictionary), 5)

    def test_lzw_uncompression(self):
        stream = BitStream(filename="test_output.lzw")
        lzw_decoder = lzw.Lzw(stream)
        lzw_decoder.uncompress()
        self.assertEqual(5, len(lzw_decoder.dictionary))

    def test_shift_mask_empty_binary(self):
        result = lzw.shift_mask(0b0)
        self.assertEqual(result, 0b0)

    def test_shift_mask_two_byte_max(self):
        result = lzw.shift_mask(0b1111111111111111)
        self.assertEqual(result, 0b11111111)

    def test_shift_mask_one_byte_max(self):
        result = lzw.shift_mask(0b11111111)
        self.assertEqual(result, 0b11111111)

    def test_shift_mask_one(self):
        result = lzw.shift_mask(0b1)
        self.assertEqual(result, 0b1)

    def test_shift_mask_9_bits(self):
        result = lzw.shift_mask(0b111111111)
        self.assertEqual(result, 0b11111111)

    def test_shift_mask_leading_zero(self):
        result = lzw.shift_mask(0b000001111111)
        self.assertEqual(result, 0b1111111)

    def test_bit_convert_zeros(self):
        byte_1, byte_2, byte_3 = lzw.int12_to_int8(0, 0)
        self.assertEqual(byte_1, 0b0)
        self.assertEqual(byte_2, 0b0)
        self.assertEqual(byte_3, 0b0)

    def test_bit_convert_small(self):
        byte_1, byte_2, byte_3 = lzw.int12_to_int8(1, 1)
        self.assertEqual(byte_1, 0b0)
        self.assertEqual(byte_2, 0b10000)
        self.assertEqual(byte_3, 0b1)

    def test_bit_convert_smallish(self):
        byte_1, byte_2, byte_3 = lzw.int12_to_int8(8, 8)
        self.assertEqual(byte_1, 0b0)
        self.assertEqual(byte_2, 0b10000000)
        self.assertEqual(byte_3, 0b1000)

    def test_bit_convert_almost_max(self):
        byte_1, byte_2, byte_3 = lzw.int12_to_int8(4094, 4094)
        self.assertEqual(byte_1, 0b11111111)
        self.assertEqual(byte_2, 0b11101111)
        self.assertEqual(byte_3, 0b11111110)

    def test_bit_convert_max(self):
        byte_1, byte_2, byte_3 = lzw.int12_to_int8(4095, 4095)
        self.assertEqual(byte_1, 0b11111111)
        self.assertEqual(byte_2, 0b11111111)
        self.assertEqual(byte_3, 0b11111111)

    def test_bit_convert_different_indexes(self):
        byte_1, byte_2, byte_3 = lzw.int12_to_int8(55, 4000)
        self.assertEqual(byte_1, 0b11)
        self.assertEqual(byte_2, 0b1111111)
        self.assertEqual(byte_3, 0b10100000)

    def test_bit_convert_one_int(self):
        byte_1, byte_2 = lzw.int12_to_int8(1)
        self.assertEqual(byte_1, 0b0)
        self.assertEqual(byte_2, 0b10000)

    def test_bit_convert_one_int_max(self):
        byte_1, byte_2 = lzw.int12_to_int8(4095)
        self.assertEqual(byte_1, 0b11111111)
        self.assertEqual(byte_2, 0b11110000)

    def test_bit_convert_one_int_min(self):
        byte_1, byte_2 = lzw.int12_to_int8(0)
        self.assertEqual(byte_1, 0b0)
        self.assertEqual(byte_2, 0b0)

    def test_bit_convert_one_int_almost_max(self):
        byte_1, byte_2 = lzw.int12_to_int8(4093)
        self.assertEqual(byte_1, 0b11111111)
        self.assertEqual(byte_2, 0b11010000)
