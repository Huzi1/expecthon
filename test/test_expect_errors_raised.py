#!/usr/bin/env python3

from unittest import TestCase

from expecthon import (
    expect,
    negative_test,
    that,
    failed,
    expection_that_code_raising,
    case,
)


class AssertionNotRaisedError(AssertionError):
    pass


# TODO find out how to do a negative test
class NegativeTestTestCase(TestCase):
    def test_negative_test(self):
        """
        Test that `negative_test` succeeds when needed
        """
        with negative_test():
            expect(that(False).is_true())

    def test_negative_test__negative_test(self):
        """
        Test that `negative_test` succeeds when needed
        """
        try:
            with negative_test():
                expect(that(True).is_true())
            raise AssertionNotRaisedError()
        except AssertionNotRaisedError:
            expect(failed("Error wasn't raised"))
        except AssertionError:
            pass


class ExpectExceptionRaisedContextManagerTestCase(TestCase):
    def test_expection_that_code_raising(self):
        with expection_that_code_raising(TypeError):
            raise TypeError

    def test_expection_that_code_raising__negative_test(self):
        with case("Other error"):
            unexpected_error = ValueError
            try:
                with expection_that_code_raising(TypeError):
                    raise unexpected_error()
                raise AssertionNotRaisedError()
            except AssertionNotRaisedError:
                expect(failed("Error wasn't raised"))
            except unexpected_error:
                pass
        with case("No error"):
            with negative_test():
                with expection_that_code_raising(TypeError):
                    pass
