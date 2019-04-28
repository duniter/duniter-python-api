Duniter Python API
==================

.. image:: https://coveralls.io/repos/duniter/duniter-python-api/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/duniter/duniter-python-api?branch=master

Python implementation of `Duniter <https://git.duniter.org/nodes/typescript/duniter>`_ BMA API

This is the most complete python library to communicate with Duniter nodes endpoints.

This library is used by `Sakia <http://sakia-wallet.org/>`_, the rich client to manage your Duniter's wallets.

Features
--------

* Support Duniter's `Basic Merkle API <https://git.duniter.org/nodes/typescript/duniter/blob/master/doc/HTTP_API.md>`_ and `protocol <https://git.duniter.org/nodes/typescript/duniter/blob/master/doc/Protocol.md>`_
* Asynchronous/synchronous without threads
* Support HTTP, HTTPS and Web Socket transport for BMA API
* Support `Elasticsearch Duniter4j <https://git.duniter.org/clients/java/duniter4j/blob/master/src/site/markdown/ES.md#request-the-es-node>`_ API
* Duniter signing key
* Sign/verify and encrypt/decrypt messages with the Duniter credentials

Requirements
------------

* Python >= 3.5.2
* `aiohttp >= 0.19 <https://pypi.org/pypi/aiohttp>`_
* `pylibscrypt <https://pypi.org/pypi/pylibscrypt>`_
* `libnacl <https://pypi.org/pypi/libnacl>`_
* `base58 <https://pypi.org/pypi/base58>`_
* `attr <https://pypi.org/project/attr/>`_

Installation
------------

You can install duniter-python-api and all its dependencies via the following pip install::

    pip3 install duniterpy

Please take a look at the document `HTTP API <https://git.duniter.org/nodes/typescript/duniter/blob/master/doc/HTTP_API.md>`_ to learn about the API.

Development
-----------

* Create a python virtual environment with `pyenv <https://github.com/pyenv/pyenv>`_ ::

    curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash`

* Install dependencies::

    pip install -r requirements.txt

* Take a look at examples folder
* Run examples from parent folder::

    PYTHONPATH=`pwd` python examples/request_data.py

* Before submit a merge requests, please check the static typing and tests.

* Install dev dependencies::

    pip install -r requirements_dev.txt

* Check static typing with `mypy <http://mypy-lang.org/>`_::

    make check

* Run all unit tests (builtin module unittest) with::

    make tests

* Run only some unit tests by passing a special ENV variable::

    make tests TESTS_FILTER=tests.documents.test_block.TestBlock.test_fromraw

Documentation
-------------

When writing docstrings, use the rst format recommended by https://www.python.org/dev/peps/pep-0287/#docstring-significant-features

* Install Sphinx::

    pip install -r requirements_dev.txt

* Generate documentation::

    make docs

* HTML Documentation is generated in docs/_build/html folder.
* `Examples are more fun than a TLTR doc <https://git.duniter.org/clients/python/duniterpy/tree/master/examples>`_

Packaging and deploy
--------------------

Pypi
++++

In the development pyenv environment, install the following tools::

    pip install --upgrade pip setuptools wheel

    pip install twine

Change the version number (semantic version number)::

    ./release.sh 0.42.3

Build the Pypi package in the ``dist`` folder::

    python setup.py sdist bdist_wheel

Deploy the package on the Pypi repository::

    twine upload dist/*

