#!/bin/bash

source ${BASH_SOURCE%/*}/qa.cfg

echo Cleaning python code in \'`pwd`\' and subdirectories
# split output of find at newlines.
IFS=$'\n'
# send all relevant files to the code cleaner
find ${CODE_DIRS} *.py *.sh | egrep "(\.rst$)|(\.rst.template$)|(README)|(\.bib$)|(\.py$)|(\.c$)|(\.h$)|(\.nwchem)|(\.pyx$)|(\.pxd$)|(\.cpp)|(\.sh)|(\.cfg)|(\.gitignore)|(\.css)" | xargs ${BASH_SOURCE%/*}/codecleaner.py
