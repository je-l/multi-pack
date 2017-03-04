#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Test for sorting module."""

import unittest

from multipack.sorting import counting_sort


class TestSorting(unittest.TestCase):

    def test_empty_arr(self):
        result = counting_sort([], 1)
        self.assertEqual([], result)

    def test_short_arr(self):
        result = counting_sort([1], 2)
        self.assertEqual([1], result)

    def test_medium_arr(self):
        result = counting_sort([3, 1, 2], 4)
        self.assertEqual([1, 2, 3], result)

    def test_medium_arr2(self):
        arr = [6, 3, 52, 20, 341, 9]
        expected = [3, 6, 9, 20, 52, 341]
        self.assertEqual(expected, counting_sort(arr, 342))

    def test_bytes(self):
        arr = b"\x00\x05\x02\x01"
        expected = b"\x00\x01\x02\x05"
        self.assertEqual(expected, counting_sort(arr, 6))
