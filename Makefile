.PHONY: docs tests check mypy pylint

# generate documentation
docs:
	cd docs && sphinx-apidoc -o . ../duniterpy && make clean && make html && cd ..

# run tests
tests:
	python3 -m unittest ${TESTS_FILTER}

# check
check: mypy pylint

# check static typing
mypy:
	python3 -m mypy duniterpy --ignore-missing-imports

# check code errors
pylint:
	pylint --disable=C --enable=C0121,C0202,C0321 --jobs=0 duniterpy/
