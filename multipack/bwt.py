#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""BWT encoding and decoding for strings."""

CHUNK_SIZE = 10000


def bwt_encode(stream):
    """Rearrange a string to more easily compressable string.
    :param stream: input stream for the transform.
    :return: generator for bwt-rearranged string.
    """
    chunk = stream.read(CHUNK_SIZE)
    while chunk:
        chunk = "\002" + chunk + "\003"
        table = create_table(chunk)
        for rotation in table:
            yield rotation[-1:]
        chunk = stream.read(CHUNK_SIZE)


def create_table(string):
    """Create the table of different rotations.
    :param string: base for the different rotations.
    :return: Sorted list of rotations. There is len(string) different rotations
    altogether.
    """
    table = []
    for index in range(len(string)):
        start = string[index:]
        end = string[:index]
        table.append(start + end)
    return sorted(table)


def bwt_decode(stream):
    """Decode bwt-rearranged text."""
    code = stream.read()
    table = [""] * len(code)
    for rotation in range(len(code)):
        column = []
        for i, _ in enumerate(code):
            column.insert(0, code[i] + table[i])
        table = sorted(column)

    print("After len:", len(table))
    decoded_row = find_decoded(table)
    return decoded_row.rstrip("\003").strip("\002")


def find_decoded(table):
    """Look for row which ends to "end of text" (ETX) control character."""
    for row in table:
        if row.endswith("\003"):
            return row
    raise Exception("No ETX character-ending row in table.")
