#!/usr/bin/env bash

#
# This script runs dynamic trapdoor tests on the code. It first cleans the working directory (you
# cannot assume it is already clean from previous builds) and then unpacks the compiled binaries
# from the previous buildkite step. Note that if you don't compile anything in a previous step,
# you should remove the download the artifacts portion of this script.
#
# Use this as a template to implement any dynamic tests.
#

## Don't touch this code if you don't understand it ##
if [ "$BUILDKITE_PULL_REQUEST" != "false" ]; then
## END ##

    source ${BASH_SOURCE%/*}/buildkite_common.sh
    get_ancestor  # Writes $ANCESTOR_SHA variable.

    echo "--- Prep working directory"
    rm -rf *_pr.tar.gz *_ancestor.tar.gz
    ./cleanfiles.sh

    echo "--- Running trapdoors tests"
    ${BASH_SOURCE%/*}/check_whitespace.py ${ANCESTOR_SHA} || report_error "Whitespace errors in some commits"

    export PYTHONPATH=$PWD

    echo "--- Unpack PR build from previous step"
    buildkite-agent artifact download calcdb_pr.tar.gz .
    tar xvf calcdb_pr.tar.gz

    echo "--- Running trapdoor tests on PR branch"
    rm -rf ${QAWORKDIR}/*.pp
    ${BASH_SOURCE%/*}/trapdoor_coverage.py --nproc=6 feature
    ${BASH_SOURCE%/*}/trapdoor_namespace.py feature

    echo "--- Unpack ancestor build from previous step"
    git checkout ${ANCESTOR_SHA}
    buildkite-agent artifact download calcdb_ancestor.tar.gz .
    ./cleanfiles.sh
    tar xvf calcdb_ancestor.tar.gz

    echo "--- Running trapdoor tests on ancestor branch"
    copy_qa_scripts

    ${QAWORKDIR}/trapdoor_coverage.py --nproc=6 ancestor
    ${QAWORKDIR}/trapdoor_namespace.py ancestor

    ${QAWORKDIR}/trapdoor_coverage.py report
    ${QAWORKDIR}/trapdoor_namespace.py report

## Don't touch this code if you don't understand it ##
fi
## END ##
