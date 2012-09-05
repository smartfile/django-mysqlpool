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
2. Instead of cloning the Django mysql backend, we import it.

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

There are a number of additional options that can be configured in settings.py:

 * MYSQLPOOL_MAX - The number of connections allowed in the pool.
 * MYSQLPOOL_OVERFLOW - The number of connections beyond max that can be used
temporarily (burst).
 * MYSQLPOOL_RECYCLE - The time (in seconds) before a connection is reaped.
This value should be less than the configured timeout value in MySQL. Mysql's
default is 120s, so the default recycle interval is 119s.
 * MYSQLPOOL_TIMEOUT - The amount of time to wait for a new connection to
complete before aborting.

.. _SmartFile: http://www.smartfile.com/
.. _Read more: http://www.smartfile.com/open-source.html
