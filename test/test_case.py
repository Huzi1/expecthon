#!/usr/bin/env python3
from unittest import TestCase
from expecthon import expect, case, that_function, success
from expecthon.case import InvalidCallerException


class CaseTestCase(TestCase):
    def test_fails_if_used_in_function_without_self(self):
        def failing_function():
            with case("This fails!"):
                ...

        expect(that_function(failing_function).fails_with(InvalidCallerException))

    def test_fails_if_self_isnt_testcase(self):
        def failing_function():
            # assigned as to make self defined
            self = 5
            with case("This fails!"):
                ...

        expect(that_function(failing_function).fails_with(InvalidCallerException))

    def test_succeeds(self):
        with case("this succeeds"):
            expect(success())
