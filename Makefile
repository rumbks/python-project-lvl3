-include Makefile.local

install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

reinstall: install build
	python3 -m pip install --user dist/*.whl --force-reinstall

lint:
	poetry run flake8 .

tests:
	poetry run pytest -vv tests

.PHONY: tests