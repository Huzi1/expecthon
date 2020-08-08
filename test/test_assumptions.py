#!/usr/bin/env python3
"""
Test all `that_*` assumptions

These are all written by creating simple tests that should succeed or fail
and then running them.
"""

from expecthon import (
    expect,
    case,
    failed_test,
    success,
    assuming,
    that,
    that_function,
    that_list_of,
)
from expecthon.assumption_classes import BaseAssumption
from .assumptions import that_assumption
import unittest


class BaseAssumptionTestCase(unittest.TestCase):
    """
    Tests regarding the `BaseAssumption` and `that`
    """

    def test_that_that_returns_correct_type(self):
        expect(that(that(None)).is_type(BaseAssumption))

    def test_equals(self):
        with case("positive test"):
            expect(that_assumption(that(5 + 5).equals).with_arguments(10).succeeds())
        with case("negative test"):
            expect(that_assumption(that(5 + 1).equals).with_arguments(10).fails())

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


class ListAssumptionTestCase(unittest.TestCase):
    """
    Tests regarding the `ListAssumption` `that_list_of`
    """

    def test_is_empty(self):
        with case("positive test"):
            expect(that_assumption(that_list_of([]).is_empty).succeeds())
        with case("negative test"):
            expect(that_assumption(that_list_of([1]).is_empty).fails())

    def test_is_not_empty(self):
        with case("positive test"):
            expect(that_assumption(that_list_of([1]).is_not_empty).succeeds())
        with case("negative test"):
            expect(that_assumption(that_list_of([]).is_not_empty).fails())

    def test_has_length(self):
        for i in range(0, 10):
            with case(f"positive test (with length={i})"):
                expect(
                    that_assumption(that_list_of([i] * i).has_length)
                    .with_arguments(i)
                    .succeeds()
                )
        with case("negative test"):
            expect(
                that_assumption(that_list_of([1]).has_length).with_arguments(2).fails()
            )
