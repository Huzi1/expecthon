#!/usr/bin/env python3
import unittest

from expecthon import expect, that, that_list, that_number


class ListExampleTestCase(unittest.TestCase):
    def test_value_is_positive(self):
        def value_that_is_positive(value):
            is_int = that(value).is_instance_of(int)
            if is_int:
                return that_number(value).is_positive()
            else:
                return is_int

        expect(that_list([0, "1", 1]).has_any(value_that_is_positive))

    def test_value_is_positive_simple(self):
        def value_that_is_positive(value):
            return that_number(value).is_positive()

        expect(that_list([-1, -2, 1, -3]).has_any(value_that_is_positive))
