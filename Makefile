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
