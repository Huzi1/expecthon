#!/usr/bin/env python3
"""
Test the base assumption class

These are all written by creating simple tests that should succeed or fail
and then running them.
"""

import unittest

from expecthon import (
    case,
    expect,
    negative_test,
    set_of,
    success,
    that,
    that_assumption,
    that_dict,
    that_function,
    that_list,
    that_number,
    that_result,
    that_string,
)

from .helpers import failed


class BaseAssumptionAssumptionTestCase(unittest.TestCase):
    def test_fails__positive_test(self):
        failing_assumption = that(True).is_false
        expect(that_assumption(failing_assumption).fails())

    def test_fails__negative_test(self):
        with negative_test():
            succeeding_assumption = that(False).is_false
            expect(that_assumption(succeeding_assumption).fails())

    def test_and_operator_assumption_and_result__negative_test(self):
        with negative_test():
            expect(that(True).is_true() & failed())

    def test_and_operator_assumption_and_result__positive_test(self):
        expect(that(True).is_true() & success())

    def test_and_operator_result_and_assumption__negative_test(self):
        with negative_test():
            expect(failed() & that(True).is_true())

    def test_and_operator_result_and_assumption__positive_test(self):
        expect(success() & that(True).is_true())

    def test_and_operator_assumption_and_none__negative_test(self):
        with negative_test():
            expect(that(False).is_true() & None)

    def test_and_operator_assumption_and_none__positive_test(self):
        expect(that(True).is_true() & None)

    def test_and_operator_none_and_assumption__negative_test(self):
        with negative_test():
            expect(None & that(False).is_true())

    def test_and_operator_none_and_assumption__positive_test(self):
        expect(None & that(True).is_true())

    def test_can_chain_results(self):
        expect(that(True).is_true().equals(True))

    def test_can_chain_results__negative_test(self):
        with case("first link fails"):
            with negative_test():
                expect(that(True).is_false().equals(True))
        with case("second link fails"):
            with negative_test():
                expect(that(True).is_true().equals(False))
        with case("both link fails"):
            with negative_test():
                expect(that(True).is_false().equals(False))
