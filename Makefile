.PHONY: check check-format mypy pylint format build deploy deploy_test
.SILENT: deploy deploy_test # do not echo commands with password

# check
check: mypy pylint check-format

# check static typing
mypy:
	python3 -m mypy mirage --ignore-missing-imports

# check code errors
pylint:
	pylint --disable=C,R0902,R0903,R0904,R0912,R0913,R0914,R0915,W0613,W0703 --enable=C0121,C0202,C0321 --jobs=0 mirage/

# check format
check-format:
	black --check mirage

# format code
format:
	black mirage

# build a wheel package in build folder and put it in dist folder
build:
	if [ -d "./build" ]; then rm -r build/*; fi
	if [ -d "./dist" ]; then rm -r dist/*; fi
	python3 setup.py sdist bdist_wheel
	twine check dist/*

# upload on PyPi repository
deploy:
	twine upload dist/* --username ${PYPI_LOGIN} --password ${PYPI_PASSWORD}

# upload on PyPi test repository
deploy_test:
	twine upload dist/* --username ${PYPI_TEST_LOGIN} --password ${PYPI_TEST_PASSWORD} --repository-url https://test.pypi.org/legacy/
