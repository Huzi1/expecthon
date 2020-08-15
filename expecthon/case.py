import inspect
from unittest import TestCase
from .expect import expect
from .assumptions import failed


class InvalidCallerException(Exception):
    msg = "The case function should only be called from objects inheriting from unittest.TestCase"


def case(msg: str):
    """
    Return an instance of the result from calling subTest on the caller object.
    Syntactic sugar to avoid writing self.subTest(msg)
    """

    test_case = get_testcase(inspect.currentframe())

    return test_case.subTest(msg)


def get_testcase(frame) -> TestCase:
    test_case = frame.f_locals.get("self", None)
    if test_case is None or not isinstance(test_case, TestCase):
        if frame.f_back:
            return get_testcase(frame.f_back)

        raise InvalidCallerException()

    return test_case
