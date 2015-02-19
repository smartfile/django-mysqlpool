# -*- coding: utf-8 -*-
"""The top-level package for ``django-mysqlpool``."""
# These imports make 2 act like 3, making it easier on us to switch to PyPy or
# some other VM if we need to for performance reasons.
from __future__ import (absolute_import, print_function, unicode_literals,
                        division)

# Make ``Foo()`` work the same in Python 2 as it does in Python 3.
__metaclass__ = type


from functools import wraps


__version__ = "0.2.1"


def auto_close_db(f):
    "Ensures the database connection is closed when the function returns."
    from django.db import connections
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        finally:
            for connection in connections.all():
                connection.close()
    return wrapper
