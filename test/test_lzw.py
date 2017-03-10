#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Test for lzw."""

import unittest
import io

import multipack.lzw as lzw


class TestLzw(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open("LICENSE", "rb") as in_stream:
            lzw_compressor = lzw.Lzw(in_stream)
            with open("test_output.lzw", "wb") as out_stream:
                for byte in lzw_compressor.compress():
                    out_stream.write(bytes([byte]))

    def test_lzw_example_empty_dict(self):
        with io.StringIO("") as empty_stream:
            lzw_e = lzw.Lzw(empty_stream)
            lzw_e.compress()
            self.assertEqual(len(lzw_e.dictionary), 256)

    def test_lzw_small_string(self):
        with io.StringIO("banana bandana " * 2) as stream:
            lzw_encoder = lzw.Lzw(stream)
            lzw_encoder.compress()
            self.assertEqual(len(lzw_encoder.dictionary), 256)

    def test_lzw_uncompression(self):
        with open("test_output.lzw", "rb") as in_stream:
            lzw_decoder = lzw.Lzw(in_stream)
            lzw_decoder.uncompress()
            self.assertEqual(256, len(lzw_decoder.dictionary))

    def test_lzw_uncompression_long(self):
        with open("test_output.lzw", "rb") as in_stream:
            lzw_decoder = lzw.Lzw(in_stream)
            byte_gen = lzw_decoder.uncompress()
            with open("LICENSE") as original_file:
                data = original_file.read()

            output = b""
            for byte in byte_gen:
                output += byte
            self.assertEqual(len(data), len(output))

    def test_lzw_uncompression_every_byte(self):
        with open("test_output.lzw", "rb") as in_stream:
            lzw_decoder = lzw.Lzw(in_stream)
            with open("test_output", "wb") as outfile:
                for byte in lzw_decoder.uncompress():
                    outfile.write(byte)

    def test_bit_convert_zeros(self):
        byte_1, byte_2, byte_3 = lzw._int12_to_int8(0, 0)
        self.assertEqual(byte_1, 0b0)
        self.assertEqual(byte_2, 0b0)
        self.assertEqual(byte_3, 0b0)

    def test_bit_convert_small(self):
        byte_1, byte_2, byte_3 = lzw._int12_to_int8(1, 1)
        self.assertEqual(byte_1, 0b0)
        self.assertEqual(byte_2, 0b10000)
        self.assertEqual(byte_3, 0b1)

    def test_bit_convert_smallish(self):
        byte_1, byte_2, byte_3 = lzw._int12_to_int8(8, 8)
        self.assertEqual(byte_1, 0b0)
        self.assertEqual(byte_2, 0b10000000)
        self.assertEqual(byte_3, 0b1000)

    def test_bit_convert_almost_max(self):
        byte_1, byte_2, byte_3 = lzw._int12_to_int8(4094, 4094)
        self.assertEqual(byte_1, 0b11111111)
        self.assertEqual(byte_2, 0b11101111)
        self.assertEqual(byte_3, 0b11111110)

    def test_bit_convert_max(self):
        byte_1, byte_2, byte_3 = lzw._int12_to_int8(4095, 4095)
        self.assertEqual(byte_1, 0b11111111)
        self.assertEqual(byte_2, 0b11111111)
        self.assertEqual(byte_3, 0b11111111)

    def test_bit_convert_different_indexes(self):
        byte_1, byte_2, byte_3 = lzw._int12_to_int8(55, 4000)
        self.assertEqual(byte_1, 0b11)
        self.assertEqual(byte_2, 0b1111111)
        self.assertEqual(byte_3, 0b10100000)

    def test_bit_convert_one_int(self):
        byte_1, byte_2 = lzw._int12_to_int8(1)
        self.assertEqual(byte_1, 0b0)
        self.assertEqual(byte_2, 0b10000)

    def test_bit_convert_one_int_max(self):
        byte_1, byte_2 = lzw._int12_to_int8(4095)
        self.assertEqual(byte_1, 0b11111111)
        self.assertEqual(byte_2, 0b11110000)

    def test_bit_convert_one_int_min(self):
        byte_1, byte_2 = lzw._int12_to_int8(0)
        self.assertEqual(byte_1, 0b0)
        self.assertEqual(byte_2, 0b0)

    def test_bit_convert_one_int_almost_max(self):
        byte_1, byte_2 = lzw._int12_to_int8(4093)
        self.assertEqual(byte_1, 0b11111111)
        self.assertEqual(byte_2, 0b11010000)

    def test_12bit_convert_minimum(self):
        byte_1 = lzw._int8_to_int12(0b0, 0b0)
        self.assertEqual(byte_1, 0b0)

    def test_12bit_convert_medium(self):
        byte_1, byte_2 = lzw._int8_to_int12(0b10, 0b10, 0b10)
        self.assertEqual(byte_1, 0b100000)
        self.assertEqual(byte_2, 0b1000000010)

    def test_12bit_convert_maximum(self):
        byte_1, byte_2 = lzw._int8_to_int12(0b11111111, 0b11111111, 0b11111111)
        self.assertEqual(byte_1, 0b111111111111)
        self.assertEqual(byte_2, 0b111111111111)

    def test_12bit_convert_almost_maximum(self):
        byte_1, byte_2 = lzw._int8_to_int12(0b1111111, 0b1111111, 0b1111111)
        self.assertEqual(byte_1, 0b11111110111)
        self.assertEqual(byte_2, 0b111101111111)
