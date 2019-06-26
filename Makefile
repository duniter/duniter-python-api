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
	python3 -m mypy tests --ignore-missing-imports
	python3 -m mypy examples --ignore-missing-imports

# check code errors
pylint:
	pylint --disable=C,R0902,R0903,R0904,R0912,R0913,R0914,R0915,W0613 --enable=C0121,C0202,C0321 --jobs=0 duniterpy/
	pylint --disable=C,R0902,R0903,R0904,R0912,R0913,R0914,R0915,W0613 --enable=C0121,C0202,C0321 --jobs=0 tests/
	pylint --disable=C,R0902,R0903,R0904,R0912,R0913,R0914,R0915,W0613 --enable=C0121,C0202,C0321 --jobs=0 examples/

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

# build a wheel package in build folder and put it in dist folder
build:
	if [ -d "./build" ]; then rm -r build/*; fi
	if [ -d "./dist" ]; then rm -r dist/*; fi
	python setup.py sdist bdist_wheel