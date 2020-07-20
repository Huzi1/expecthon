#!/usr/bin/env python3
# TODO add comments

from typing import Any, List
from .assumption_classes import BaseAssumption, AssumptionResult, assuming


def that(value: Any) -> BaseAssumption:
    return BaseAssumption(value)


class ListAssumption(BaseAssumption):
    ValueType = List[Any]

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


def that_list_of(value: Any) -> ListAssumption:
    return ListAssumption(value)
