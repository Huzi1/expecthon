#!/usr/bin/env python3

from typing import Any, Callable, List, Dict

from .base_assumption import BaseAssumption, assuming, not_assuming, that
from .builtin_assumptions import (
    FunctionAssumption,
    ListAssumption,
    NumberAssumption,
    StringAssumption,
    DictionaryAssumption,
)
from .result import AssumptionResult, failed, success, AssumptionResultBuilder

__unittest = True


def that_list(value: List[Any]) -> ListAssumption:
    return ListAssumption(value)


def that_dict(value: Dict[Any, Any]) -> DictionaryAssumption:
    return DictionaryAssumption(value)


def that_function(value: Callable[[], Any]) -> FunctionAssumption:
    return FunctionAssumption(value)


def that_number(value: Callable[[], Any]) -> NumberAssumption:
    return NumberAssumption(value)


def that_string(value: str) -> StringAssumption:
    return StringAssumption(value)


__all__ = [
    "assuming",
    "not_assuming",
    "AssumptionResult",
    "BaseAssumption",
    "AssumptionResultBuilder",
    "failed",  # TODO move to a static function
    "success",
    "that",
    "that_list",
    "that_function",
    "that_string",
    "that_number",
    "that_dict",
]
