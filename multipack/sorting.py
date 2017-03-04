#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Sorting for burrows-wheeler transform."""


def counting_sort(in_arr, max_value):
    """Sort an array of integers which all are fairly close to each other.
    :param in_arr: Array for sorting.
    :param max_value: exclusive upper bound for values in the array.
    :return: sorted array.
    """

    counts = [0] * max_value
    for num in in_arr:
        counts[num] += 1
    sorted_arr = []

    for i in range(max_value):
        for j in range(counts[i]):
            sorted_arr.append(i)

    if isinstance(in_arr, bytes):
        return bytes(sorted_arr)

    return sorted_arr
