#!/usr/bin/env python
# -*- coding: utf8 -*-

import datetime

try:
    from cdecimal import Decimal
except ImportError: #pragma: no cover
    from decimal import Decimal

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from agate import Table
from agate.data_types import *
from agate.exceptions import *

class TestColumns(unittest.TestCase):
    def setUp(self):
        self.rows = (
            (1, 2, 'a'),
            (2, 3, 'b'),
            (None, 4, 'c')
        )

        self.number_type = Number()
        self.text_type = Text()

        self.columns = (
            ('one', self.number_type),
            ('two', self.number_type),
            ('three', self.text_type)
        )

        self.table = Table(self.rows, self.columns)

    def test_stringify(self):
        self.assertEqual(str(self.table.columns['one']), "<agate.Column: (Decimal('1'), Decimal('2'), None)>")

    def test_stringify_long(self):
        rows = (
            (1, 2, 'a'),
            (2, 3, 'b'),
            (None, 4, 'c'),
            (1, 2, 'a'),
            (2, 3, 'b'),
            (None, 4, 'c')
        )

        self.table = Table(rows, self.columns)

        self.assertEqual(str(self.table.columns['one']), "<agate.Column: (Decimal('1'), Decimal('2'), None, Decimal('1'), Decimal('2'), ...)>")

    def test_repr(self):
        self.table = Table(self.rows, self.columns)

        self.assertEqual(repr(self.table.columns['one']), "<agate.Column: index=0 name='one' data_type=Number>")

    def test_length(self):
        self.assertEqual(len(self.table.columns), 3)

    def test_get_column_data(self):
        self.assertSequenceEqual(self.table.columns['one'].get_data(), (1, 2, None))

    def test_get_column(self):
        self.assertSequenceEqual(self.table.columns['one'], (1, 2, None))

    def test_get_column_cached(self):
        c = self.table.columns['one']
        c2 = self.table.columns['one']
        c3 = self.table.columns['two']

        self.assertIs(c, c2)
        self.assertIsNot(c2, c3)

    def test_get_invalid_column(self):
        with self.assertRaises(ColumnDoesNotExistError):
            self.table.columns['four']

    def test_column_length(self):
        self.assertEqual(len(self.table.columns['one']), 3)

    def test_get_column_item(self):
        self.assertEqual(self.table.columns['one'][1], 2)

    def test_column_contains(self):
        self.assertEqual(1 in self.table.columns['one'], True)
        self.assertEqual(3 in self.table.columns['one'], False)

    def test_iterate_columns(self):
        it = iter(self.table.columns)

        self.assertSequenceEqual(next(it), (1, 2, None))
        self.assertSequenceEqual(next(it), (2, 3, 4))
        self.assertSequenceEqual(next(it), ('a', 'b', 'c'))

        with self.assertRaises(StopIteration):
            next(it)

    def test_columns_equal(self):
        table2 = Table(self.rows, self.columns)

        self.assertTrue(self.table.columns['one'] == table2.columns['one'])

    def test_columns_not_equal(self):
        table2 = Table(self.rows, self.columns)

        self.assertFalse(self.table.columns['one'] != table2.columns['one'])

    def test_immutable(self):
        with self.assertRaises(TypeError):
            self.table.columns['one'] = 'foo'

        with self.assertRaises(TypeError):
            self.table.columns['one'][0] = 100
