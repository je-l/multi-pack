#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Data structures."""


class LinkedList:
    """Linked list implementation."""
    def __init__(self):
        self.first = None

    def add_last(self, key, value):
        """Add new node to this linked list."""
        if self.first is None:
            self.first = Node(key, value)
        else:
            temp_last = self.first
            while temp_last.next is not None:
                temp_last = temp_last.next
            temp_last.next = Node(key, value)

    def add_first(self, key, value):
        """Add a new data node to first position in the linked list."""
        new_node = Node(key, value)
        new_node.next = self.first
        self.first = new_node

    def __str__(self):
        string = ""
        node = self.first
        while node is not None:
            string += str(node) + ", "
            node = node.next
        return string


class Node:
    """Node in linked list."""

    def __init__(self, key, value):
        self.key = key
        self.data = value
        self.next = None

    def __str__(self):
        return str(self.data)


class HashTable:
    """Hash table with linked list collision handling.

    Hardcoded for 4096 keys. 6151 is the default table size as it's not close
    to a power of two and it's a prime number.
    """
    def __init__(self, size=6151):
        self.nodes = [None for i in range(size)]
        self.size = 0

    def __setitem__(self, key, value):
        """Add new key-value pair to the hash table."""
        node_hash = self.hash(key)
        if self.nodes[node_hash] is None:
            self.nodes[node_hash] = LinkedList()
            self.nodes[node_hash].add_first(key, value)
        else:
            node = self.nodes[node_hash].first
            while node is not None:
                if node.key == key:
                    node.data = value
                    return
                node = node.next
            self.nodes[node_hash].add_last(key, value)

        self.size += 1

    def __getitem__(self, item):
        """Get value for specified key."""
        hashed = self.hash(item)
        if self.nodes[hashed] is not None:
            node = self.nodes[hashed].first
            while node is not None:
                if node.key == item:
                    return node.data

                node = node.next
        raise KeyError('key "{}" not in hash table.'.format(item))

    def hash(self, key):
        """Remainder hashing function as in course material."""
        hashed = hash(key)
        return hashed % len(self.nodes)

    def __len__(self):
        return self.size

    def __str__(self):
        text = ""
        for i in range(len(self.nodes)):
            if self.nodes[i] is None:
                continue
            text += str(self.nodes[i]) + "\n"
        return text
