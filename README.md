# Duniter Python API

Python implementation for [Duniter](https://git.duniter.org/nodes/typescript/duniter) BMA API

This is the most complete Python library to communicate with Duniter nodes endpoints.

This library is used by two clients:
- [Sakia](http://sakia-wallet.org/), the rich client to manage your Duniter's wallets.
- [Silkaj](https://silkaj.duniter.org/), the command line client.

## Features
- Support Duniter's [Basic Merkle API](https://git.duniter.org/nodes/typescript/duniter/blob/master/doc/HTTP_API.md) and [protocol](https://git.duniter.org/nodes/common/doc/blob/master/rfc/0009_Duniter_Blockchain_Protocol_V11.md)
- Asynchronous/synchronous without threads
- Support HTTP, HTTPS and Web Socket transport for the BMA API
- Support [Elasticsearch Duniter4j](https://git.duniter.org/clients/java/duniter4j/blob/master/src/site/markdown/ES.md#request-the-es-node>) API
- Duniter signing key
- Sign/verify and encrypt/decrypt messages with the Duniter credentials

## Requirements
- Python >= 3.5.3
- [aiohttp >= 3.6.1](https://pypi.org/pypi/aiohttp)
- [pylibscrypt](https://pypi.org/pypi/pylibscrypt)
- [libnacl](https://pypi.org/pypi/libnacl)
- [base58](https://pypi.org/pypi/base58)
- [attr](https://pypi.org/project/attr/)

## Installation
You can install DuniterPy and its dependencies with the following command:
```bash
pip3 install duniterpy --user
```

## Install the development environment
- Install [Poetry](https://poetry.eustace.io):
```bash
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python - --preview
```

## Documentation
Online official automaticaly generated documentation: https://clients.duniter.io/python/duniterpy/index.html

The [examples folder](https://git.duniter.org/clients/python/duniterpy/tree/master/examples) contains scripts to help you!

Please take a look at the document [HTTP API](https://git.duniter.org/nodes/typescript/duniter/blob/master/doc/HTTP_API.md) to learn more about the BMA API.

How to generate and read locally the autodoc:

- Install Sphinx
```bash
poetry install -E sphinx
```

- Generate documentation
```bash
poetry run make docs
```

- The HTML documentation is generated in `docs/_build/html` folder.

## Development
* When writing docstrings, use the reStructuredText format recommended by https://www.python.org/dev/peps/pep-0287/#docstring-significant-features
* Use make commands to check the code and the format.

Black, the formatting tool, requires Python 3.6 or higher.

* Install runtime dependencies
```bash
poetry install --no-dev
```

* Have a look at the examples folder
* Run examples from parent folder
```bash
poetry run python examples/request_data.py
```

* Before submitting a merge requests, please check the static typing and tests.

* Install dev dependencies
```bash
poetry install
```

* Check static typing with [mypy](http://mypy-lang.org/)
```bash
make check
```

* Run all unit tests (builtin `unittest` module) with:
```bash
make tests
```

* Run only some unit tests by passing a special ENV variable:
```bash
make tests TESTS_FILTER=tests.documents.test_block.TestBlock.test_fromraw
```

## Packaging and deploy
### PyPi
Change and commit and tag the new version number (semantic version number)
```bash
./release.sh 0.42.3
```

Build the PyPi package in the `dist` folder
```bash
make build
```

Deploy the package to PyPi test repository (prefix the command with a space in order for the shell not to save in its history system the command containing the password)
```bash
[SPACE]make deploy_test PYPI_TEST_LOGIN=xxxx PYPI_TEST_PASSWORD=xxxx
```

Install the package from PyPi test repository
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.python.org/simple/ duniterpy
```

Deploy the package on the PyPi repository (prefix the command with a space in order for the shell not to save in its history system the command containing the password)
```bash
[SPACE]make deploy PYPI_LOGIN=xxxx PYPI_PASSWORD=xxxx
```

## Packaging status
[![Packaging status](https://repology.org/badge/vertical-allrepos/python:duniterpy.svg)](https://repology.org/project/python:duniterpy/versions)
