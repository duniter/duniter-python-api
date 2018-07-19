.PHONY: docs tests

# generate documentation
docs:
	cd docs && sphinx-apidoc -o . ../duniterpy && make html && cd ..

# run tests
tests:
	python -m unittest

