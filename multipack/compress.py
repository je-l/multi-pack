#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Main module for compression and command line arguments."""

import os
from os.path import isfile
import time
import argparse

from multipack.lzw import Lzw
from multipack.bwt import bwt_encode, bwt_decode, rle_encode, rle_decode


def lzw_compress(filename):
    """Compress text stream.
    :param filename: File name for the compression.
    """
    with open(filename, "rb") as in_stream:
        lzw_compressor = Lzw(in_stream)
        with open(filename + ".lzw", "wb") as out_stream:
            for index in lzw_compressor.compress():
                out_stream.write(bytes([index]))
            if ARGS.verbose:
                print("Final dict size:", len(lzw_compressor.dictionary))
    os.remove(filename)


def lzw_uncompress(file_name):
    """Uncompress an lzw-compressed file, and print the output.
    :param file_name: file name for uncompression.
    """
    with open(file_name, "rb") as in_stream:
        lzwer = Lzw(in_stream)
        with open(file_name[:-4], "wb") as out_file:
            for byte in lzwer.uncompress():
                out_file.write(byte)
    os.remove(file_name)


def bwt_compress(filename):
    """Compress with btw."""
    with open(filename, "rb") as in_stream:
        with open(filename + ".bwt", "wb") as out_stream:
            bwt_encoded = bwt_encode(in_stream)
            rle_encoded = rle_encode(bwt_encoded)
            out_stream.write(rle_encoded)
    os.remove(filename)


def bwt_uncompress(filename):
    """Uncompress with bwt."""
    with open(filename, "rb") as in_stream:
        with open(filename[:-4], "wb") as out_stream:
            for chunk in bwt_decode(rle_decode(in_stream)):
                out_stream.write(chunk)
    os.remove(filename)


def main():
    """Main function. First argument is the file for compression."""
    start_ts = time.time()
    if not isfile(ARGS.filename):
        print('No file "{}" found'.format(ARGS.filename))
        return
    file_end = ARGS.filename[-4:]
    if (file_end == ".lzw" and ARGS.lzw) or (file_end == ".bwt" and ARGS.bwt):
        cli_uncompress()
    else:
        cli_compress()

    if ARGS.verbose:
        elapsed = time.time() - start_ts
        print("Complete in {:.0f} ms".format(elapsed * 1000))


def cli_compress():
    """Compress file with either LZW or BWT techniques."""
    original_size = os.stat(ARGS.filename).st_size
    if ARGS.verbose:
        print("Original size: {:.1f} KB".format(original_size / 1024))
    if ARGS.lzw:
        lzw_compress(ARGS.filename)
    elif ARGS.bwt:
        bwt_compress(ARGS.filename)
    if ARGS.lzw:
        min_size = os.stat(ARGS.filename + ".lzw").st_size
    else:
        min_size = os.stat(ARGS.filename + ".bwt").st_size
    if ARGS.verbose:
        print("output size: {:.1f} KB".format(min_size / 1024))

    ratio = original_size / min_size
    percentage = min_size / original_size * 100
    if ARGS.verbose:
        print("Compression ratio: {:.2f} ({:.1f}%)".format(ratio, percentage))


def cli_uncompress():
    """Uncompress."""
    if ARGS.lzw:
        lzw_uncompress(ARGS.filename)
    elif ARGS.bwt:
        bwt_uncompress(ARGS.filename)


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
