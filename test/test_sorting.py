#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Test for sorting module."""

import unittest

from multipack.sorting import counting_sorted, merge_sort


class TestSorting(unittest.TestCase):

    def test_empty_arr(self):
        result = counting_sorted([], 1)
        self.assertEqual([], result)

    def test_short_arr(self):
        result = counting_sorted([1], 2)
        self.assertEqual([1], result)

    def test_medium_arr(self):
        result = counting_sorted([3, 1, 2], 4)
        self.assertEqual([1, 2, 3], result)

    def test_medium_arr2(self):
        arr = [6, 3, 52, 20, 341, 9]
        expected = [3, 6, 9, 20, 52, 341]
        self.assertEqual(expected, counting_sorted(arr, 342))

    def test_bytes(self):
        arr = b"\x00\x05\x02\x01"
        expected = b"\x00\x01\x02\x05"
        self.assertEqual(expected, counting_sorted(arr, 6))

    def test_bytes2(self):
        arr = b"a\x00bc\x02"
        expected = b"\x00\x02abc"
        self.assertEqual(expected, counting_sorted(arr, 256))

    def test_merge_empty(self):
        arr = []
        merge_sort(arr)
        self.assertEqual([], arr)

    def test_merge_ints(self):
        arr = [3, 2, 1]
        merge_sort(arr)
        self.assertEqual([1, 2, 3], arr)

    def test_merge_short(self):
        arr = [b"aaa", b"ccc", b"bbb"]
        merge_sort(arr)
        self.assertEqual([b"aaa", b"bbb", b"ccc"], arr)

    def test_merge_short2(self):
        arr = [b"p", b"a", b"k"]
        merge_sort(arr)
        self.assertEqual([b"a", b"k", b"p"], arr)
