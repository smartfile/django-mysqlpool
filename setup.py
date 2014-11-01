#!/bin/env python
# -*- coding: utf-8 -*-
"""The setup script for ``django_mysqlpool``."""
# These imports make 2 act like 3, making it easier on us to switch to PyPy or
# some other VM if we need to for performance reasons.
from __future__ import (absolute_import, print_function, unicode_literals,
                        division)

# Make ``Foo()`` work the same in Python 2 as it does in Python 3.
__metaclass__ = type


import re
from setuptools import setup, find_packages


REQUIRES = [
    "sqlalchemy >=0.7, <1.0",
]


def find_version(fname):
    """Attempt to find the version number in the file names fname.

    Raises ``RuntimeError`` if not found.
    """
    version = ""
    with open(fname, "r") as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError("Cannot find version information")
    return version


__version__ = find_version("django_mysqlpool/__init__.py")


def read(fname):
    """Return the contents of the file-like ``fname``."""
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name="django-mysqlpool",
    version=__version__,
    description="Django database backend for MySQL that provides pooling ala SQLAlchemy.",  # noqa
    long_description=read("README.rst"),
    author=["Ben Timby", "Hank Gay"],
    author_email=["btimby@gmail.com", "hank@rescuetime.com"],
    maintainer=["Ben Timby", "Hank Gay"],
    maintainer_email=["btimby@gmail.com", "hank@rescuetime.com"],
    url="https://github.com/gthank/django-mysqlpool",
    install_requires=REQUIRES,
    license=read("LICENSE"),
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
    packages=find_packages(),
)
