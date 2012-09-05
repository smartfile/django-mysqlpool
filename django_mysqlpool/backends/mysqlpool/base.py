from django.conf import settings
from django.db.backends.mysql import base
from django.db.backends.mysql.client import DatabaseClient
from django.db.backends.mysql.creation import DatabaseCreation
from django.db.backends.mysql.introspection import DatabaseIntrospection
from django.db.backends.mysql.validation import DatabaseValidation
from django.core.exceptions import ImproperlyConfigured

try:
    import sqlalchemy.pool as pool
except ImportError, e:
    raise ImproperlyConfigured("Error loading SQLAlchemy module: %s" % e)


MYSQLPOOL_RECYCLE = 119


DatabaseWrapper = base.DatabaseWrapper


def copy_if_defined(source, skey, dest, dkey, default=None):
    value = getattr(source, skey, None)
    if value is not None:
        dest[dkey] = value
    elif default is not None:
        dest[dkey] = default


class PooledDatabase(object):
    def __init__(self):
        kwargs = {}
        copy_if_defined(settings, 'MYSQLPOOL_RECYCLE', kwargs, 'recycle', RECYCLE_DEFAULT)
        copy_if_defined(settings, 'MYSQLPOOL_MAX', kwargs, 'pool_size')
        copy_if_defined(settings, 'MYSQLPOOL_OVERFLOW', kwargs, 'max_overflow')
        copy_if_defined(settings, 'MYSQLPOOL_TIMEOUT', kwargs, 'timeout')
        self.pool = pool.manage(base.Database, **kwargs)

    def connect(self, **kwargs):
        return self.pool.connect(**kwargs)


# Monkey-patch the regular mysql backend to use a connection pool.
base.Database = PooledDatabase()
