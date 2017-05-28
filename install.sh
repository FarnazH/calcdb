#!/usr/bin/env bash

cd ${BASH_SOURCE%/*}

cp .gitignore ../
cp -a pre-commit ../.git/hooks/
cp -a cleanfiles.sh ../