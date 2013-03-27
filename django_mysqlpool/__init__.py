from functools import wraps

from django_mysqlpool.backends.mysqlpool.base import close_pool


def auto_close_db(f):
    "Ensures the database connection is closed when the function returns."
    from django.db import connection
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        finally:
            connection.close()
    return wrapper
