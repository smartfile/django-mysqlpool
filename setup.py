#!/bin/env python

import os
from distutils.core import setup

name = 'django-mysqlpool'
version = '0.1'
release = '9'
versrel = version + '-' + release
readme = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = file(readme).read()

setup(
    name = name,
    version = versrel,
    description = 'Django database backend for MySQL that provides pooling ala SQLAlchemy.',
    long_description = long_description,
    author = 'Ben Timby',
    author_email = 'btimby@gmail.com',
    maintainer = 'Ben Timby',
    maintainer_email = 'btimby@gmail.com',
    url = 'http://github.com/smartfile/' + name + '/',
    license = 'MIT',
    install_requires = [
        'SQLAlchemy',
    ],
    packages = [
        "django_mysqlpool",
        "django_mysqlpool.backends",
        "django_mysqlpool.backends.mysqlpool",
    ],
    classifiers = (
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
