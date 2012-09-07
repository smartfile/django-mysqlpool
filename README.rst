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

Connection Closing
------------------

While this has nothing to do directly with connection pooling, it is tangentially
related. Once you start pooling (and limiting) the database connections it
becomes important to close them.

This project was originally created because our FTP server (written in Python
and using Django for database interaction) was exhausting all of our database
connections. The idea was that pooling would be more efficient, and also
enforce a connection limit for each FTP process.

Once deployed, we quickly exhausted the per-process limit. This was actually a
big success for us, as it mean the FTP server stopped functioning, without impacting
any other database clients. Investigating, we found that Django only closes database
connections when it is done handling a request. Since our FTP server did not follow
the normal request processing pipeline, we needed to close our connections proactively
(thus returning them to the pool as soon as possible). Below is a very good
description of the problem we faced.

http://stackoverflow.com/questions/1303654/threaded-django-task-doesnt-automatically-handle-transactions-or-db-connections

A decorator was created for wrapping any function that used the Django ORM,
automatically closing the connection. You can use it as follows::

    from django_mysqlpool import auto_close_db

    @auto_close_db
    def function_that_uses_db():
        MyModel.objects.all().delete()

With pooling, closing the connection early and often is the key to good performance.
Closing returns the connection to the pool to be reused, thus the total number of
connections is decreased.

.. _SmartFile: http://www.smartfile.com/
.. _Read more: http://www.smartfile.com/open-source.html
