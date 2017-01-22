#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Main class for comparison of compression techniques"""

import io
import lzw


def compress(file_input):
    """Compress a file using LZW compression algorithm.
    :param file_input:
    :return: compressed output
    """
    with open(file_input) as stream:
        lzw_compr = lzw.Lzw(stream)
        lzw_compr.compress()


def compress_str(string_input):
    """Compress string, print output
    :param string_input: string for compression.
    """
    with io.StringIO(string_input) as stream:
        lzw_compressor = lzw.Lzw(stream)
        lzw_compressor.compress()
        lzw_compressor.print_dictionary()


def main():
    """Main function. String 'banana bandana' is compressed."""
    test_str = "banana bandana"

    print("Text to be compressed: [{}]".format(test_str))
    compress_str(test_str)


if __name__ == "__main__":
    main()
