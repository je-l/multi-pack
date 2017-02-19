#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Main module for comparison of compression techniques"""

import os
import time
import argparse

from multipack.lzw import Lzw
from multipack.bwt import *


def lzw_compress(file_input):
    """Compress a file using LZW compression algorithm.
    :param file_input:
    :return: compressed output
    """
    with open(file_input, "rb") as in_stream:
        lzw_compress_stream(in_stream)


def lzw_compress_stream(in_stream):
    """Compress text stream.
    :param in_stream: text stream for compression.
    """
    lzw_compressor = Lzw(in_stream)
    with open("output.lzw", "wb") as out_stream:
        for index in lzw_compressor.compress():
            out_stream.write(bytes([index]))
        print("Compressed file written")
        print("Final dict size:", len(lzw_compressor.dictionary))


def lzw_uncompress(file_name):
    """Uncompress an lzw-compressed file, and print the output.
    :param file_name: file name for uncompression.
    """
    with open(file_name, "rb") as in_stream:
        lzwer = Lzw(in_stream)
        with open("output", "wb") as out_file:
            for byte in lzwer.uncompress():
                out_file.write(byte)


def bwt_compress(filename):
    """Compress with btw."""
    with open(filename) as in_stream:
        with open("output.bwt", "w") as out_stream:
            for chunk in bwt_encode(in_stream):
                out_stream.write(chunk)


def bwt_uncompress(filename):
    """Uncompress with bwt."""
    with open(filename) as in_file:
        with open("output", "w") as out_file:
            for chunk in bwt_decode(in_file):
                out_file.write(chunk)


def main():
    """Main function. First argument is the file for compression."""
    args = init_args()
    start_ts = time.time()
    original_size = os.stat(args.filename).st_size
    print("Original size: {:.1f} KB".format(original_size / 1024))
    print("Compressing file:", args.filename)
    if args.lzw:
        lzw_compress(args.filename)
    elif args.bwt:
        bwt_compress(args.filename)
    compress_complete_ts = time.time()
    elapsed = compress_complete_ts - start_ts
    print("Compress complete in {:.0f} ms".format(elapsed * 1000))

    if args.lzw:
        lzw_uncompress("output.lzw")
    elif args.bwt:
        bwt_uncompress("output.bwt")
    elapsed = time.time() - compress_complete_ts
    print("Uncompress complete in {:.0f} ms".format(elapsed * 1000))
    min_size = os.stat("output.bwt").st_size
    print("output size: {:.1f} KB".format(min_size / 1024))

    ratio = original_size / 0.1 if min_size == 0 else min_size
    percentage = min_size / original_size * 100
    print("Compression ratio: {:.2f} ({:.1f}%)".format(ratio, percentage))
    print("Total time: {:.0f} ms".format((time.time() - start_ts) * 1000))


def init_args():
    """Create command line parameters and return the parsed input."""
    arg = argparse.ArgumentParser(description="Compress and uncompress files "
                                              "with LZW and BWT algorithms.")
    algo_choice = arg.add_mutually_exclusive_group(required=True)
    arg.add_argument("filename",
                     metavar="FILE",
                     help="Filename for the target file.")
    algo_choice.add_argument("--lzw",
                             help="Use Lempel-Ziv-Welch compression technique.",
                             action="store_true")
    algo_choice.add_argument("--bwt",
                             help="Use Burrows-Wheeler transform technique.",
                             action="store_true")
    args = arg.parse_args()
    return args


if __name__ == "__main__":
    main()
