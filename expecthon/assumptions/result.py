#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List, Optional, Union

__unittest = True


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
    def success(self) -> bool:
        """
        Whether no errors has been saved (the result is successful)
        """
        return not self.error_messages

    @classmethod
    def empty(cls) -> "AssumptionResult":
        return AssumptionResult([])

    def __and__(self, other: Union["AssumptionResult", None]) -> "AssumptionResult":
        if other is None:
            return self._copy()

        if isinstance(other, AssumptionResult):
            return AssumptionResult(self.error_messages + other.error_messages)
        return NotImplemented

    def __rand__(self, other: Union["AssumptionResult", None]) -> "AssumptionResult":
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
        return AssumptionResult([error_message] if not self._clause else [])


def failed(error_message: str) -> AssumptionResult:
    return AssumptionResult([error_message])


def success() -> AssumptionResult:
    return AssumptionResult([])


def assumption_result_or_empty(result: Optional[AssumptionResult]) -> AssumptionResult:
    """
    Returns the result if not None otherwise creates an empty result
    """
    if result is None:
        return AssumptionResult.empty()
    return result
