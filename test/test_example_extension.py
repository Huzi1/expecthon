import unittest
from dataclasses import dataclass
from datetime import datetime
from typing import List
from expecthon import assuming, expect, negative_test
from expecthon.assumptions import BaseAssumption


@dataclass
class Person:
    first_name: str
    last_name: str
    age: int

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.age} years old)"


class PersonAssumption(BaseAssumption[Person]):
    def is_older_than(self, other_person: Person):
        return self._add_result(
            assuming(self._value.age > other_person.age).else_report(
                f"{self._value} is not older than {other_person}"
            )
        )


def that_person(person: Person):
    return PersonAssumption(person)


class PersonTestCase(unittest.TestCase):
    def test_is_older_than(self):
        bob = Person(first_name="Bob", last_name="Johnson", age=30)
        alice = Person(first_name="Alice", last_name="Tyson", age=25)
        expect(that_person(bob).is_older_than(alice))
