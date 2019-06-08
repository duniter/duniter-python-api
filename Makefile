.PHONY: docs tests check check-format mypy pylint format

# generate documentation
docs:
	cd docs && sphinx-apidoc -o . ../duniterpy && make clean && make html && cd ..

# run tests
tests:
	python3 -m unittest ${TESTS_FILTER}

# check
check: mypy pylint check-format

# check static typing
mypy:
	python3 -m mypy duniterpy --ignore-missing-imports

# check code errors
pylint:
	pylint --disable=C,R0913,R0903,R0902,R0914,R0912,R0915,W0613 --enable=C0121,C0202,C0321 --jobs=0 duniterpy/

# check format
check-format:
	black --check duniterpy

# format code
format:
	black duniterpy
