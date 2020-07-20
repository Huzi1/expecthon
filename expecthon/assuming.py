#!/usr/bin/env python3

from typing import Any
from .assumption_classes import BaseAssumption


def that(value: Any) -> BaseAssumption:
    return BaseAssumption(value)
