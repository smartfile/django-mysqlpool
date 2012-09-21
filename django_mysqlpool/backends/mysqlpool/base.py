from UserDict import UserDict
from django.conf import settings
from django.db.backends.mysql import base
from django.core.exceptions import ImproperlyConfigured

try:
    import sqlalchemy.pool as pool
except ImportError, e:
    raise ImproperlyConfigured("Error loading SQLAlchemy module: %s" % e)


# Global variable to hold the actual connection pool.
MYSQLPOOL = None
# Default pool type (QueuePool, SingletonThreadPool, AssertionPool, NullPool, StaticPool).
MYSQLPOOL_BACKEND = 'QueuePool'
# Needs to be less than MySQL connection timeout (server setting). The default is 120,
# so default to 119.
MYSQLPOOL_TIMEOUT = 119

def isiterable(value):
    "Checks if the provided value is iterable."
    try:
        iter(value)
        return True
    except TypeError:
        return False


class OldDatabaseProxy(object):
    """Saves a reference to the old connect function. Proxies calls to it's
    own connect() method to the old function."""
    def __init__(self, old_connect):
        self.old_connect = old_connect

    def connect(self, **kwargs):
        # Bounce the call to the old function.
        return self.old_connect(**kwargs)


class HashableDict(UserDict):
    """A dictionary that is hashable. This is not generally useful, but created
    specifically to hold the "conv" parameter that needs to be passed to MySQLdb."""
    def __hash__(self):
        items = sorted(self.items())
        items = [(n, tuple(v)) for n, v in items if isiterable(v)]
        return hash(tuple(items))


# Define this here so Django can import it.
DatabaseWrapper = base.DatabaseWrapper

# Wrap the old connect() function so our pool can call it.
OldDatabase = OldDatabaseProxy(base.Database.connect)


def get_pool():
    "Creates one and only one pool using the configured settings."
    global MYSQLPOOL
    if MYSQLPOOL is None:
        backend = getattr(settings, 'MYSQLPOOL_BACKEND', MYSQLPOOL_BACKEND)
        backend = getattr(pool, backend)
        kwargs = getattr(settings, 'MYSQLPOOL_ARGUMENTS', {})
        kwargs.setdefault('poolclass', backend)
        # The user can override this, but set it by default for safety.
        kwargs.setdefault('recycle', MYSQLPOOL_TIMEOUT)
        MYSQLPOOL = pool.manage(OldDatabase, **kwargs)
    return MYSQLPOOL


def connect(**kwargs):
    "Obtains a database connection from the connection pool."
    conv = kwargs.pop('conv', None)
    if conv:
        # SQLAlchemy serializes the parameters to keep unique connection parameter
        # groups in their own pool. We need to store conv in a manner that is
        # compatible with their serialization.
        kwargs['conv'] = HashableDict(conv)
    # Open the connection via the pool.
    return get_pool().connect(**kwargs)


# Monkey-patch the regular mysql backend to use our hacked-up connect() function.
base.Database.connect = connect
