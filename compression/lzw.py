#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Lempel–Ziv–Welch compression algorithm example, with small dictionary."""


class Lzw:
    """Lempel-Ziv-Welch compression example. Compresses 14 byte string to
    10 byte string."""

    def __init__(self, stream):
        self.stream = stream
        self.dictionary = {}
        self.index = 0
        self.str = ""
        self.init_dict()

    def dict_add(self, dict_string):
        """Add new string to dictionary. Key is a string and value is
        integer.
        :param dict_string: new string for the dictionary.
        """
        self.dictionary[dict_string] = self.index
        self.index += 1

    def init_dict(self):
        """Initialize the dictionary with few letters. Normally this would
        be all extended ASCII letters (0-255).
        """
        self.dict_add("a")
        self.dict_add("b")
        self.dict_add("d")
        self.dict_add("n")
        self.dict_add(" ")

    def print_dictionary(self):
        """Print dictionary pairs for debugging."""
        print("Dictionary:")
        for i in sorted(self.dictionary, key=self.dictionary.get):
            print("{:>2}=[{}]".format(self.dictionary[i], i))

    def compress(self):
        """Compress the string using the dictionary.
        :return an iterable of dictionary keys."""
        print("Encoded output: ", end="")
        char = self.stream.read(1)
        while len(char) > 0:
            if self.str + char in self.dictionary:
                self.str = self.str + char
            else:
                print(str(self.dictionary[self.str]) + ",", end="")
                self.dict_add(self.str + char)
                self.str = char
            char = self.stream.read(1)
        print(str(self.dictionary[self.str]))
        return self.dictionary.values()


def ints_to_bytes(first, second):
    """Convert two 12-bit integers to three bytes."""
    if first > 4095 or second > 4095:
        raise Exception("Index more than 12 bits")
    byte_1 = first >> 4
    byte_2_start = first << 4
    byte_2 = shift_mask(byte_2_start)
    byte_2 |= second >> 8
    byte_3 = shift_mask(second)

    return byte_1, byte_2, byte_3


def shift_mask(binary):
    """Drop bits from the left until 8 bits are left."""
    if binary.bit_length() < 9:
        return binary
    return 0xff & binary
