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
        with case("positive test"):
            for i in set_of.integers():
                expect(that_assumption(that(i).equals).with_arguments(i).succeeds())
        with case("negative test"):
            expect(that_assumption(that(1 + 1).equals).with_arguments(3).fails())

    def test_doesnt_equals(self):
        with case("positive test"):
            for i in set_of.integers():
                expect(
                    that_assumption(that(i + 1).doesnt_equals)
                    .with_arguments(i)
                    .succeeds()
                )
        with case("negative test"):
            expect(that_assumption(that(1 + 1).doesnt_equals).with_arguments(2).fails())

    def test_is(self):
        with case("positive test"):
            expect(that_assumption(that(5).is_).with_arguments(5).succeeds())
        with case("negative test"):
            # as lists are pass by reference
            expect(that_assumption(that([1]).is_).with_arguments([1]).fails())

    def test_is_not(self):
        with case("positive test"):
            # as lists are pass by reference
            expect(that_assumption(that([1]).is_not).with_arguments([1]).succeeds())
        with case("negative test"):
            expect(that_assumption(that(1).is_not).with_arguments(1).fails())

    def test_is_type(self):
        with case("positive test"):
            expect(that_assumption(that(5).is_type).with_arguments(int).succeeds())
        with case("negative test"):
            expect(that_assumption(that("5").is_type).with_arguments(int).fails())

    def test_is_true(self):
        with case("positive test"):
            expect(that_assumption(that(True).is_true).succeeds())
        with case("negative test"):
            expect(that_assumption(that(False).is_true).fails())

    def test_is_false(self):
        with case("positive test"):
            expect(that_assumption(that(False).is_false).succeeds())
        with case("negative test"):
            expect(that_assumption(that(True).is_false).fails())


class StringAssumptionTestCase(unittest.TestCase):
    """
    Tests regarding the `StringAssumption` `that_string`
    """

    def test_contains(self):
        with case("positive test"):
            expect(
                that_assumption(that_string("test").contains)
                .with_arguments("te")
                .succeeds()
            )

        with case("negative test"):

            expect(
                that_assumption(that_list("test").contains)
                .with_arguments("ass")
                .fails()
            )


class NumlberAssumptionTestCase(unittest.TestCase):
    """
    Tests regarding the `DecimalAssumption` `that_number`
    """

    def test_contains(self):
        for i in set_of.positive_integers():
            with case(f"positive test (i={i})"):
                expect(that_assumption(that_number(i).is_positive).succeeds())

        with case("Zero Fails"):
            expect(that_assumption(that_number(0).is_positive).fails())
        for i in set_of.negative_integers():
            with case(f"negative test (i={i})"):
                expect(that_assumption(that_number(i).is_positive).fails())


class FunctionAssumptionTestCase(unittest.TestCase):
    ...
    # TODO


class ListAssumptionTestCase(unittest.TestCase):
    """
    Tests regarding the `ListAssumption` `that_list_of`
    """

    def test_is_empty(self):
        with case("positive test"):
            expect(that_assumption(that_list([]).is_empty).succeeds())
        with case("negative test"):
            expect(that_assumption(that_list([1]).is_empty).fails())

    def test_is_not_empty(self):
        with case("positive test"):
            expect(that_assumption(that_list([1]).is_not_empty).succeeds())
        with case("negative test"):
            expect(that_assumption(that_list([]).is_not_empty).fails())

    def test_has_length(self):
        with case(f"positive test"):
            for i in set_of.positive_integers():
                i_elements = [i] * i
                expect(that_list(i_elements).has_length(i))
                expect(
                    that_assumption(that_list(i_elements).has_length)
                    .with_arguments(i)
                    .succeeds()
                )
        with case("negative test"):
            expect(that_assumption(that_list([1]).has_length).with_arguments(2).fails())

    def test_contains(self):
        with case("positive test"):
            expect(
                that_assumption(that_list([1, 2, 3]).contains)
                .with_arguments(2)
                .succeeds()
            )

        with case("negative test"):

            expect(
                that_assumption(that_list([1, 2, 3]).contains).with_arguments(5).fails()
            )

    def test_has_any(self):
        with case("positive test"):
            expect(
                that_assumption(that_list([1, 2, 3]).has_any)
                .with_arguments(lambda v: that(v).equals(2))
                .succeeds()
            )
        with case("negative test"):
            expect(
                that_assumption(that_list([1, 2, 3]).has_any)
                .with_arguments(lambda v: that(v).equals(4))
                .fails()
            )


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
