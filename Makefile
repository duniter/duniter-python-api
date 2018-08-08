.PHONY: docs tests check

# generate documentation
docs:
	cd docs && sphinx-apidoc -o . ../duniterpy && make clean && make html && cd ..

# run tests
tests:
	python -m unittest

# check static typing
check:
	mypy duniterpy --ignore-missing-imports
