#!/usr/bin/env python3
from typing import List
from .assumptions import AssumptionResult

__unittest = True


def expect(assumption: AssumptionResult) -> None:
    """
    Expect the assumption to be true - raises AssertionError otherwise
    """
    _raise_if_wrong_type(assumption)

    _raise_if_assumption_failed(assumption)


def _raise_if_wrong_type(assumption: AssumptionResult) -> None:
    if not isinstance(assumption, AssumptionResult):
        raise ValueError(f"{assumption} is the wrong type {type(assumption)}")


def _raise_if_assumption_failed(assumption: AssumptionResult):

    if not assumption.success:
        raise AssertionError(_format_error_messages(assumption.error_messages))


def _format_error_messages(error_messages: List[str]) -> str:
    if len(error_messages) == 1:
        return error_messages[0]
    indent = "  "
    sep = f"\n{indent} - "
    return (
        "Following errors occurred:" + sep + (sep.join(str(p) for p in error_messages))
    )
