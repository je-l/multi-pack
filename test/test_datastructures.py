#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Tests for data structures."""

import unittest
from multipack.datastructures import Node, LinkedList, HashTable, DynamicArray


class TestDatastructures(unittest.TestCase):

    def test_node_creation(self):
        node = Node(1, 2)
        self.assertEqual(2, node.data)

    def test_node_comparison_1(self):
        node_1 = Node(1, 1)
        node_2 = Node(2, 2)
        node_3 = Node(3, 3)
        node_4 = Node(4, 4)
        node_5 = Node(5, 5)
        node_5_2 = Node(5, 5)
        self.assertTrue(node_1 < node_2)
        self.assertEqual(node_5, node_5_2)
        self.assertTrue(node_4 > node_3)

    def test_linked_list_creation(self):
        linked_list = LinkedList()
        self.assertIsNone(linked_list.first)

    def test_linked_list_(self):
        linked_list = LinkedList()
        self.assertIsNone(linked_list.first)

    def test_linked_list_add_last(self):
        linked_list = LinkedList()
        linked_list.add_last("k", 1)
        linked_list.add_last("o", 2)

        self.assertEqual(1, linked_list.first.data)

    def test_linked_list_small(self):
        linked_list = LinkedList()
        for i in range(1, 5):
            linked_list.add_first(i, i)
        total = 0
        node = linked_list.first
        while node is not None:
            total += node.data
            node = node.next

        self.assertEqual(10, total)

    def test_hash_table_length_same_keys(self):
        hash_table = HashTable()
        for i in range(3):
            hash_table["nice"] = 7

        self.assertEqual(1, len(hash_table))

    def test_hash_table_one_key_length(self):
        hash_table = HashTable()
        hash_table[2] = "k"
        self.assertEqual(1, len(hash_table))

    def test_hash_table_full_length(self):
        hash_table = HashTable()
        for i in range(4096):
            hash_table[i] = i
        self.assertEqual(4096, len(hash_table))

    def test_hash_table_same_key_value_does_change(self):
        hash_table = HashTable()
        hash_table["ab"] = 3
        hash_table["ab"] = 33
        self.assertEqual(33, hash_table["ab"])

    def test_missing_key_raises_key_error(self):
        hash_table = HashTable()

        with self.assertRaises(KeyError):
            k = hash_table["k"]

    def test_hash_table_contains(self):
        hash_table = HashTable()
        hash_table["a"] = 2
        self.assertTrue("a" in hash_table)

    def test_hash_table_contains_missing(self):
        hash_table = HashTable()
        hash_table["a"] = 2
        self.assertFalse("b" in hash_table)

    def test_hash_table_contains_complex(self):
        hash_table = HashTable()
        emoji_string = "$affs🐲d"
        hash_table[emoji_string] = -1
        self.assertTrue(emoji_string in hash_table)

    def test_dyn_array_short(self):
        dyn_arr = DynamicArray()
        dyn_arr.append(2)
        self.assertEqual(2, dyn_arr[0])

    def test_dyn_array_medium(self):
        dyn_arr = DynamicArray()
        for i in range(30):
            dyn_arr.append(i)
        self.assertEqual(29, dyn_arr[29])

    def test_dyn_array_len(self):
        dyn_arr = DynamicArray()
        self.assertEqual(0, len(dyn_arr))

    def test_dyn_array_len_2(self):
        dyn_arr = DynamicArray()
        for i in range(33):
            dyn_arr.append("k")
        self.assertEqual(33, len(dyn_arr))
