#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Sorting for burrows-wheeler transform."""


def counting_sorted(in_arr, max_value):
    """Sort an array of integers which all are fairly close to each other.
    :param in_arr: Array for sorting.
    :param max_value: exclusive upper bound for values in the array.
    :return: sorted array.
    """
    counts = [0] * max_value
    for num in in_arr:
        counts[num] += 1
    sorted_arr = [None] * len(in_arr)
    index = 0
    for number in range(max_value):
        for j in range(counts[number]):
            sorted_arr[index] = number
            index += 1

    if isinstance(in_arr, bytes):
        return bytes(sorted_arr)

    return sorted_arr


def merge_sort(array):
    """Sort an array using merge sort. Array is sorted in-place.
    :param array: input array for sorting.
    """
    length = len(array)
    temp = [None] * length
    width = 1
    while width < length:
        left = 0
        while left < length:
            merge(array, left, min(left + width, length),
                  min(left + 2 * width, length), temp)
            left += 2 * width
        width *= 2
        for left, _ in enumerate(temp):
            array[left] = temp[left]


def merge(arr, left, mid, right, temp_arr):
    """Merge two arrays.
    :param arr: input array.
    :param left: left bound for first half.
    :param mid: right bound for first half, left bound for second half.
    :param right: right bound for second half.
    :param temp_arr: working array for the output.
    """
    l = left
    r = mid

    for i in range(left, right):
        if l < mid and (r >= right or arr[l] <= arr[r]):
            temp_arr[i] = arr[l]
            l += 1
        else:
            temp_arr[i] = arr[r]
            r += 1
