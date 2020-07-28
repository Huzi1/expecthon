#!/usr/bin/env python3
"""
Test all `that_*` assumptions

These are all written by creating simple tests that should succeed or fail
and then running them.
"""

from expecthon import expect, case, failed_test, success, assuming, that, that_function
from expecthon.assumption_classes import BaseAssumption
import unittest


class BaseAssumptionTestCase(unittest.TestCase):
    """
    Tests regarding the `BaseAssumption` and `that`
    """

    def test_that_that_returns_correct_type(self):
        expect(that(that(None)).is_type(BaseAssumption))

    def test_equals(self):
        expect(that(5+5).equals(10))

    def test_is_type(self):
        expect(that(5+5).is_type(int))

    def test_is_true(self):
        with case("positive test"):
            expect(that(True).is_true())
        with case("negative test"):
            def expect_that_false_is_true():
                expect(that(False).is_true())

            expect(that_function(expect_that_false_is_true).fails_with(AssertionError))

    def test_is_false(self):
        with case("positive test"):
            expect(that([]).is_false())
        with case("negative test"):
            def expect_that_true_is_false():
                expect(that(True).is_false())

            expect(that_function(expect_that_true_is_false).fails_with(AssertionError))
