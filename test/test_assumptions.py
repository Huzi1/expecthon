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

    def test_equals_negative_test(self):
        with negative_test():
            expect(that(1 + 1).equals(3))

    def test_doesnt_equals(self):
        for i in set_of.integers():
            expect(that(i + 1).doesnt_equals(i))

    def test_doesnt_equals_negative_test(self):
        with negative_test():
            expect(that(1 + 1).doesnt_equals(2))

    def test_is(self):
        for i in set_of.anything():
            expect(that(i).is_(i))

    def test_is_negative_test(self):
        with negative_test():
            # as lists are pass by reference
            expect(that([1]).is_([1]))

    def test_is_not(self):
        # as lists are pass by reference
        expect(that([1]).is_not([1]))

    def test_is_not_negative_test(self):
        with negative_test():
            expect(that(1).is_not(1))

    def test_is_type(self):
        for i in set_of.integers():
            expect(that(i).is_type(int))

    def test_is_type_negative_test(self):
        with negative_test():
            expect(that("5").is_type(int))

    def test_is_true(self):
        expect(that(True).is_true())

    def test_is_true_negative_test(self):
        with negative_test():
            expect(that(False).is_true())

    def test_is_false(self):
        expect(that(False).is_false())

    def test_is_false_negative_test(self):
        with negative_test():
            expect(that(True).is_false())


class StringAssumptionTestCase(unittest.TestCase):
    """
    Tests regarding the `StringAssumption` `that_string`
    """

    def test_contains(self):
        expect(that_string("test").contains("te"))

    def test_contains_negative_test(self):
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

    def test_is_empty_negative_test(self):
        with negative_test():
            expect(that_list([1]).is_empty())

    def test_is_not_empty(self):
        expect(that_list([1]).is_not_empty())

    def test_is_not_empty_negative_test(self):
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

    def test_contains_negative_test(self):
        with negative_test():
            expect(that_list([1, 2, 3]).contains(5))

    def test_has_any(self):
        expect(that_list([1, 2, 3]).has_any(lambda v: that(v).equals(2)))

    def test_has_any_negative_test(self):
        with negative_test():
            expect(that_list([1, 2, 3]).has_any(lambda v: that(v).equals(4)))


class BaseAssumptionAssumptionTestCase(unittest.TestCase):
    def test_fails(self):
        with case("positive test"):
            failing_assumption = that(True).is_false
            expect(
                that_assumption(that_assumption(failing_assumption).fails).succeeds()
            )
        with case("negative test"):
            succeeding_assumption = that(False).is_false
            expect(
                that_assumption(that_assumption(succeeding_assumption).fails).fails()
            )

    def test_succeeds(self):
        with case("positive test"):
            failing_assumption = that(False).is_false
            expect(
                that_assumption(that_assumption(failing_assumption).succeeds).succeeds()
            )
        with case("negative test"):
            succeeding_assumption = that(True).is_false
            expect(
                that_assumption(that_assumption(succeeding_assumption).succeeds).fails()
            )

    def test_and_operator(self):
        with case("Assumption and result"):
            with case("Should fail"):
                expect(that_result(that(True).is_true() & failed()).is_not_successful())
            with case("Should succeed"):
                expect(that_result(that(True).is_true() & success()).is_successful())

        with case("result and assumption"):
            with case("Should fail"):
                expect(that_result(failed() & that(True).is_true()).is_not_successful())
            with case("Should succeed"):
                expect(that_result(success() & that(True).is_true()).is_successful())
        with case("assumption and None"):
            with case("Should fail"):
                expect(that_result(that(False).is_true() & None).is_not_successful())
            with case("Should succeed"):
                expect(that_result(that(True).is_true() & None).is_successful())
