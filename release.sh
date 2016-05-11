#!/bin/bash

#__version__     = '0.20.1dev9'
current=`grep -P "__version__     = \'\d+.\d+.\d+(\w*)\'" duniterpy/__init__.py | grep -oP "\d+.\d+.\d+(\w*)"`
echo "Current version: $current"

if [[ $1 =~ ^[0-9]+.[0-9]+.[0-9]+[0-9a-z]+$ ]]; then
  sed -i "s/__version__     = '$current'/__version__     = '$1'/g" duniterpy/__init__.py
  git commit duniterpy/__init__.py -m "$1"
  git tag "$1"
else
  echo "Wrong version format"
fi
