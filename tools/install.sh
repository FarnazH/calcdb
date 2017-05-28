#!/usr/bin/env bash

cd ${BASH_SOURCE%/*}

cp .gitignore ../
cp -a pre-commit ../.git/hooks/
mkdir ../qaworkdir
cp -a ./qa/trapdoor.cfg ../qaworkdir
cp -a ./qa/pycodestyle.ini ../qaworkdir
