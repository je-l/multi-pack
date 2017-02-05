#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Data structures."""


class Linkedlist:
    """Linked list implementation."""

    def __init__(self):
        self.first = None

    def add(self):
        """Add new node to this linked list."""
        pass

    class Node:
        """Node in linked list."""

        def __init__(self, data):
            self.data = data
            self.next = None
