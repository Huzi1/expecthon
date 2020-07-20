#!/usr/bin/env python3

from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="expethon",
    version="0.1.0",
    description="Simple spec testing framework",
    long_description=readme,
    author="Casper Weiss Bang",
    author_email="cwb@svadilfare.dev",
    url="https://github.com/svadilfare/expecthon",
    license=license,
    packages=find_packages(exclude=("tests", "docs")),
)
