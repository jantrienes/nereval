.PHONY: init test test-coverage lint

all: init test test-coverage lint

init:
	pipenv install

test:
	pipenv run pytest

test-coverage:
	pipenv run pytest --cov=nereval --cov-report term

lint:
	pylint nereval.py || exit 0

pypi:
	rm -fr dist/
	pipenv run python setup.py sdist bdist_wheel
	twine upload dist/*

pypi-test:
	rm -fr dist/
	pipenv run python setup.py sdist bdist_wheel
	twine upload --repository pypitest dist/*
