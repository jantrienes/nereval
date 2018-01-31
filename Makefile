.PHONY: init test test-coverage lint

all: init test test-coverage lint

init:
	pip install -r requirements.txt

test:
	pytest

test-coverage:
	pytest --cov=nereval --cov-report term

lint:
	pylint nereval.py || exit 0

pypi:
	python setup.py sdist bdist_wheel
	twine upload dist/*

pypi-test:
	python setup.py sdist bdist_wheel
	twine upload --repository pypitest dist/*
