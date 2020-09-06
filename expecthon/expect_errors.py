#!/usr/bin/env python3

from .expect import expect
from .assumptions import failed

__unittest = True


def negative_test():
    # TODO run as a subtest.
    return expection_that_code_raising(AssertionError)


def expection_that_code_raising(expected_exception: Exception):
    return ExpectExceptionRaisedContextManager(expected_exception)


class ExpectExceptionRaisedContextManager:
    def __init__(self, expected_exception: Exception):
        self._expected_exception = expected_exception

    def __enter__(self):
        # TODO find a way to run as a subtest
        ...

    def __exit__(self, type, value, traceback):
        if type == self._expected_exception:
            return True
        if type is not None:
            return False
        else:
            expect(
                failed(f"Testcase should have failed with {self._expected_exception}")
            )
