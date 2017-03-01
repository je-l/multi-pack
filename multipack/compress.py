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
        if ARGS.verbose:
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
    with open(filename, "rb") as in_stream:
        with open("output.bwt", "wb") as out_stream:
            bwt_encoded = bwt_encode(in_stream)
            rle_encoded = rle_encode(bwt_encoded)
            out_stream.write(rle_encoded)


def bwt_uncompress(filename):
    """Uncompress with bwt."""
    with open(filename, "rb") as in_stream:
        with open("output", "wb") as out_stream:
            for chunk in bwt_decode(rle_decode(in_stream)):
                out_stream.write(chunk)


def main():
    """Main function. First argument is the file for compression."""
    start_ts = time.time()
    original_size = os.stat(ARGS.filename).st_size
    if ARGS.verbose:
        print("Original size: {:.1f} KB".format(original_size / 1024))
    if ARGS.lzw:
        lzw_compress(ARGS.filename)
    elif ARGS.bwt:
        bwt_compress(ARGS.filename)
    compress_complete_ts = time.time()
    elapsed = compress_complete_ts - start_ts
    if ARGS.verbose:
        print("Compress complete in {:.0f} ms".format(elapsed * 1000))

    if ARGS.lzw:
        lzw_uncompress("output.lzw")
    elif ARGS.bwt:
        bwt_uncompress("output.bwt")
    elapsed = time.time() - compress_complete_ts
    if ARGS.verbose:
        print("Uncompress complete in {:.0f} ms".format(elapsed * 1000))
    if ARGS.lzw:
        min_size = os.stat("output.lzw").st_size
    else:
        min_size = os.stat("output.bwt").st_size
    if ARGS.verbose:
        print("output size: {:.1f} KB".format(min_size / 1024))

    ratio = original_size / (0.1 if min_size == 0 else min_size)
    percentage = min_size / original_size * 100
    if ARGS.verbose:
        print("Compression ratio: {:.2f} ({:.1f}%)".format(ratio, percentage))
        print("Total time: {:.0f} ms".format((time.time() - start_ts) * 1000))


def init_args():
    """Create command line parameters and return the parsed input."""
    arg = argparse.ArgumentParser(description="Compress and uncompress files "
                                              "with LZW or BWT technique.")
    arg.add_argument("-v", "--verbose", help="be verbose", action="store_true")
    algo_choice = arg.add_mutually_exclusive_group(required=True)
    arg.add_argument("filename",
                     metavar="FILE",
                     help="filename for the target file")
    algo_choice.add_argument("--lzw",
                             help="use Lempel-Ziv-Welch compression technique",
                             action="store_true")
    algo_choice.add_argument("--bwt",
                             help="use Burrows-Wheeler transform technique",
                             action="store_true")
    return arg.parse_args()


ARGS = init_args()
