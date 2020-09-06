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
from expecthon.assumptions import BaseAssumption


class BaseAssumptionTestCase(unittest.TestCase):
    """
    Tests regarding the `BaseAssumption` and `that`
    """

    def test_that_that_returns_correct_type(self):
        expect(that(that(None)).is_instance_of(BaseAssumption))

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

    def test_is_instance_of(self):
        for i in set_of.integers():
            expect(that(i).is_instance_of(int))

    def test_is_instance_of__negative_test(self):
        with negative_test():
            expect(that("5").is_instance_of(int))

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

    def test_caseinsensitive_equals(self):
        expect(that_string("test").insensitively().equals("TeSt"))

    def test_caseinsensitive_equals__negative_test(self):
        with negative_test():
            expect(that_string("test").insensitively().equals("TeSt1"))


class NumlberAssumptionTestCase(unittest.TestCase):
    """
    Tests regarding the `DecimalAssumption` `that_number`
    """

    def test_is_positive(self):
        for i in set_of.positive_integers():
            expect(that_number(i).is_positive())

    def test_is_positive__special_case_zero(self):
        with negative_test():
            expect(that_number(0).is_positive())

    def test_is_positive__negative_test(self):
        for i in set_of.negative_integers():
            with negative_test():
                expect(that_number(i).is_positive())

    def test_is_negative(self):
        for i in set_of.negative_integers():
            expect(that_number(i).is_negative())

    def test_is_negative__negative_test(self):
        with negative_test():
            for i in set_of.positive_integers():
                expect(that_number(i).is_negative())

    def test_is_negative__special_case_zero(self):
        with negative_test():
            expect(that_number(0).is_negative())

    def test_is_bigger_than(self):
        for i in set_of.few_integers():
            for j in set_of.few_integers().bigger_than(i):
                expect(that_number(j).is_bigger_than(i))

    def test_is_bigger_than__negative_test(self):
        with negative_test():
            for i in set_of.few_integers():
                for j in set_of.few_integers().bigger_than(i):
                    expect(that_number(i).is_bigger_than(j))

    def test_is_bigger_than_equals(self):
        for i in set_of.few_integers():
            for j in set_of.few_integers().bigger_than_equals(i):
                expect(that_number(j).is_bigger_than_equals(i))

    def test_is_bigger_than_equals__negative_test(self):
        with negative_test():
            for i in set_of.few_integers():
                for j in set_of.few_integers().bigger_than_equals(i):
                    expect(that_number(i).is_bigger_than_equals(j))

    def test_is_less_than(self):
        for i in set_of.few_integers():
            for j in set_of.few_integers().less_than(i):
                expect(that_number(j).is_less_than(i))

    def test_is_less_than__negative_test(self):
        with negative_test():
            for i in set_of.few_integers():
                for j in set_of.few_integers().less_than(i):
                    expect(that_number(i).is_less_than(j))

    def test_is_less_than_equals(self):
        for i in set_of.few_integers():
            for j in set_of.few_integers().less_than_equals(i):
                expect(that_number(j).is_less_than_equals(i))

    def test_is_less_than_equals__negative_test(self):
        with negative_test():
            for i in set_of.few_integers():
                for j in set_of.few_integers().less_than_equals(i):
                    expect(that_number(i).is_less_than_equals(j))

    def test_can_chain_results(self):
        expect(that_number(1).is_positive().is_bigger_than(0))

    def test_can_chain_results__negative_test(self):
        with case("first link fails"):
            with negative_test():
                expect(that_number(1).is_negative().is_bigger_than(0))
        with case("second link fails"):
            with negative_test():
                expect(that_number(1).is_positive().is_bigger_than(2))
        with case("both link fails"):
            with negative_test():
                expect(that_number(1).is_negative().is_bigger_than(2))


class FunctionAssumptionTestCase(unittest.TestCase):
    def test_fails_with(self):
        error = TypeError

        expect(that_function(get_function_that_fails_with(error)).fails_with(error))

    def test_fails_with__negative_test(self):
        with case("No error raised"):
            with negative_test():
                expect(that_function(noop_function).fails_with(TypeError))
        with case("wrong error type"):
            with negative_test():
                expect(
                    that_function(get_function_that_fails_with(ValueError)).fails_with(
                        TypeError
                    )
                )


def noop_function():
    pass


def get_function_that_fails_with(error_type):
    def failing_function():
        raise error_type

    return failing_function


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

    def test_for_all(self):
        expect(that_list([1, 2, 3]).for_all(lambda v: that_number(v).is_positive()))

    def test_for_all__negative_test(self):
        with negative_test():
            expect(
                that_list([1, -2, 2, 3]).for_all(lambda v: that_number(v).is_positive())
            )


class DictionaryAssumptionTestCase(unittest.TestCase):
    def test_contains_key(self):
        expect(that_dict({1: 2, 3: 4}).contains_key(1))

    def test_contains_key__negative_test(self):
        with negative_test():
            expect(that_dict({1: 2, "test": 4}).contains_key(2))
