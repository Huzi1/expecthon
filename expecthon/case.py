import inspect

CASE_TYPE_ERROR_MSG = "The case function should only be called from objects inheriting from unittest.TestCase"


def case(msg: str):
    """
    Return an instance of the result from calling subTest on the caller object.
    Syntactic sugar to avoid writing self.subTest(msg)
    """
    locals_from_calling_function = inspect.currentframe().f_back.f_locals

    if 'self' not in locals_from_calling_function:
        raise TypeError(CASE_TYPE_ERROR_MSG)

    self_from_calling_function = locals_from_calling_function['self']

    if not hasattr(self_from_calling_function, 'subTest'):
        raise TypeError(CASE_TYPE_ERROR_MSG)

    return self_from_calling_function.subTest(msg)
