#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Main module for comparison of compression techniques"""

import os
import sys
import time

import lzw


def compress(file_input):
    """Compress a file using LZW compression algorithm.
    :param file_input:
    :return: compressed output
    """
    with open(file_input, "rb") as in_stream:
        compress_stream(in_stream)


def compress_stream(in_stream):
    """Compress text stream.
    :param in_stream: text stream for compression.
    """
    lzw_compressor = lzw.Lzw(in_stream)
    with open("output.lzw", "wb") as out_stream:
        for index in lzw_compressor.compress():
            out_stream.write(bytes([index]))
        print("Compressed file written")
        print("Final dict size:", len(lzw_compressor.dictionary))


def uncompress(file_name):
    """Uncompress an lzw-compressed file, and print the output.
    :param file_name: file name for uncompression.
    """
    with open(file_name, "rb") as in_stream:
        lzwer = lzw.Lzw(in_stream)
        with open("output", "wb") as out_file:
            for byte in lzwer.uncompress():
                out_file.write(byte)


def main():
    """Main function. First argument is the file for compression."""
    start_ts = time.time()
    if len(sys.argv) < 2:
        print("Argument missing.")
        return
    filename = sys.argv[1]
    original_size = os.stat(filename).st_size
    print("Original size: {:.1f} KB".format(original_size / 1024))
    print("Compressing file:", filename)
    compress(sys.argv[1])
    compress_complete_ts = time.time()
    elapsed = compress_complete_ts - start_ts
    print("Compress complete in {:.0f} ms".format(elapsed * 1000))
    uncompress("output.lzw")
    elapsed = time.time() - compress_complete_ts
    print("Uncompress complete in {:.0f} ms".format(elapsed * 1000))
    min_size = os.stat("output.lzw").st_size
    print("output size: {:.1f} KB".format(min_size / 1024))
    print("Compression ratio: {:.2f}".format(original_size / min_size))
    print("Total time: {:.0f} ms".format((time.time() - start_ts) * 1000))


if __name__ == "__main__":
    main()
