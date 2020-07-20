#!/usr/bin/env python3
"""
Tests the core classes for the underlying system
"""
import unittest
from expecthon import (
    AssumptionResult,
    expect,
    that,
    that_list_of,
    BaseAssumption,
)


class AssumptionResultAssumption(BaseAssumption):
    # TODO find out how to override type
    ValueType = AssumptionResult

    def is_successful(self) -> "AssumptionResult":
        return (
            that(self._value).is_type(AssumptionResult)
            & that_list_of(self._value.error_messages).is_empty()
            & that(self._value.success).is_true()
        )

    def is_not_successful(self) -> "AssumptionResult":
        return (
            that(self._value).is_type(AssumptionResult)
            & that_list_of(self._value.error_messages).is_not_empty()
            & that(self._value.success).is_false()
        )


def that_assumption_result(result: AssumptionResult) -> AssumptionResultAssumption:
    return AssumptionResultAssumption(result)


def empty():
    return AssumptionResult.empty()


def fail_result():
    return AssumptionResult(["failed"])


class AssumptionResultTestCase(unittest.TestCase):
    """
    Test all operations on the AssumptionResult class
    """

    def test_empty(self):
        """
        Test the `AssumptionResult.empty()` function
        """
        expect(that_assumption_result(empty()).is_successful())

    def test_and(self):
        """
        Test the bitwise `&` operator which concats two results
        """
        with self.subTest("Both successful"):
            result = empty() & empty()
            expect(that_assumption_result(result).is_successful())
        with self.subTest("first fail, second succeed"):
            result = fail_result() & empty()
            expect(that_assumption_result(result).is_not_successful()
                   & that_list_of(result.error_messages).has_length(1)
                   )
        with self.subTest("first succeed, second fail"):
            result = empty() & fail_result()
            expect(
                that_assumption_result(result).is_not_successful()
                & that_list_of(result.error_messages).has_length(1)
            )
        with self.subTest("two fail"):
            result = fail_result() & fail_result()
            expect(
                that_assumption_result(result).is_not_successful()
                & that_list_of(result.error_messages).has_length(2)
            )
            with self.subTest("three chained"):
                with self.subTest("combined first"):
                    combined_result = result & fail_result()
                    expect(
                        that_assumption_result(combined_result).is_not_successful()
                        & that_list_of(combined_result.error_messages).has_length(3)
                    )
                with self.subTest("combined last"):
                    combined_result = fail_result() & result
                    expect(
                        that_assumption_result(combined_result).is_not_successful()
                        & that_list_of(combined_result.error_messages).has_length(3)
                    )
