#!/usr/bin/env python3

from expecthon.assumptions import AssumptionResult


def empty() -> AssumptionResult:
    return AssumptionResult.empty()


def failed(msg: str = "failed") -> AssumptionResult:
    return AssumptionResult([msg])
