#!/usr/bin/env bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
SCRIPTDIR+="/postmanScripts/"

for file in $SCRIPTDIR/*.json; do
    file="$(basename $file)"
    echo "Executing postman file $file"
    ./test.runner.sh $file
done