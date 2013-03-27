test:
	python tests.py

verify:
	pyflakes -x W django_mysqlpool
	pep8 --exclude=migrations --ignore=E501,E225 django_myqlpool

install:
	python setup.py install

publish:
	python setup.py register
	python setup.py sdist upload
