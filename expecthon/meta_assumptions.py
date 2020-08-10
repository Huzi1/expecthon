#!/usr/bin/env python3

# TODO add comments
from typing import Any, Callable, Dict, Tuple

from .assumptions import (
    FunctionAssumption,
    ListAssumption,
    that_list_of,
    BaseAssumption,
    that,
    assuming,
    AssumptionResult,
)
from .expect import expect


class AssumptionResultAssumption(BaseAssumption[AssumptionResult]):
    def _copy_with_added_result(
        self, new_result: AssumptionResult
    ) -> "AssumptionResultAssumption":
        return AssumptionResultAssumption(self._value, new_result & self._result)

    def is_successful(self) -> "AssumptionResultAssumption":
        return self._copy_with_added_result(
            assuming(
                that(self._value).is_type(AssumptionResult)
                & that_list_of(self._value.error_messages).is_empty()
                & that(self._value.success).is_true()
            ).else_report("Result was not successful")
        )

    def is_not_successful(self) -> "AssumptionResultAssumption":
        return self._copy_with_added_result(
            assuming(
                that(self._value).is_type(AssumptionResult)
                & that_list_of(self._value.error_messages).is_not_empty()
                & that(self._value.success).is_false()
            ).else_report("Result was not unsuccesful")
        )

    def has_failure_count_of(self, count: int) -> "AssumptionResultAssumption":
        return self._copy_with_added_result(
            self.is_not_successful()
            & that_list_of(self._value.error_messages).has_length(count)
        )

    def where_error_messages(self) -> ListAssumption:
        return ListAssumption(self._value.error_messages)


def that_result(result: AssumptionResult) -> AssumptionResultAssumption:
    return AssumptionResultAssumption(result)


class BaseAssumptionAssumption(BaseAssumption[Callable[[], Any]]):
    """
    Test assumptions regarding the BaseAssumption class
    """

    def __init__(
        self,
        func,
        func_args: Tuple[Any, ...] = None,
        func_kwargs: Dict[str, Any] = None,
        *args,
        **kwargs,
    ):
        super().__init__(func, *args, **kwargs)
        self._func_args = func_args or tuple()
        self._func_kwargs = func_kwargs or {}
        self._function_assumption = FunctionAssumption(
            lambda: expect(self._value(*self._func_args, **self._func_kwargs))
        )

    def _copy_with_added_result(
        self, new_result: AssumptionResult
    ) -> "BaseAssumptionAssumption":
        return BaseAssumptionAssumption(
            self._value, assumption_result=new_result & self._result
        )

    def succeeds(self) -> "BaseAssumptionAssumption":
        return self._copy_with_added_result(
            assuming(self._function_assumption.succeeds()).else_report(
                "Assumption should have succeeded!"
            )
        )

    def fails(self) -> "BaseAssumptionAssumption":
        # TODO contain the source of the error
        return self._copy_with_added_result(
            assuming(
                self._function_assumption.fails_with(AssertionError).result()
            ).else_report("Assumption should have failed")
        )

    def with_arguments(self, *args, **kwargs) -> "BaseAssumptionAssumption":
        return BaseAssumptionAssumption(self._value, args, kwargs, self._result)


def that_assumption(
    assumption: Callable[[], AssumptionResult]
) -> BaseAssumptionAssumption:
    return BaseAssumptionAssumption(assumption)
