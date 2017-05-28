#!/usr/bin/env bash

#
# This script compiles the Cython/C++ portion of HORTON and then uploads it for other
# build agents to unpack and use.
#
# You should reimplement this step with your specific build procedure if you have to compile code.
# Do not touch the details within the marked section or you will break buildkite testing for
# your project.
#


## Don't touch this code if you don't understand it ##
source ${BASH_SOURCE%/*}/buildkite_common.sh
get_ancestor  # Writes $ANCESTOR_SHA variable.
## END ##

echo "--- Basic source tests"
${BASH_SOURCE%/*}/check_names.py

echo "--- Build Cython files & HORTON"
./cleanfiles.sh
CC="ccache gcc" ./setup.py build_ext -i

echo "--- Packing build"
find horton -name "*.so" -o -name "*.pyc" | tar -zcvf horton_pr.tar.gz -T -
buildkite-agent artifact upload horton_pr.tar.gz

## Don't touch this code if you don't understand it ##
if [ "$BUILDKITE_PULL_REQUEST" != "false" ]; then
    echo "--- Checkout ancestor"
    git checkout ${ANCESTOR_SHA}
## END ##

    echo "--- Build Cython files & HORTON [Ancestor]"
    ./cleanfiles.sh
    CC="ccache gcc" ./setup.py build_ext -i

    echo "--- Packing build [Ancestor]"
    find horton -name "*.so" -o -name "*.pyc" | tar -zcvf horton_ancestor.tar.gz -T -
    buildkite-agent artifact upload horton_ancestor.tar.gz

## Don't touch this code if you don't understand it ##
fi
## END ##
