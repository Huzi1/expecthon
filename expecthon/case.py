import inspect


def case(msg: str):
    """
    Return an instance of the result from calling subTest on the caller object.
    Syntactic sugar to avoid writing self.subTest(msg)
    """
    return inspect.currentframe().f_back.f_locals['self'].subTest(msg)
