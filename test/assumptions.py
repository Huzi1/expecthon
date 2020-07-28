#!/usr/bin/env python3

from expecthon import AssumptionResult, BaseAssumption, that, that_list_of
from expecthon.assumptions import ListAssumption

__all__ = ["AssumptionResultAssumption", "that_result", "empty", "failed"]


class AssumptionResultAssumption(BaseAssumption[AssumptionResult]):
    # TODO find out how to override type

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


def that_result(result: AssumptionResult) -> AssumptionResultAssumption:
    return AssumptionResultAssumption(result)


def empty() -> AssumptionResult:
    return AssumptionResult.empty()


def failed() -> AssumptionResult:
    return AssumptionResult(["failed"])
