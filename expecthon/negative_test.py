#!/usr/bin/env python3
from .expect import expect
from .assumptions import failed

__unittest = True


def negative_test():
    # TODO run as a subtest.
    return NegativeTestContextManager()


class NegativeTestContextManager:
    def __enter__(self):
        # TODO find a way to run as a subtest
        ...

    def __exit__(self, type, value, traceback):
        if type == AssertionError:
            return True
        if type is not None:
            raise type

        expect(failed("Testcase should have failed"))
