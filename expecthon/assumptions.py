#!/usr/bin/env python3
# TODO add comments

from typing import Any, List, Callable
from .assumption_classes import BaseAssumption, AssumptionResult, assuming, failed_test


def that(value: Any) -> BaseAssumption:
    return BaseAssumption(value)


class ListAssumption(BaseAssumption[List[Any]]):
    def _copy_with_added_result(self, new_result: AssumptionResult) -> "ListAssumption":
        return ListAssumption(self._value, new_result & self._result)

    def is_empty(self) -> "ListAssumption":
        return self._copy_with_added_result(
            assuming(len(self._value) == 0).else_report(f"{self._value} is not empty")
        )

    def is_not_empty(self) -> "ListAssumption":
        return self._copy_with_added_result(
            assuming(len(self._value) != 0).else_report(f"{self._value} is empty")
        )

    def has_length(self, expected_value: int) -> "ListAssumption":
        return self._copy_with_added_result(
            assuming(len(self._value) == expected_value).else_report(
                f"{self._value} should be length {expected_value}"
            )
        )

    def contains(self, expected_value: Any) -> "ListAssumption":
        return self._copy_with_added_result(
            assuming(expected_value in self._value).else_report(
                f"{self._value} doesn't contain ´{expected_value}´"
            )
        )


class FunctionAssumption(BaseAssumption[Callable[[], Any]]):

    # TODO find a way where we don't have to repeat this
    def _copy_with_added_result(self, new_result: AssumptionResult) -> "ListAssumption":
        return ListAssumption(self._value, new_result & self._result)

    def fails_with(self, expected_exception: Exception) -> "FunctionAssumption":
        try:
            self._value()
            return self._copy_with_added_result(
                failed_test(f"function should have failed with {expected_exception}")
            )
        except Exception as exception:
            return self._copy_with_added_result(
                assuming(type(exception) is expected_exception).else_report(
                    "Wrong exception raised -"
                    f" expected {expected_exception}, but got {type(exception)}"
                )
            )


def that_list_of(value: List[Any]) -> ListAssumption:
    return ListAssumption(value)


def that_function(value: Callable[[], Any]) -> FunctionAssumption:
    return FunctionAssumption(value)
