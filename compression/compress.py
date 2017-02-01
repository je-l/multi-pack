#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Main class for comparison of compression techniques"""

import io
import sys
from bitstring import BitStream

import lzw


def compress(file_input):
    """Compress a file using LZW compression algorithm.
    :param file_input:
    :return: compressed output
    """
    with open(file_input) as in_stream:
        compress_stream(in_stream)


def compress_stream(in_stream):
    """Compress text stream.
    :param in_stream: text stream for compression.
    """
    lzw_compressor = lzw.Lzw(in_stream)
    with open("output.lzw", "wb") as out_stream:
        for index in lzw_compressor.compress():
            out_stream.write(index.to_bytes(1, byteorder="little"))
        print("Compressed file written")
        print("Final dict size:", len(lzw_compressor.dictionary))


def compress_str(string_input):
    """Compress string, print output
    :param string_input: string for compression.
    """
    with io.StringIO(string_input) as in_stream:
        compress_stream(in_stream)


def uncompress(file_name):
    """Uncompress an lzw-compressed file, and print the output.
    :param file_name: file name for uncompression.
    """
    in_stream = BitStream(filename=file_name)
    lzwer = lzw.Lzw(in_stream)
    with open("output", "w") as out_file:
        for char in lzwer.uncompress():
            out_file.write(char)


def main():
    """Main function. If an argument is given, a file is compressed,
    otherwise a test string is compressed.
    """
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        print("Compressing file:", filename)
        compress(sys.argv[1])
    else:
        test_str = "banana bandana " * 2

        print(test_str)
        print("Disk usage before: {} bytes".format(len(test_str)))
        compress_str(test_str)
    uncompress("output.lzw")


if __name__ == "__main__":
    main()
