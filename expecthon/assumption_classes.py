#!/usr/bin/env python3
from typing import TypeVar, Union, Optional, List
from dataclasses import dataclass


@dataclass
class AssumptionResult:
    """
    Holds the result of a given assumption / test expection.

    Accessible is all the errors, in other words, the failed assumptions, as well
    as a few helper methods in this regard.
    """
    error_messages: List[str]

    def _copy(self) -> "AssumptionResult":
        return AssumptionResult(self.error_messages)

    @property
    def success(self):
        return not self.error_messages

    @classmethod
    def empty(cls) -> "AssumptionResult":
        return AssumptionResult([])

    def __and__(self, other: Union["AssumptionResult", "BaseAssumption", None]) -> "AssumptionResult":
        if other is None:
            return self._copy()
        if isinstance(other, BaseAssumption):
            other = other._result

        if isinstance(other, AssumptionResult):
            return AssumptionResult(
                self.error_messages +
                other.error_messages
            )
        raise NotImplementedError()

    def __plus__(self, other: Union["AssumptionResult", "BaseAssumption", None]) -> "AssumptionResult":
        return self & other


class AssumptionResultBuilder:
    """
    Builder to create a fluent interface for creating AssumptionResults

    Should primarily be used with `assuming`
    """

    def __init__(self, clause: bool):
        self._clause = clause

    def else_report(self, error_message: str) -> AssumptionResult:
        """
        Returns a failed AssumptionResult if self._clause is true with the given error messages
        """
        return AssumptionResult([error_message] if self._clause else [])


def assuming(clause: bool) -> AssumptionResultBuilder:
    """
    Returns a builder for AssumptionResults for fluent interfaces.

    Can be used like:
    `assuming(1+1).else_report("One doesn't equal One")`
    """
    return AssumptionResultBuilder(clause)


T = TypeVar("T")


class BaseAssumption:
    """
    Used to create AssumptionResults, which is the basis for any test

    We Have an assumption, which we then test with the interpreter (and our testcases),
    which in turn returns a AssumptionResult, which shows all the failed assumptions.
    """

    def __init__(self, value: T, assumption_result: Optional[AssumptionResult] = None):
        self._value = value
        self._result = assumption_result_or_empty(assumption_result)

    def _copy_with_added_result(self, new_result: AssumptionResult) -> "BaseAssumption":
        return BaseAssumption(self._value, new_result & self._result)

    def equals(self, expected_value: T) -> "BaseAssumption":
        return self._copy_with_added_result(assuming(
            self._value == expected_value
        ).else_report(
            f"{self._value} should equal {expected_value}"
        ))

    def doesnt_equals(self, expected_value: T) -> "BaseAssumption":
        return self._copy_with_added_result(assuming(
            self._value == expected_value
        ).else_report(
            f"{self._value} shouldn't equal {expected_value}"
        ))

    def is_(self, expected_value: T) -> "BaseAssumption":
        return self._copy_with_added_result(assuming(
            self._value is expected_value
        ).else_report(
            f"{self._value} should be {expected_value}"
        ))

    def is_not(self, expected_value: T) -> "BaseAssumption":
        return self._copy_with_added_result(assuming(
            self._value is not expected_value
        ).else_report(
            f"{self._value} should be {expected_value}"
        ))

    def __and__(self, other: Union["BaseAssumption", AssumptionResult, None]) -> AssumptionResult:

        if other is None:
            return self._result
        if isinstance(other, AssumptionResult):
            return self._result & other
        return self._result & other._result


def assumption_result_or_empty(result: Optional[AssumptionResult]) -> AssumptionResult:
    """
    Returns the result if not None otherwise creates an empty result
    """
    if result is None:
        return AssumptionResult.empty()
    return result
