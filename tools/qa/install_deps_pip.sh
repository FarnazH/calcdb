#!/usr/bin/env bash

source ${BASH_SOURCE%/*}/common.sh

# This script assumes that a virtualenv is created, in which pip will then automatically
# install the dependencies.

# All packages are first wheeled, i.e. a binary package is made, which can be cached.

# Pip is called multiple times to have more regular output, which keeps travis happy.

pip install --upgrade pip
pip install wheel
mkdir -p ${PIP_WHEEL_DIR}

# Packages for testing
pip wheel nose
pip install --no-index --upgrade nose
pip wheel pycodestyle
pip install --no-index --upgrade pycodestyle
pip wheel pylint
pip install --no-index --upgrade pylint
pip wheel coverage
pip install --no-index --upgrade coverage
pip wheel pydocstyle
pip install --no-index --upgrade pydocstyle
pip wheel GitPython
pip install --no-index --upgrade GitPython

# Packages for calcdb documentation
pip wheel sphinx
pip install --no-index --upgrade sphinx
pip wheel sphinx_rtd_theme
pip install --no-index --upgrade sphinx_rtd_theme
pip wheel breathe
pip install --no-index --upgrade breathe

# Remove old wheels
${BASH_SOURCE%/*}/remove_old_wheels.py
