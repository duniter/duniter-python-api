.PHONY: docs tests check check-format mypy pylint format build deploy deploy_test
.SILENT: deploy deploy_test # do not echo commands with password

# generate documentation
docs:
	cd docs && rm duniterpy.*; poetry run sphinx-apidoc -o . ../duniterpy && make clean && make html && cd ..

# run tests
tests:
	poetry run python3 -m unittest ${TESTS_FILTER}

# check
check: mypy pylint check-format

# check static typing
mypy:
	 poetry run mypy duniterpy --ignore-missing-imports
	 poetry run mypy tests --ignore-missing-imports
	 poetry run mypy examples --ignore-missing-imports

# check code errors
pylint:
	poetry run pylint --disable=C,R0902,R0903,R0904,R0912,R0913,R0914,R0915,W0613,R0801 --enable=C0121,C0202,C0321 --jobs=0 duniterpy/
	poetry run pylint --disable=C,R0902,R0903,R0904,R0912,R0913,R0914,R0915,W0613,R0801 --enable=C0121,C0202,C0321 --jobs=0 tests/
	poetry run pylint --disable=C,R0902,R0903,R0904,R0912,R0913,R0914,R0915,W0613,E0401,R0801 --enable=C0121,C0202,C0321 --jobs=0 examples/

# check format
check-format:
	black --check duniterpy
	black --check tests
	black --check examples

# format code
format:
	black duniterpy
	black tests
	black examples

# build a wheel package in dist folder
build:
	if [ -d "./dist" ]; then rm -r dist/*; fi
	poetry build

# upload on PyPi repository
deploy:
	poetry publish --build --username ${PYPI_LOGIN} --password ${PYPI_PASSWORD} --repository pypi_test

# upload on PyPi test repository
deploy_test:
	poetry config repositories.pypi_test https://test.pypi.org/legacy/
	poetry publish --build --username ${PYPI_TEST_LOGIN} --password ${PYPI_TEST_PASSWORD} --repository pypi_test
