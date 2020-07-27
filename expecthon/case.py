import inspect
from unittest import TestCase
from typing import Dict, Any


class InvalidCallerException(Exception):
    msg = "The case function should only be called from objects inheriting from unittest.TestCase"


def case(msg: str):
    """
    Return an instance of the result from calling subTest on the caller object.
    Syntactic sugar to avoid writing self.subTest(msg)
    """

    test_case = get_testcase_from_caller(inspect.currentframe())

    return test_case.subTest(msg)


def get_testcase_from_caller(frame) -> TestCase:
    test_case = get_self_from_caller(frame)
    if not isinstance(test_case, TestCase):
        raise InvalidCallerException()
    return test_case


def get_self_from_caller(frame) -> object:
    locals_from_calling_function = get_locals_from_caller(frame)

    if "self" not in locals_from_calling_function:
        raise InvalidCallerException()
    return locals_from_calling_function["self"]


def get_locals_from_caller(frame) -> Dict[str, Any]:
    return frame.f_back.f_locals
