#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""BWT encoding and decoding for strings."""

CHUNK_SIZE = 10000


def bwt_encode(stream):
    """Rearrange a string into more easily compressable string."""
    chunk = stream.read(CHUNK_SIZE)
    while chunk:
        chunk = "\002" + chunk + "\003"
        table = create_table(chunk)
        for rotation in table:
            yield rotation[-1:]
        chunk = stream.read(CHUNK_SIZE)


def create_table(string):
    """Create the table of different rotations.
    :return: Sorted list of rotations."""
    table = []
    for index in range(len(string)):
        start = string[index:]
        end = string[:index]
        table.append(start + end)
    return sorted(table, key=str.upper)


def bwt_decode(code):
    """Decode """
    pass
