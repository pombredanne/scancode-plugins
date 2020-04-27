#!/usr/bin/env bash
# Script to setup the scancode run and dev environment
# for any issue please contact chamohan@amd.com

set -e
set -x
export SCL=`which scl`
cd scancode;source  python3-virtualenv/bin/activate
${SCL} enable devtoolset-7 /bin/bash
