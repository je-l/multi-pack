#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Lempel–Ziv–Welch compression algorithm example, with small dictionary."""


class Lzw:
    """Lempel-Ziv-Welch compression example."""

    def __init__(self, stream):
        self.stream = stream
        self.dictionary = None
        self.index = 0
        self.str = b""
        self.max = 2 ** 12
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
        for i in range(256):
            self.dict_add(bytes([i]))

    def compress(self):
        """Compress the input stream into 12-bit indexes.
        :return yields three bytes for every two 12-bit integers."""
        indices = self.lzw()
        for first_int in indices:
            second_int = next(indices, None)
            for byte in int12_to_int8(first_int, second_int):
                yield byte

    def lzw(self):
        """Compress the string using the dictionary.
        :return: a generator of dictionary keys.
        """
        char = self.stream.read(1)
        while len(char) > 0:
            if self.str + char in self.dictionary:
                self.str = self.str + char
            else:
                if len(self.str) == 0:
                    pass
                else:
                    yield self.dictionary[self.str]
                if len(self.dictionary) < self.max:
                    self.dict_add(self.str + char)
                self.str = char
            char = self.stream.read(1)
        yield self.dictionary[self.str]

    def init_uncompress_dict(self):
        """Initialize dictionary for uncompression"""
        self.dictionary = []
        for i in range(256):
            self.dictionary.append(bytes([i]))

    def uncompress(self):
        """Uncompress with lzw."""
        self.init_uncompress_dict()
        indices = [bit.uint for bit in self.stream.cut(12)]
        prev_index = indices[0]
        entry = None
        yield self.dictionary[prev_index]

        for index in indices[1:]:
            if index >= len(self.dictionary):
                entry += bytes([entry[0]])
            else:
                entry = self.dictionary[index]
            yield entry
            char = bytes([entry[0]])
            new = self.dictionary[prev_index] + char
            if len(self.dictionary) < self.max:
                self.dictionary.append(new)
            prev_index = index


def int12_to_int8(first, second=None):
    """Convert two 12-bit integers to three 8-bit integers for serialization.
    :param first: First 12-bit integer for conversion.
    :param second: Second 12-bit integer for conversion.
    :return: tuple of three 8-bit integers.
    """
    if first > 4095 or (second is not None and second > 4095):
        raise Exception("More than 12 bits")
    byte_1 = first >> 4
    byte_2_start = first << 4
    byte_2 = shift_mask(byte_2_start)
    if second is None:
        return byte_1, byte_2
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
