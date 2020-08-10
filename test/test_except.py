#!/usr/bin/env python3


import unittest

from expecthon import expect, failed, that_string


class ExceptTestCase(unittest.TestCase):
    """
    Test that the `except` function works correctly
    """

    def test_except_fails(self):
        """
        Test the `AssumptionResult.empty()` function
        """
        error_msg = "test_error"
        try:
            expect(failed(error_msg))

            raise Exception()
        except AssertionError as e:
            expect(that_string(str(e)).contains(error_msg))
        except Exception as e:
            raise AssertionError("Should have raised AssertionError") from e

    def test_except_fails_multiple(self):
        """
        Test the `AssumptionResult.empty()` function
        """
        error_msg_1 = "error 1"
        error_msg_2 = "error 2"
        try:
            expect(failed(error_msg_1) & failed(error_msg_2))

            raise Exception()
        except AssertionError as e:
            that_error_message = that_string(str(e))
            expect(
                that_error_message.contains(error_msg_1)
                & that_error_message.contains(error_msg_2)
            )
        except Exception as e:
            raise AssertionError("Should have raised AssertionError") from e

    def test_except_fails_if_wrong_type(self):
        """
        Test the `AssumptionResult.empty()` function
        """
        try:
            expect(1)

            raise Exception()
        except ValueError:
            # All good, this should happen.
            pass
        except Exception as e:
            raise AssertionError("Should have raised AssertionError") from e
