# Duniter Python API
[![Build Status](https://travis-ci.org/duniter/duniter-python-api.svg)](https://travis-ci.org/duniter/duniter-python-api) [![Coverage Status](https://coveralls.io/repos/duniter/duniter-python-api/badge.svg?branch=master&service=github)](https://coveralls.io/github/duniter/duniter-python-api?branch=master)

Python implementation of [Duniter](https://git.duniter.org/nodes/typescript/duniter) BMA API

## Features
 * Supports Duniter's [Basic Merkle API](https://git.duniter.org/nodes/typescript/duniter/blob/master/doc/HTTP_API.md) and [protocol](https://git.duniter.org/nodes/typescript/duniter/blob/master/doc/Protocol.md)
 * Asynchronous
 * duniter signing key

## Requirements
 * Python >= 3.5
 * [aiohttp >= 0.19](https://pypi.python.org/pypi/aiohttp "aiohttp")
 * [pylibscrypt](https://pypi.python.org/pypi/pylibscrypt "pylibscrypt")
 * [libnacl](https://pypi.python.org/pypi/libnacl "libnacl")
 * [base58](https://pypi.python.org/pypi/base58 "base58")

## Installation
You can install duniter-python-api and all its dependencies via the following pip install:
`pip install duniterpy`

Please take a look at the document [HTTP API](https://github.com/duniter/duniter-bma/blob/master/doc/API.md) to learn about the API.

## Development
- Create a python environment with pyenv
- Add PYTHONPATH env var to your shell containing the path to this repository
- Take a look at examples
- Run examples from parent folder `python example/request_data.py`

## Documentation

- [HTML Documentation](https://github.com/duniter/duniter-python-api/tree/master/docs/_build/html)
- [Examples](https://github.com/duniter/duniter-python-api/tree/master/examples)
