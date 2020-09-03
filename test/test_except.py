#!/usr/bin/env python3


import unittest

from expecthon import (
    expect,
    failed,
    that_string,
    negative_test,
    expection_that_code_raising,
)


class AssertionNotRaisedError(Exception):
    MSG = "Should have raised AssertionError"


class ExceptTestCase(unittest.TestCase):
    """
    Test that the `except` function works correctly
    """

    def test_except_fails(self):
        error_msg = "test_error"
        # TODO verify that raised error has the correct body
        with negative_test():
            expect(failed(error_msg))

    def test_except_fails_multiple(self):
        error_msg_1 = "error 1"
        error_msg_2 = "error 2"
        # TODO verify that raised error has the correct body
        with negative_test():
            expect(failed(error_msg_1) & failed(error_msg_2))

    def test_except_fails_if_wrong_type(self):
        with expection_that_code_raising(ValueError):
            expect(1)
