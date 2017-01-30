#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Main class for comparison of compression techniques"""

import io
from bitstring import BitStream

import lzw


def compress(file_input):
    """Compress a file using LZW compression algorithm.
    :param file_input:
    :return: compressed output
    """
    with open(file_input) as in_stream:
        lzw_compr = lzw.Lzw(in_stream)
        lzw_compr.compress()


def compress_str(string_input):
    """Compress string, print output
    :param string_input: string for compression.
    """
    with io.StringIO(string_input) as in_stream:
        lzw_compressor = lzw.Lzw(in_stream)
        with open("output.lzw", "wb") as out_stream:
            for byte in lzw_compressor.compress():
                out_stream.write(byte.to_bytes(1, byteorder="little"))
            print("Compressed file written")


def uncompress(file_name):
    """Uncompress an lzw-compressed file, and print the output.
    :param file_name: file name for uncompression.
    """
    in_stream = BitStream(filename=file_name)
    lzwer = lzw.Lzw(in_stream)
    for char in lzwer.uncompress():
        print(char, end="")
    print("")


def main():
    """Main function. String is compressed and uncompressed."""
    test_str = "banana bandana " * 2

    print(test_str)
    print("Disk usage before: {} bytes".format(len(test_str)))
    compress_str(test_str)
    uncompress("output.lzw")


if __name__ == "__main__":
    main()
