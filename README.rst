Duniter Python API
==================

.. image:: https://travis-ci.org/duniter/duniter-python-api.svg
    :target: https://travis-ci.org/duniter/duniter-python-api

.. image:: https://coveralls.io/repos/duniter/duniter-python-api/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/duniter/duniter-python-api?branch=master

Python implementation of `Duniter <https://git.duniter.org/nodes/typescript/duniter>`_ BMA API

Features
--------

 * Supports Duniter's `Basic Merkle API <https://git.duniter.org/nodes/typescript/duniter/blob/master/doc/HTTP_API.md>`_ and `protocol <https://git.duniter.org/nodes/typescript/duniter/blob/master/doc/Protocol.md>`_
 * Asynchronous
 * Duniter signing key

Requirements
------------

 * Python >= 3.5
 * `aiohttp >= 0.19 <https://pypi.python.org/pypi/aiohttp>`_
 * `pylibscrypt <https://pypi.python.org/pypi/pylibscrypt>`_
 * `libnacl <https://pypi.python.org/pypi/libnacl>`_
 * `base58 <https://pypi.python.org/pypi/base58>`_

Installation
------------

You can install duniter-python-api and all its dependencies via the following pip install:

:code:`pip install duniterpy`

Please take a look at the document `HTTP API <https://github.com/duniter/duniter-bma/blob/master/doc/API.md>`_ to learn about the API.

Development
-----------

 * Create a python environment with pyenv
 * Add PYTHONPATH env var to your shell containing the path to this repository
 * Take a look at examples
 * Run examples from parent folder :code:`python example/request_data.py`

Documentation
-------------

 * `HTML Documentation <https://github.com/duniter/duniter-python-api/tree/master/docs/_build/html>`_
 * `Examples <https://github.com/duniter/duniter-python-api/tree/master/examples>`_
