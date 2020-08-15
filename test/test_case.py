#!/usr/bin/env python3
import inspect
from unittest import TestCase

from expecthon import case, expect, success, that
from expecthon.case import get_testcase


# TODO find out how to do a negative test
class CaseTestCase(TestCase):
    def test_get_testcase(self):
        """
        Test that the correct testcase is found
        """
        testcase = get_testcase(inspect.currentframe())
        expect(that(testcase).equals(self))

    def test_get_testcase_in_nested_function(self):
        """
        Test that the correct testcase is found in nested function
        """

        def get_test_case_wrapper():
            return lambda: get_testcase(inspect.currentframe())

        testcase = get_test_case_wrapper()()
        expect(that(testcase).equals(self))

    def test_can_use_case(self):
        with case("this succeeds"):
            expect(success())
