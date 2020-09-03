#!/usr/bin/env python3
import decimal
from typing import Callable

# TODO make a way to limit the size of generators / sets


def anything():
    """
    Returns a generator of arbitrary objects / values
    """
    # TODO make smaller
    return [*integers(), *strings()]


def strings():
    """
    Returns a generator of arbitrary strings
    """
    return ("A" * i for i in positive_integers())


def lists():
    """
    Returns a generator of arbitrary lists
    """
    return ([i] * i for i in positive_integers())


class IntGeneratorFactory:
    def __init__(
        self,
        min_value: int,
        max_value: int,
        step: int = 1,
        selector: Callable[[int], bool] = None,
    ):
        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        self._selector = selector or (lambda x: True)

    def __iter__(self):
        return (
            x
            for x in range(self._min_value, self._max_value, self._step)
            if self._selector(x)
        )

    def bigger_than_equals(self, limit: int) -> "IntGeneratorFactory":
        return type(self)(limit, self._max_value, self._step, self._selector)

    def bigger_than(self, limit: int) -> "IntGeneratorFactory":
        return self.bigger_than_equals(limit + 1)

    def less_than(self, limit: int) -> "IntGeneratorFactory":
        return type(self)(self._min_value, limit, self._step, self._selector)

    def less_than_equals(self, limit: int) -> "IntGeneratorFactory":
        return self.less_than(limit + 1)


def integers():
    """
    Returns a generator of arbitrary integers (excluding zero)
    """
    return IntGeneratorFactory(-500, 500, 9)


def few_integers():
    """
    Returns a generator of arbitrary integers (excluding zero)
    """
    return IntGeneratorFactory(-20, 20)


def positive_integers():
    """
    Returns a generator of arbitrary positive integers (excluding zero)
    """
    return range(1, 1000, 3)


def negative_integers():
    """
    Returns a generator of arbitrary negative integers (excluding zero)
    """
    return range(-1000, 0, 3)
