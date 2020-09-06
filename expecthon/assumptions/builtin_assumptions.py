#!/usr/bin/env python3
# TODO add comments
import decimal
from typing import Any, Callable, List, Type, Union, Optional, Dict

from .base_assumption import BaseAssumption, assuming, not_assuming, that
from .result import AssumptionResult, failed

__unittest = True


class ListAssumption(BaseAssumption[List[Any]]):
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

    def for_all(
        self, assumer_func: Callable[[Any], AssumptionResult]
    ) -> "ListAssumption":
        # TODO find a way to visualize the function
        return self._add_result(
            assuming(
                all(assumer_func(element).success for element in self._value)
            ).else_report(f"No elements that fulfill the clause was found")
        )


class CaseInsensitiveStringAssumption(BaseAssumption[str]):
    def __init__(
        self, value: str, assumption_result: Optional[AssumptionResult] = None
    ):
        super().__init__(value.lower(), assumption_result)

    def equals(self, expected_value) -> "CaseInsensitiveStringAssumption":
        return super().equals(expected_value.lower())


class StringAssumption(BaseAssumption[str]):
    def contains(self, expected_value: Any) -> "ListAssumption":
        return self._add_result(
            assuming(expected_value in self._value).else_report(
                f"{self._value} doesn't contain ´{expected_value}´"
            )
        )

    def insensitively(self) -> CaseInsensitiveStringAssumption:
        return CaseInsensitiveStringAssumption(self._value)


class NumberAssumption(BaseAssumption[Union[decimal.Decimal, float, int]]):
    def is_positive(self) -> "NumberAssumption":
        return self._add_result(
            assuming(self._value > 0).else_report(
                f"{self._value} isn't bigger than zero"
            )
        )

    def is_negative(self) -> "NumberAssumption":
        return self._add_result(
            assuming(self._value < 0).else_report(
                f"{self._value} isn't bigger than zero"
            )
        )

    def is_bigger_than(self, limit: decimal.Decimal) -> "NumberAssumption":
        return self._add_result(
            assuming(self._value > limit).else_report(
                f"{self._value} isn't bigger than {limit}"
            )
        )

    def is_bigger_than_equals(self, limit: decimal.Decimal) -> "NumberAssumption":
        return self._add_result(
            assuming(self._value >= limit).else_report(
                f"{self._value} isn't bigger than or equals {limit}"
            )
        )

    def is_less_than(self, limit: decimal.Decimal) -> "NumberAssumption":
        return self._add_result(
            assuming(self._value < limit).else_report(
                f"{self._value} isn't less than {limit}"
            )
        )

    def is_less_than_equals(self, limit: decimal.Decimal) -> "NumberAssumption":
        return self._add_result(
            assuming(self._value <= limit).else_report(
                f"{self._value} isn't less than or equals {limit}"
            )
        )


class DictionaryAssumption(BaseAssumption[Dict[Any, Any]]):
    def contains_key(self, expected_key: Any) -> "DictionaryAssumption":
        return self._add_result(
            assuming(expected_key in self._value).else_report(
                f"{self._value} doesn't contain the key `{expected_key}`"
            )
        )


class FunctionAssumption(BaseAssumption[Callable[[], Any]]):
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
