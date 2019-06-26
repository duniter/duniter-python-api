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

Documentation
-------------

`Examples <https://git.duniter.org/clients/python/duniterpy/tree/master/examples>`_ folder is full of scripts to help you!

But you can also generate and read the autodoc:

* Install Sphinx::

    pip install -r requirements_dev.txt

* Generate documentation::

    make docs

* HTML Documentation is generated in docs/_build/html folder.

Please take a look at the document `HTTP API <https://git.duniter.org/nodes/typescript/duniter/blob/master/doc/HTTP_API.md>`_
to learn more about the BMA API.

Development
-----------

* When writing docstrings, use the reStructuredText format recommended by https://www.python.org/dev/peps/pep-0287/#docstring-significant-features
* Use make commands to check your code and format it correctly.

.. warning::

    The development tools require Python 3.6.x or higher.

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


Packaging and deploy
--------------------

Pypi
++++

In the development pyenv environment, install the build and deploy tools::

    pip install --upgrade -r requirements_deploy.txt

Change and commit and tag the new version number (semantic version number)::

    ./release.sh 0.42.3

Build the Pypi package in the ``dist`` folder::

    make build

Deploy the package on the Pypi test repository (use a space before make to not keep command with password in shell history)::

    [SPACE]make deploy_test PYPI_TEST_LOGIN=xxxx PYPI_TEST_PASSWORD=xxxx

Install the package from Pypi test repository::

    pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.python.org/simple/ duniterpy

Deploy the package on the Pypi repository (use a space before make to not keep command with password in shell history)::

    [SPACE]make deploy PYPI_LOGIN=xxxx PYPI_PASSWORD=xxxx


