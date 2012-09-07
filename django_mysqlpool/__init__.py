from functools import wraps
from django.db import connection


def auto_close_db(f):
    "Ensures the database connection is closed when the function returns."
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        finally:
            connection.close()
    return wrapper
