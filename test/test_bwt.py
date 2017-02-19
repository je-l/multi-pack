#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Test for burrows-wheeler transform."""

import unittest

from multipack.bwt import *


class TestBwt(unittest.TestCase):

    def test_transformed_len(self):
        with open("LICENSE") as f:
            length = len([i for i in bwt_encode(f)])
            self.assertEqual(1065, length)

    def test_create_table_empty(self):
        table = create_table("")
        self.assertEqual([], table)

    def test_create_table_short(self):
        table = create_table("a")
        self.assertEqual(["a"], table)

    def test_create_table_short_2(self):
        table = create_table("abcde")
        self.assertEqual(["abcde", "bcdea", "cdeab", "deabc", "eabcd"], table)

    def test_find_etx(self):
        table = ["fo\003o", "bar\003"]
        self.assertEqual("bar\003", find_decoded(table))
