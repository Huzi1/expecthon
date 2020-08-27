#!/usr/bin/env python3
from typing import Generic, Optional, TypeVar, Union, Any

from .result import (
    AssumptionResult,
    assumption_result_or_empty,
    AssumptionResultBuilder,
)

T = TypeVar("T")


class BaseAssumption(Generic[T], AssumptionResult, object):
    """
    Used to create AssumptionResults, which is the basis for any test

    We Have an assumption, which we then test with the interpreter (and our testcases),
    which in turn returns a AssumptionResult, which shows all the failed assumptions.
    """

    def __init__(self, value: T, assumption_result: Optional[AssumptionResult] = None):
        self._value = value
        super().__init__(assumption_result_or_empty(assumption_result).error_messages)

    def _add_result(
        self, new_result: AssumptionResult
    ) -> "BaseAssumption[T]":
        return type(self)(self._value, self & new_result)

    def _copy(self) -> "BaseAssumption[T]":
        return type(self)(self._value, self)

    def equals(self, expected_value: T) -> "BaseAssumption":
        return self._add_result(
            assuming(self._value == expected_value).else_report(
                f"{self._value} should equal {expected_value}"
            )
        )

    def doesnt_equals(self, expected_value: T) -> "BaseAssumption":
        return self._add_result(
            assuming(self._value != expected_value).else_report(
                f"{self._value} shouldn't equal {expected_value}"
            )
        )

    def is_(self, expected_value: T) -> "BaseAssumption":
        return self._add_result(
            assuming(self._value is expected_value).else_report(
                f"{self._value} should be {expected_value}"
            )
        )

    def is_not(self, expected_value: T) -> "BaseAssumption":
        return self._add_result(
            assuming(self._value is not expected_value).else_report(
                f"{self._value} should be {expected_value}"
            )
        )

    def is_false(self) -> "BaseAssumption":
        return self._add_result(
            assuming(not bool(self._value)).else_report(
                f"{self._value} should be falsy"
            )
        )

    def is_true(self) -> "BaseAssumption":
        return self._add_result(
            assuming(bool(self._value)).else_report(f"{self._value} should be truthy")
        )

    def is_type(self, expected_type: type) -> "BaseAssumption":
        return self._add_result(
            assuming(isinstance(self._value, expected_type)).else_report(
                f"{self._value} is not instance of {expected_type}"
            )
        )

    def and_(self) -> "BaseAssumption":
        return self._copy()


def that(value: Any) -> BaseAssumption:
    return BaseAssumption(value)


def not_assuming(
    clause: Union[bool, AssumptionResult, BaseAssumption]
) -> AssumptionResultBuilder:
    """
    Returns a builder for AssumptionResults for fluent interfaces.

    Can be used like:
    `assuming(1+1).else_report("One doesn't equal One")`
    """
    if isinstance(clause, AssumptionResult):
        clause = clause.success
    return AssumptionResultBuilder(not clause)


def assuming(
    clause: Union[bool, AssumptionResult, BaseAssumption]
) -> AssumptionResultBuilder:
    """
    Returns a builder for AssumptionResults for fluent interfaces.

    Can be used like:
    `assuming(1+1).else_report("One doesn't equal One")`
    """
    if isinstance(clause, AssumptionResult):
        clause = clause.success
    return AssumptionResultBuilder(clause)
