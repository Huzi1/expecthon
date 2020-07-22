#!/usr/bin/env python3
"""
Tests the core classes for the underlying system
"""
import unittest

from expecthon import expect, case

from .assumptions import empty, failed, that_result


class AssumptionResultTestCase(unittest.TestCase):
    """
    Test all operations on the AssumptionResult class
    """

    def test_empty(self):
        """
        Test the `AssumptionResult.empty()` function
        """
        expect(that_result(empty()).is_successful())

    def test_and(self):
        """
        Test the bitwise `&` operator which concats two results
        """

        with case("Both successful"):
            expect(that_result(empty() & empty()).is_successful())

        with case("first fail, second succeed"):
            expect(that_result(failed() & empty()).has_failure_count_of(1))

        with case("first succeed, second fail"):
            expect(that_result(empty() & failed()).has_failure_count_of(1))

        with case("two fail"):
            expect(that_result(failed() & failed()).has_failure_count_of(2))

    def test_and_chaining(self):
        """
        checking associative law `(A & B) & C` == `A & (B & C)`
        """
        with case("combined first"):
            result = (failed() & failed()) & failed()
            expect(that_result(result).has_failure_count_of(3))

        with case("combined last"):
            result = failed() & (failed() & failed())
            expect(that_result(result).has_failure_count_of(3))
