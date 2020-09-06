#!/usr/bin/env python3
"""
Tests the core classes for the underlying system
"""
import unittest

from expecthon import (
    expect,
    case,
    success,
    assuming,
    that,
    that_result,
    expection_that_code_raising,
)
from expecthon.assumptions import AssumptionResultBuilder

from .helpers import empty, failed


class AssumptionResultTestCase(unittest.TestCase):
    """
    Test all operations and helpers related to the AssumptionResult class
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

    def test_and_none(self):
        """
        Test that we can do `A & None`
        """
        result = failed() & None
        expect(that_result(result).has_failure_count_of(1))

    def test_and_wrong_type(self):
        """
        Test that we can do `A & None`
        """
        with expection_that_code_raising(TypeError):
            result = failed() & "bla"

    def test_success(self):
        """
        test the `failed_test` helper function
        """
        expect(that_result(success()).is_successful())

    def test_failed_test(self):
        """
        test the `failed_test` helper function
        """
        error_msg = "fail"
        expect(
            that_result(failed(error_msg))
            .has_failure_count_of(1)
            .and_()
            .where_error_messages()
            .contains(error_msg)
        )


class AssumptionResultBuilderTestCase(unittest.TestCase):
    """
    Test all helpers and operations of the AssumptionResultBuilder
    """

    def test_assuming(self):
        """
        test the `assuming` helper function
        """

        error_msg = "fail"
        with case("returns Builder True"):
            expect(that(assuming(True)).is_instance_of(AssumptionResultBuilder))
        with case("or_else is empty if clause is True"):
            expect(that_result(assuming(True).else_report(error_msg)).is_successful())

        with case("or_else is not empty if clause is False"):
            expect(
                that_result(assuming(False).else_report(error_msg))
                .has_failure_count_of(1)
                .and_()
                .where_error_messages()
                .contains(error_msg)
            )
