#!/bin/bash

#__version__     = '0.20.1dev9'
current=`grep -P "version=\"\d+.\d+.\d+(\w*)\"" setup.py | grep -oP "\d+.\d+.\d+(\w*)"`
echo "Current version: $current"

if [[ $1 =~ ^[0-9]+.[0-9]+.[0-9]+[0-9a-z]*$ ]]; then
  sed -i "s/version=\"$current\"/version=\"$1\"/g" setup.py
  git commit setup.py -m "$1"
  git tag "$1" -a -m "$1"
else
  echo "Wrong version format"
fi
