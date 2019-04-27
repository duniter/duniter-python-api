.PHONY: docs tests check

# generate documentation
docs:
	cd docs && sphinx-apidoc -o . ../duniterpy && make clean && make html && cd ..

# run tests
tests:
	python3 -m unittest

# check static typing
check:
	python3 -m mypy duniterpy --ignore-missing-imports
