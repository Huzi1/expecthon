#!/usr/bin/env python3

from unittest import TestCase

from expecthon import expect, negative_test, that


# TODO find out how to do a negative test
class CaseTestCase(TestCase):
    def test_negative_test(self):
        """
        Test that `negative_test` succeeds when needed
        """
        with negative_test():
            expect(that(False).is_true())
