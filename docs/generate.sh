#!/usr/bin/env bash

# Infos how-to generate automatically all rst documents for a python package :
# http://stackoverflow.com/questions/4616693/automatically-generating-documentation-for-all-python-package-contents

# generate rst files of all the package
sphinx-apidoc -o . ../duniterpy

# generate HTML
make html
