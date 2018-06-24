Duniter Python API
==================

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

* Create a python environment with `pyenv <https://github.com/pyenv/pyenv>`_ ::

    curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash`

* Add PYTHONPATH env var to your shell containing the path to this repository
* Run unit tests with ::

    python -m unittest

* Take a look at examples folder
* Run examples from parent folder ::

    python examples/request_data.py

Documentation
-------------

* `HTML Documentation <https://git.duniter.org/clients/python/duniterpy/tree/master/docs/_build/html>`_
* `Examples <https://git.duniter.org/clients/python/duniterpy/tree/master/examples>`_

Packaging and deploy
--------------------

Pypi
++++

*The README file must be in RestructuredText format (README.rst) for the long description field of the package.*

In the development pyenv environment, install the following tools::

    pip install --upgrade pip setuptools wheel

    pip install twine

Change the version number (semantic version number)::

    ./release.sh 0.42.3

Build the Pypi package in the ``dist`` folder::

    python setup.py sdist bdist_wheel

Deploy the package on the Pypi repository::

    twine upload dist/*

