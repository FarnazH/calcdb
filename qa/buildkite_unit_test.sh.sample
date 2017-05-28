#!/usr/bin/env bash

#
# This script runs the basic unit tests.
#
# You likely only need to make minimal changes to the contents of this script. Note that if you
# don't compile anything in a previous step, you should remove the download the artifacts portion
# of this script.
#

source ${BASH_SOURCE%/*}/buildkite_common.sh

echo "--- Prep working directory"
rm -rf *_pr.tar.gz *_ancestor.tar.gz
./cleanfiles.sh

echo "--- Build refatoms"
rm -rf data/refatoms/*.h5 #data/refatoms/*.tar.bz2
make -C data/refatoms/

export PYTHONPATH=$PWD
export HORTONDATA=$PWD/data

echo "--- Unpack PR build from previous step"
buildkite-agent artifact download horton_pr.tar.gz .
tar xvf horton_pr.tar.gz

echo "--- Running Nosetests"
nosetests -v --processes=2 --process-timeout=60 -a slow horton

## Don't touch this code if you don't understand it ##
if [ "$BUILDKITE_PULL_REQUEST" = "false" ]; then
## END ##

  nosetests -v --processes=2 --process-timeout=60 -a "!slow" horton

## Don't touch this code if you don't understand it ##
fi
## END ##
