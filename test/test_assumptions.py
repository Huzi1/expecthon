#!/usr/bin/env python3
"""
Test all `that_*` assumptions

These are all written by creating simple tests that should succeed or fail
and then running them.
"""

import unittest

from expecthon import (
    case,
    expect,
    set_of,
    success,
    that,
    that_assumption,
    that_list,
    that_number,
    that_result,
    that_string,
    negative_test,
)
from expecthon.assumptions import BaseAssumption

from .helpers import failed


class BaseAssumptionTestCase(unittest.TestCase):
    """
    Tests regarding the `BaseAssumption` and `that`
    """

    def test_that_that_returns_correct_type(self):
        expect(that(that(None)).is_type(BaseAssumption))

    def test_equals(self):
        for i in set_of.integers():
            expect(that(i).equals(i))

    def test_equals__negative_test(self):
        with negative_test():
            expect(that(1 + 1).equals(3))

    def test_doesnt_equals(self):
        for i in set_of.integers():
            expect(that(i + 1).doesnt_equals(i))

    def test_doesnt_equals__negative_test(self):
        with negative_test():
            expect(that(1 + 1).doesnt_equals(2))

    def test_is(self):
        for i in set_of.anything():
            expect(that(i).is_(i))

    def test_is__negative_test(self):
        with negative_test():
            # as lists are pass by reference
            expect(that([1]).is_([1]))

    def test_is_not(self):
        # as lists are pass by reference
        expect(that([1]).is_not([1]))

    def test_is_not__negative_test(self):
        with negative_test():
            expect(that(1).is_not(1))

    def test_is_type(self):
        for i in set_of.integers():
            expect(that(i).is_type(int))

    def test_is_type__negative_test(self):
        with negative_test():
            expect(that("5").is_type(int))

    def test_is_true(self):
        expect(that(True).is_true())

    def test_is_true__negative_test(self):
        with negative_test():
            expect(that(False).is_true())

    def test_is_false(self):
        expect(that(False).is_false())

    def test_is_false__negative_test(self):
        with negative_test():
            expect(that(True).is_false())


class StringAssumptionTestCase(unittest.TestCase):
    """
    Tests regarding the `StringAssumption` `that_string`
    """

    def test_contains(self):
        expect(that_string("test").contains("te"))

    def test_contains__negative_test(self):
        with negative_test():
            expect(that_list("test").contains("ass"))


class NumlberAssumptionTestCase(unittest.TestCase):
    """
    Tests regarding the `DecimalAssumption` `that_number`
    """

    def test_is_positive(self):
        for i in set_of.positive_integers():
            with case(f"positive test (i={i})"):
                expect(that_number(i).is_positive())

    def test_zero_is_not_positive(self):
        with negative_test():
            expect(that_number(0).is_positive())

    def test_less_than_zero_is_not_positive(self):
        for i in set_of.negative_integers():
            with case(f"i={i}"):
                with negative_test():
                    expect(that_number(i).is_positive())


class FunctionAssumptionTestCase(unittest.TestCase):
    ...
    # TODO


class ListAssumptionTestCase(unittest.TestCase):
    """
    Tests regarding the `ListAssumption` `that_list`
    """

    def test_is_empty(self):
        expect(that_list([]).is_empty())

    def test_is_empty__negative_test(self):
        with negative_test():
            expect(that_list([1]).is_empty())

    def test_is_not_empty(self):
        expect(that_list([1]).is_not_empty())

    def test_is_not_empty__negative_test(self):
        with negative_test():
            expect(that_list([]).is_not_empty())

    def test_has_length(self):
        for elements in set_of.lists():
            expect(that_list(elements).has_length(len(elements)))

    def test_has_length_negatiev_test(self):
        with negative_test():
            expect(that_list([1]).has_length(2))

    def test_contains(self):
        expect(that_list([1, 2, 3]).contains(2))

    def test_contains__negative_test(self):
        with negative_test():
            expect(that_list([1, 2, 3]).contains(5))

    def test_has_any(self):
        expect(that_list([1, 2, 3]).has_any(lambda v: that(v).equals(2)))

    def test_has_any__negative_test(self):
        with negative_test():
            expect(that_list([1, 2, 3]).has_any(lambda v: that(v).equals(4)))


class BaseAssumptionAssumptionTestCase(unittest.TestCase):
    def test_fails__positive_test(self):
        failing_assumption = that(True).is_false
        expect(
            that_assumption(failing_assumption).fails()
        )

    def test_fails__negative_test(self):
        with negative_test():
            succeeding_assumption = that(False).is_false
            expect(
                that_assumption(succeeding_assumption).fails()
            )

    def test_succeeds__positive_test(self):
        failing_assumption = that(False).is_false
        expect(
            that_assumption(failing_assumption).succeeds()
        )

    def test_succeeds__negative_test(self):
        with negative_test():
            succeeding_assumption = that(True).is_false
            expect(
                that_assumption(succeeding_assumption).succeeds()
            )

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
