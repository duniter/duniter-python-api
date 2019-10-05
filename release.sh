#!/bin/bash

#__version__     = '0.20.1dev9'
current=`grep -P "__version__ = \"\d+.\d+.\d+(\w*)\"" duniterpy/__init__.py | grep -oP "\d+.\d+.\d+(\w*)"`
echo "Current version: $current"

if [[ $1 =~ ^[0-9]+.[0-9]+.[0-9]+[0-9a-z]*$ ]]; then
  # update version in duniterpy
  sed -i "s/__version__ = \"$current\"/__version__ = \"$1\"/g" duniterpy/__init__.py
  # update version in pyproject.toml
  poetry version "$1"
  # update version in documentation configuration
  sed -i "s/version = '$current'/version = '$1'/g" docs/conf.py
  sed -i "s/release = '$current'/release = '$1'/g" docs/conf.py
  # commit changes and add version tag
  git commit pyproject.toml duniterpy/__init__.py docs/conf.py -m "$1"
  git tag "$1" -a -m "$1"
else
  echo "Wrong version format"
fi
