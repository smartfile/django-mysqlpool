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

.. _SmartFile: http://www.smartfile.com/
.. _Read more: http://www.smartfile.com/open-source.html
