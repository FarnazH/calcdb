#!/usr/bin/env bash

#
# This file installs the python project into a prefix'd directory. This can be useful for testing
# certain aspects of the setup.py file. It forms part of a larger continuous integration framework
# for testing code releases.
#
# Reimplement as needed.
#

source ${BASH_SOURCE%/*}/buildkite_common.sh

echo "--- Basic source tests"
${BASH_SOURCE%/*}/check_names.py

echo "--- Build"
./cleanfiles.sh
rm -rf installation
./setup.py install --prefix=$PWD/installation

echo "--- Running Nosetests"
cd installation
PATH=$PATH:$PWD/bin PYTHONPATH=$PWD/lib/python2.7/site-packages:$PWD/lib64/python2.7/site-packages nosetests -v --processes=2 --process-timeout=60 -a slow calcdb

## Don't touch this code if you don't understand it ##
if [ "$BUILDKITE_PULL_REQUEST" = "false" ]; then
## END ##

  PATH=$PATH:$PWD/bin PYTHONPATH=$PWD/lib/python2.7/site-packages:$PWD/lib64/python2.7/site-packages nosetests -v --processes=2 --process-timeout=60 -a "!slow" calcdb

## Don't touch this code if you don't understand it ##
fi
## END ##
