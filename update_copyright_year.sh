#!/bin/bash

# Script to update the copyright year in header files

NEW_YEAR=`date +"%Y"`
OLD_YEAR=`expr $NEW_YEAR - 1`
find duniterpy tests examples -type f -name "*.py" | \
xargs sed -i "s/Copyright  2014-$OLD_YEAR V/Copyright  2014-$NEW_YEAR V/g"
