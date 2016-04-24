#duniter-python-api
[![Build Status](https://travis-ci.org/duniter-io/duniter-python-api.svg)](https://travis-ci.org/duniter-io/duniter-python-api) [![Coverage Status](https://coveralls.io/repos/duniter-io/duniter-python-api/badge.svg?branch=master&service=github)](https://coveralls.io/github/duniter-io/duniter-python-api?branch=master)

A python implementation of [duniter](https://github.com/duniter-io/duniter) API

## Features
 * Supports duniter's Basic Merkle Api
 * Asynchronous
 * duniter signing key

## Requirements
 * Python >= 3.5
 * [aiohttp >= 0.19](https://pypi.python.org/pypi/aiohttp "aiohttp")
 * [pylibscrypt](https://pypi.python.org/pypi/pylibscrypt "pylibscrypt")
 * [libnacl](https://pypi.python.org/pypi/libnacl "libnacl")
 * [base58](https://pypi.python.org/pypi/base58 "base58")

##Installation
You can install duniter-python-api and all its dependencies via the following pip install :
`pip install duniterpy`

Please take a look at the document [HTTP API](https://github.com/duniter-io/duniter/blob/master/doc/HTTP_API.md) to learn about the API.
