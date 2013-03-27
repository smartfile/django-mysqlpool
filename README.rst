A `SmartFile`_ Open Source project. `Read more`_ about how SmartFile
uses and contributes to Open Source software.

.. figure:: http://www.smartfile.com/images/logo.jpg
   :alt: SmartFile

Introduction
------------

This is a simple Django database backend that pools MySQL connections. This
backend is based on a blog post by Ed Menendez.

http://menendez.com/blog/mysql-connection-pooling-django-and-sqlalchemy/

The main differences being:

1. The work is done for you.
2. Instead of cloning the Django mysql backend, we monkey-patch it.

The second point sounds bad, but it is the best option because it does not
freeze the Django MySQL backend at a specific revision. Using this method
allows us to benefit from any bugs that the Django project fixes, while
layering on connection pooling.

The actual pooling is done using SQLAlchemy. While imperfect (this backend
is per-process only) it has usefulness. The main problem it solves for us
is that it restricts a process to a certain number of total connections.

Usage
-----

Configure this backend instead of the default Django mysql backend.

::

    DATABASES = {
        'default': {
            'ENGINE': 'django_mysqlpool.backends.mysqlpool',
            'NAME': 'db_name',
            'USER': 'username',
            'PASSWORD': 'password',
            'HOST': '',
            'PORT': '',
        },
    }

Configuration
-------------

You can define the pool implementation and the specific arguments passed to it.
The available implementations (backends) and their arguments are defined within
the SQLAlchemy documentation.

http://docs.sqlalchemy.org/en/rel_0_7/core/pooling.html

 * MYSQLPOOL_BACKEND - The pool implementation name ('QueuePool' by default).
 * MYSQLPOOL_ARGUMENTS - The kwargs passed to the pool.

For example, to use a QueuePool without threadlocal, you could use the following
configuration::

    MYSQLPOOL_BACKEND = 'QueuePool'
    MYSQLPOOL_ARGUMENTS = {
        'use_threadlocal': False,
    }

Connection Closing
------------------

While this has nothing to do directly with connection pooling, it is tangentially
related. Once you start pooling (and limiting) the database connections it
becomes important to close them.

This is really only relevant when you are dealing with a threaded application. Such
was the case for one of our servers. It would create many threads for handling
conncurrent operations. Each thread resulted in a connection to the database being
opened persistently. Once we deployed connection pooling, this service quickly
exhausted the connection limit of it's pool.

This sounds like a huge failure, but for us it was a great success. The reason is
that we implemented pooling specifically to limit each process to a certain
number of connections. This prevents any given process from impacting other
services, turning a global issue into a local issue. Once we were able to identify
the specific service that was abusing our MySQL server, we were able to fix it.

The problem we were having with this threaded server is very well described below.

http://stackoverflow.com/questions/1303654/threaded-django-task-doesnt-automatically-handle-transactions-or-db-connections

Therefore, this library provides a decorator that can be used in a similar situation
to help with connection management. You can use it like so::

    from django_mysqlpool import auto_close_db

    @auto_close_db
    def function_that_uses_db():
        MyModel.objects.all().delete()

With pooling (and threads), closing the connection early and often is the key to good
performance. Closing returns the connection to the pool to be reused, thus the total
number of connections is decreased. We also needed to disable the `use_threadlocal`
option of the QueuePool, so that multiple threads could share the same connection.
Once we decorated all functions that utilized a connection, this service used less
connections than it's total thread count.

Forking
-------

If you are using mysqlpool with a daemon (our project uses Django admin commands to
build daemons) then you need to take care with the connection pool. After a fork()
the pool will be unusable. In our case, the file descriptors for the connections
were closed, and in the child, any new connections or files assumed the fd of the
MySQL connection this caused the Django ORM to read/write on some non-MySQL
connection in our case, Redis, so Django would send SQL to redis an expect a
reply! The solution is to close the pool before fork()ing. This will release the
pooled connections which will be reopened when the child first attempts to use
them.

    from django_mysqlpool import close_pool

    close_pool()
    pid = os.fork()


.. _SmartFile: http://www.smartfile.com/
.. _Read more: http://www.smartfile.com/open-source.html
