#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Lempel–Ziv–Welch compression algorithm example, with 4096 dictionary size."""

from multipack.datastructures import HashTable, DynamicArray


class Lzw:
    """Lempel-Ziv-Welch compression implementation."""

    def __init__(self, stream, dict_size=4096):
        self.stream = stream
        self.dictionary = None
        self.index = 0
        self.str = b""
        self.max = dict_size
        self.init_dict()

    def dict_add(self, dict_string):
        """Add new string to dictionary, and increment the index. Key is a
        string and value is integer index.
        :param dict_string: new string for the dictionary.
        """
        self.dictionary[dict_string] = self.index
        self.index += 1

    def init_dict(self):
        """Initialize the dictionary with 256 characters."""
        self.dictionary = HashTable()
        for i in range(256):
            self.dict_add(bytes([i]))

    def compress(self):
        """Compress the input stream into 12-bit indexes.
        :return: yields three bytes for every two 12-bit integers.
        """
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
                yield self.dictionary[self.str]
                if len(self.dictionary) < self.max:
                    self.dict_add(self.str + char)
                self.str = char
            char = self.stream.read(1)
        yield self.dictionary[self.str]

    def init_uncompress_dict(self):
        """Initialize dictionary for uncompression"""
        self.dictionary = DynamicArray()
        for i in range(256):
            self.dictionary.append(bytes([i]))

    def uncompress(self):
        """Uncompress with lzw.
        :return: Generator for the uncompressed bytes.
        """
        self.init_uncompress_dict()
        deserializer = self.deserializer()
        prev_index = next(deserializer)
        entry = b""
        yield self.dictionary[prev_index]

        for index in deserializer:
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

    def deserializer(self):
        """Read the binary stream until there is no more characters.
        :return: Indices for the dictionary.
        """
        while True:
            byte_1 = self.stream.read(1)
            byte_2 = self.stream.read(1)
            byte_3 = self.stream.read(1)
            if not byte_1 or not byte_2:
                break

            int_8_1 = int.from_bytes(byte_1, byteorder="little")
            int_8_2 = int.from_bytes(byte_2, byteorder="little")
            int_8_3 = int.from_bytes(byte_3, byteorder="little")
            if not byte_3:
                int_1 = int8_to_int12(int_8_1, int_8_2)
                yield int_1
                continue

            int_1, int_2 = int8_to_int12(int_8_1, int_8_2, int_8_3)
            yield int_1
            yield int_2


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
    byte_2 = 0xff & byte_2_start
    if second is None:
        return byte_1, byte_2
    byte_2 |= second >> 8
    byte_3 = 0xff & second

    return byte_1, byte_2, byte_3


def int8_to_int12(first, second, third=None):
    """Convert three or two bytes to 12-bit integers."""
    if first > 256 or second > 256:
        raise Exception("More than 8 bits")
    elif third is not None and third > 256:
        raise Exception("Third more than 8 bits")

    byte_1_end = second >> 4
    byte_1 = first << 4 | byte_1_end
    if third is None:
        return byte_1
    byte_2_start = 0xf & second
    byte_2 = byte_2_start << 8 | third

    return byte_1, byte_2
