.PHONY: init test test-coverage lint

all: init test test-coverage lint

init:
	pip install -r requirements.txt

test:
	pytest

test-coverage:
	pytest --cov=muceval --cov-report term

lint:
	pylint muceval.py || exit 0
