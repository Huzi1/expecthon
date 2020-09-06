# Expecthon
**Status**[![PyPi - Version](https://img.shields.io/pypi/v/expecthon.svg)](https://pypi.org/project/expecthon/)
![supported-versions](https://img.shields.io/pypi/pyversions/expecthon.svg)
![PyPI - Status](https://img.shields.io/pypi/status/expecthon)
[![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/expecthon)](https://libraries.io/pypi/expecthon/sourcerank)


**Main**
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=svadilfare_expecthon&metric=coverage)](https://sonarcloud.io/dashboard?id=svadilfare_expecthon)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=svadilfare_expecthon&metric=alert_status)](https://sonarcloud.io/dashboard?id=svadilfare_expecthon) 
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=svadilfare_expecthon&metric=code_smells)](https://sonarcloud.io/dashboard?id=svadilfare_expecthon)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=svadilfare_expecthon&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=svadilfare_expecthon)


**Develop**
[![Coverage](https://sonarcloud.io/api/project_badges/measure?branch=develop&project=svadilfare_expecthon&metric=coverage)](https://sonarcloud.io/dashboard?id=svadilfare_expecthon)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?branch=develop&project=svadilfare_expecthon&metric=alert_status)](https://sonarcloud.io/dashboard?id=svadilfare_expecthon) 
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?branch=develop&project=svadilfare_expecthon&metric=code_smells)](https://sonarcloud.io/dashboard?id=svadilfare_expecthon)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?branch=develop&project=svadilfare_expecthon&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=svadilfare_expecthon)


python spec testing framework. This aims to help make tests as readable as
possible, by composing your tests in natural language. It wraps the builtin
unittest module.

## Requirements

Supports \*Python >=3.7

## Install

`pip install expecthon`

## Examples

Examples range in complexity.

### Simple

A very simple example

```python
from expecthon import expect, that

expect(
   that(5+5).equal(10)
)
```

Unlike normal testing you can test multiple things at the same time, making
debugging more easy, as you don't simply get the first failed assertion, but all
(if you so choose)

```python
from expecthon import expect, that_number

x = 4
expect(
 that_number(x).is_negative()
 & that_number(x).is_divisble_by(3)
)
```

which will raise an failed assertion showing both errors.

### Lists

Some times you have a large list of elements and you want to test whether one of
the elements live up to some rule. This can be done the following way:

```python
from expecthon import expect, that, that_number, that_list

def value_that_is_positive(value):
    return that_number(value).is_positive()

expect(that_list([-1, -2, 1, -3]).has_any(value_that_is_positive))
```

### Negative tests

You do, at times, want to test that something is _not_ the case. This has mainly
been relevant in the context of developing this framework, as you also want to
provide a so called [negative
test](https://en.wikipedia.org/wiki/Negative_testing). The framework handles
this the following way:

```python
with negative_test():
  expect(that(1).equals(2))
```

### Extending the tests

The testing framework is very bare in nature, and it is recommended that you add
more assumptions that is relevant for you. Here is a short example of extensions:

Here i will provide a short example, given that you have a class:

_person.py_

```python
from dataclasses import dataclass

@dataclass
class Person:
    first_name: str
    last_name: str
    age: int
```

#### Adding more `Assumptions`

Assumptions are the class that lies behind the `that` function. Please create
all these in your module in a files called `assumptions.py` (possibly prepending
context)

```python
class PersonAssumption(BaseAssumption[Person]):
    def is_older_than(self, other_person: Person):
        return self._add_result(
            assuming(self._value.age > other_person.age).else_report(
                f"{self._value} is not older than {other_person}"
            )
        )


def that_person(person: Person):
    return PersonAssumption(person)
```

## Roadmap

- Helpers for Django
- Support function mocking
- Smart way of passing a `lambda x; that(x).something()` into `has_any` etc
