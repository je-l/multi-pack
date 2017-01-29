#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Lempel–Ziv–Welch compression algorithm example, with small dictionary."""


class Lzw:
    """Lempel-Ziv-Welch compression example."""

    def __init__(self, stream):
        self.stream = stream
        self.dictionary = None
        self.index = 0
        self.str = ""
        self.init_dict()

    def dict_add(self, dict_string):
        """Add new string to dictionary, and increment the index. Key is a
        string and value is integer index.
        :param dict_string: new string for the dictionary.
        """
        self.dictionary[dict_string] = self.index
        self.index += 1

    def init_dict(self):
        """Initialize the dictionary with few letters. Normally this would
        be some 8-bit charset.
        """
        self.dictionary = {}
        self.dict_add("a")
        self.dict_add("b")
        self.dict_add("d")
        self.dict_add("n")
        self.dict_add(" ")

    def compress(self):
        """Compress the input stream into 12-bit indexes.
        :return yields three bytes for every two 12-bit integers."""
        int_iter = iter(self.lzw())
        for first_int in int_iter:
            second_int = next(int_iter)
            byte1, byte2, byte3 = int12_to_int8(first_int, second_int)
            yield byte1
            yield byte2
            yield byte3

    def lzw(self):
        """Compress the string using the dictionary.
        :return: a generator of dictionary keys.
        """
        char = self.stream.read(1)
        while len(char) > 0:
            if self.str + char in self.dictionary:
                self.str = self.str + char
            else:
                yield self.dictionary[self.str]
                self.dict_add(self.str + char)
                self.str = char
            char = self.stream.read(1)
        yield self.dictionary[self.str]

    def init_uncompress_dict(self):
        """Initialize dictionary for uncompression"""
        self.dictionary = ["a", "b", "d", "n", " "]
        # self.dictionary = ["a", "b"]

    def uncompress(self):
        """Uncompress with lzw."""
        self.init_uncompress_dict()
        indexes = [bits.uint for bits in self.stream.cut(12)]
        print("Compressed disk usage: {} bytes".format(len(indexes) * 12 // 8))
        prev_index = indexes[0]
        entry = None
        print("Uncompressed text: [", end="")
        print(self.dictionary[prev_index], end="")

        for index in indexes[1:]:
            if index >= len(self.dictionary):
                entry = entry + entry[0]
            else:
                entry = self.dictionary[index]
            print(entry, end="")
            char = entry[0]
            new = self.dictionary[prev_index] + char
            self.dictionary.append(new)
            prev_index = index
        print("]")
        print("Uncompression dict:", self.dictionary)


def int12_to_int8(first, second):
    """Convert two 12-bit integers to three 8-bit integers for serialization.
    :param first: First 12-bit integer for conversion.
    :param second: Second 12-bit integer for conversion.
    :return: tuple of three 8-bit integers.
    """
    if first > 4095 or second > 4095:
        raise Exception("More than 12 bits")
    byte_1 = first >> 4
    byte_2_start = first << 4
    byte_2 = shift_mask(byte_2_start)
    byte_2 |= second >> 8
    byte_3 = shift_mask(second)

    return byte_1, byte_2, byte_3


def shift_mask(bits):
    """Drop bits from the left until 8 bits are left.
    :Example:
        0b101011110000 -> 0b11110000"""
    if bits.bit_length() < 9:
        return bits
    return 0xff & bits
