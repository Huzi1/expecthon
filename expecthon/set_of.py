#!/usr/bin/env python3


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


def integers():
    """
    Returns a generator of arbitrary integers (excluding zero)
    """
    return range(-1000, 1000, 3)


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
