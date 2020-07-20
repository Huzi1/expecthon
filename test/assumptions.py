#!/usr/bin/env python3

from expecthon import AssumptionResult, BaseAssumption, that, that_list_of


class AssumptionResultAssumption(BaseAssumption[AssumptionResult]):
    # TODO find out how to override type

    def is_successful(self) -> "AssumptionResult":
        return (
            that(self._value).is_type(AssumptionResult)
            & that_list_of(self._value.error_messages).is_empty()
            & that(self._value.success).is_true()
        )

    def is_not_successful(self) -> "AssumptionResult":
        return (
            that(self._value).is_type(AssumptionResult)
            & that_list_of(self._value.error_messages).is_not_empty()
            & that(self._value.success).is_false()
        )

    def has_failure_count_of(self, count: int) -> "AssumptionResult":
        return self.is_not_successful() & that_list_of(
            self._value.error_messages
        ).has_length(count)


def that_result(result: AssumptionResult) -> AssumptionResultAssumption:
    return AssumptionResultAssumption(result)


def empty():
    return AssumptionResult.empty()


def failed():
    return AssumptionResult(["failed"])
