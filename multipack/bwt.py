#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""BWT compression using run-length encoding."""

from multipack.sorting import counting_sorted, merge_sort

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
        table = _create_table(chunk)
        for rotation in table:
            yield rotation[-1:]
        chunk = stream.read(CHUNK_SIZE)


def _create_table(string):
    """Create the table of different rotations.
    :param string: base for the different rotations.
    :return: Sorted list of rotations. There is len(string) different rotations
    altogether.
    """
    table = [None] * len(string)
    for index, _ in enumerate(string):
        start = string[index:]
        end = string[:index]
        table[-index] = (start + end)
    merge_sort(table)
    return table


def bwt_decode(enc_input):
    """Decode bwt-rearranged byte generator.
    :param enc_input: byte generator of encoded BWT data.
    :return: byte generator of decoded data. The yielded chunks are very large.
    """
    input_chunk = _read_chunk(enc_input)

    while input_chunk:
        input_length = len(input_chunk)
        byte_start, indices = _create_indices(input_chunk)
        local_index = input_chunk.index(b"\x03")
        output = [b""] * input_length
        for i in range(input_length):
            next_byte = input_chunk[local_index]
            output[input_length - i - 1] = next_byte
            local_index = byte_start[next_byte] + indices[local_index]
        yield bytes(output).rstrip(b"\x03").strip(b"\x02")
        input_chunk = _read_chunk(enc_input)


def _read_chunk(source):
    """Read chunk of data from generator and return it.
    :param source: source generator for the bytes.
    :return: chunk of bwt encoded data.
    """
    next_bytes = b""
    for byte in range(CHUNK_SIZE + 2):
        try:
            next_bytes += next(source)
        except StopIteration:
            break
    return next_bytes


def _create_indices(bwt_input):
    """Generate indices helper list for BWT uncompression.
    :param bwt_input: byte string input.
    :return: indice lists for the uncompression.
    """
    input_length = len(bwt_input)
    byte_start = [None] * 256
    indices = [None] * input_length

    first_column = counting_sorted(bwt_input, 256)
    count = [0] * 256
    for byte in range(input_length):
        index = bwt_input[byte]
        indices[byte] = count[index]
        count[index] += 1
        index = first_column[byte]
        if byte_start[index] is None:
            byte_start[index] = byte

    return byte_start, indices


def _find_decoded(table):
    """Look for row which ends to "end of text" (ETX) control character.
    :param table: table of strings, where one should end with ETX control
    character.
    :return: decoded string.
    """
    for row in table:
        if row.endswith(b"\x03"):
            return row
    raise Exception("No ETX character-ending row in table.")


def rle_encode(byte_arr):
    """Use run length encoding on a byte string.
    :param byte_arr: byte generator.
    :return: byte string of encoded data.
    """
    output = b""
    streak = 1
    try:
        prev = next(byte_arr)
    except StopIteration:
        return b""
    while True:
        try:
            char = next(byte_arr)
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
    """Decode run-length encoded byte stream.
    :param stream: byte stream for the encoding.
    :return: byte-generator, which returns one byte at a time.
    """
    while True:
        byte = stream.read(1)
        if not byte:
            break
        count = int.from_bytes(stream.read(1), byteorder="little")
        for i in range(count):
            yield byte
