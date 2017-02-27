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
    if not chunk:
        yield b"\x03\x02"
    while chunk:
        chunk = b"\x02" + chunk + b"\x03"
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
    for index, _ in enumerate(string):
        start = string[index:]
        end = string[:index]
        table.append(start + end)
    return sorted(table)


def bwt_decode(text_input):
    """Decode bwt-rearranged text."""
    table = [b""] * len(text_input)
    for rotation, j in enumerate(text_input):
        column = []
        for i, a in enumerate(text_input):
            column.insert(0, bytes([text_input[i]]) + table[i])

        table = sorted(column)

    decoded_row = find_decoded(table)
    return decoded_row.rstrip(b"\x03").strip(b"\x02")


def find_decoded(table):
    """Look for row which ends to "end of text" (ETX) control character.
    :param table: table of strings, where one should end with ETX control
    character.
    :return: decoded string.
    """
    for row in table:
        if row.endswith(b"\x03"):
            return row
    raise Exception("No ETX character-ending row in table.")


def rle_encode(stream):
    """Use run length encoding on a byte string."""
    output = b""
    streak = 1
    try:
        prev = next(stream)
    except StopIteration:
        return b""
    while True:
        try:
            char = next(stream)
        except StopIteration:
            break
        if char == prev and streak < 255:
            streak += 1
        else:
            output += prev + bytes([streak])
            streak = 1
        prev = char

    output += prev + bytes([streak])
    return output


def rle_decode(stream):
    """Decode run-length encoded byte stream."""
    while True:
        byte = stream.read(1)
        if not byte:
            break
        count = int.from_bytes(stream.read(1), byteorder="little")
        for i in range(count):
            yield byte
