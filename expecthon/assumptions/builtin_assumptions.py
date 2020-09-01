#!/usr/bin/env python3
# TODO add comments
import decimal
from typing import Any, Callable, List, Type, Union

from .base_assumption import BaseAssumption, assuming, not_assuming, that
from .result import AssumptionResult, failed

__unittest = True


class ListAssumption(BaseAssumption[List[Any]]):
    def _add_result(self, new_result: AssumptionResult) -> "ListAssumption":
        return ListAssumption(self._value, new_result & self)

    def is_empty(self) -> "ListAssumption":
        return self._add_result(
            assuming(that(len(self._value)).equals(0)).else_report(
                f"{self._value} is not empty"
            )
        )

    def is_not_empty(self) -> "ListAssumption":
        return self._add_result(
            not_assuming(self.is_empty()).else_report(f"{self._value} is empty")
        )

    def has_length(self, expected_value: int) -> "ListAssumption":
        return self._add_result(
            assuming(that(len(self._value)).equals(expected_value)).else_report(
                f"{self._value} should be length {expected_value}"
            )
        )

    def contains(self, expected_value: Any) -> "ListAssumption":
        return self._add_result(
            assuming(expected_value in self._value).else_report(
                f"{self._value} doesn't contain ´{expected_value}´"
            )
        )

    def has_any(
        self, assumer_func: Callable[[Any], AssumptionResult]
    ) -> "ListAssumption":
        # TODO find a way to visualize the function
        return self._add_result(
            assuming(
                any(assumer_func(element).success for element in self._value)
            ).else_report(f"No elements that fulfill the clause was found")
        )


class StringAssumption(BaseAssumption[str]):
    def _add_result(self, new_result: AssumptionResult) -> "StringAssumption":
        return StringAssumption(self._value, new_result & self)

    def contains(self, expected_value: Any) -> "ListAssumption":
        return self._add_result(
            assuming(expected_value in self._value).else_report(
                f"{self._value} doesn't contain ´{expected_value}´"
            )
        )


class DecimalAssumption(BaseAssumption[decimal.Decimal]):
    def _add_result(self, new_result: AssumptionResult) -> "DecimalAssumption":
        return DecimalAssumption(self._value, new_result & self)

    def is_positive(self) -> "DecimalAssumption":
        return self._add_result(
            assuming(self._value > 0).else_report(
                f"{self._value} isn't bigger than zero"
            )
        )

    def is_negative(self) -> "DecimalAssumption":
        return self._add_result(
            assuming(self._value < 0).else_report(
                f"{self._value} isn't bigger than zero"
            )
        )

    def is_bigger_than(self, limit: decimal.Decimal) -> "DecimalAssumption":
        return self._add_result(
            assuming(self._value > limit).else_report(
                f"{self._value} isn't bigger than {limit}"
            )
        )

    def is_bigger_than_equals(self, limit: decimal.Decimal) -> "DecimalAssumption":
        return self._add_result(
            assuming(self._value >= limit).else_report(
                f"{self._value} isn't bigger than or equals {limit}"
            )
        )

    def is_less_than(self, limit: decimal.Decimal) -> "DecimalAssumption":
        return self._add_result(
            assuming(self._value < limit).else_report(
                f"{self._value} isn't less than {limit}"
            )
        )

    def is_less_than_equals(self, limit: decimal.Decimal) -> "DecimalAssumption":
        return self._add_result(
            assuming(self._value <= limit).else_report(
                f"{self._value} isn't less than or equals {limit}"
            )
        )


class FunctionAssumption(BaseAssumption[Callable[[], Any]]):

    # TODO find a way where we don't have to repeat this
    def _add_result(self, new_result: AssumptionResult) -> "FunctionAssumption":
        return FunctionAssumption(self._value, new_result & self)

    def fails_with(
        self, expected_exception: Union[Exception, Type[Exception]]
    ) -> "FunctionAssumption":
        try:
            self._value()
            return self._add_result(
                failed(f"function should have failed with {expected_exception}")
            )
        except Exception as exception:
            return self._add_result(
                assuming(type(exception) is expected_exception).else_report(
                    "Wrong exception raised -"
                    f" expected {expected_exception}, but got {type(exception)}"
                )
            )

    def succeeds(self) -> "FunctionAssumption":
        try:
            self._value()
            return self._copy()
        except Exception as exception:
            return self._add_result(
                failed(f"function should have succeeded (failed with {exception})")
            )
