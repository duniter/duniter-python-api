#!/bin/bash

#__version__     = '0.20.1dev9'
current=`grep -P "__version__ = \"\d+.\d+.\d+(\w*)\"" mirage/__init__.py | grep -oP "\d+.\d+.\d+(\w*)"`
echo "Current version: $current"

if [[ $1 =~ ^[0-9]+.[0-9]+.[0-9]+[0-9a-z]*$ ]]; then
  # update version in mirage
  sed -i "s/__version__ = \"$current\"/__version__ = \"$1\"/g" mirage/__init__.py
  # update version in setup.py
  sed -i "s/version=\"$current\",/version=\"$1\",/" setup.py

  # commit changes and add version tag
  git commit setup.py mirage/__init__.py -m "$1"
  git tag "$1" -a -m "$1"
else
  echo "Wrong version format"
fi
