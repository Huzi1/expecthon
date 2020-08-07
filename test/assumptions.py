#!/usr/bin/env python3

from typing import Callable, List, Dict, Any, Tuple
from expecthon import (
    AssumptionResult,
    BaseAssumption,
    that,
    that_list_of,
    that_function,
)
from expecthon.assumptions import ListAssumption, FunctionAssumption
from expecthon import expect

__all__ = ["AssumptionResultAssumption", "that_result", "empty", "failed"]


class AssumptionResultAssumption(BaseAssumption[AssumptionResult]):
    def _copy_with_added_result(
        self, new_result: AssumptionResult
    ) -> "AssumptionResultAssumption":
        return AssumptionResultAssumption(self._value, new_result & self._result)

    def is_successful(self) -> "AssumptionResultAssumption":
        return self._copy_with_added_result(
            that(self._value).is_type(AssumptionResult)
            & that_list_of(self._value.error_messages).is_empty()
            & that(self._value.success).is_true()
        )

    def is_not_successful(self) -> "AssumptionResultAssumption":
        return self._copy_with_added_result(
            that(self._value).is_type(AssumptionResult)
            & that_list_of(self._value.error_messages).is_not_empty()
            & that(self._value.success).is_false()
        )

    def has_failure_count_of(self, count: int) -> "AssumptionResultAssumption":
        return self._copy_with_added_result(
            self.is_not_successful()
            & that_list_of(self._value.error_messages).has_length(count)
        )

    def where_error_messages(self) -> ListAssumption:
        return ListAssumption(self._value.error_messages)


class BaseAssumptionAssumption(BaseAssumption[Callable[[], Any]]):
    """
    Test assumptions regarding the BaseAssumption class
    """

    def __init__(
        self,
        func,
        func_args: Tuple[Any] = None,
        func_kwargs: Dict[str, Any] = None,
        *args,
        **kwargs
    ):
        super().__init__(func, *args, **kwargs)
        self._func_args = func_args or tuple()
        self._func_kwargs = func_kwargs or {}

    def _copy_with_added_result(
        self, new_result: AssumptionResult
    ) -> "BaseAssumptionAssumption":
        return BaseAssumptionAssumption(
            self._value, assumption_result=new_result & self._result
        )

    def succeeds(self) -> "BaseAssumptionAssumption":
        return self._copy_with_added_result(
            FunctionAssumption(
                lambda: expect(self._value(*self._func_args, **self._func_kwargs))
            )
            .succeeds()
            .result()
        )

    def fails(self) -> "BaseAssumptionAssumption":
        return self._copy_with_added_result(
            FunctionAssumption(
                lambda: expect(self._value(*self._func_args, **self._func_kwargs))
            )
            .fails_with(AssertionError)
            .result()
        )

    def with_arguments(self, *args, **kwargs) -> "BaseAssumptionAssumption":
        return BaseAssumptionAssumption(self._value, args, kwargs, self._result)


def that_result(result: AssumptionResult) -> AssumptionResultAssumption:
    return AssumptionResultAssumption(result)


def that_assumption(
    assumption: Callable[[], AssumptionResult]
) -> BaseAssumptionAssumption:
    return BaseAssumptionAssumption(assumption)


def empty() -> AssumptionResult:
    return AssumptionResult.empty()


def failed() -> AssumptionResult:
    return AssumptionResult(["failed"])
