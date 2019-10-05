#!/usr/bin/env bash

if [ $# -ne 1 ]; then
    echo "usage: test.runner.sh <name of script> e.g. Percolatio.grants.json"
    exit 1
fi

set -x

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
SCRIPTDIR+="/postmanScripts"
SCRIPTNAME=$1
APIURL=${APIURL:-http://127.0.0.1:8000/api}
USERNAME=${USERNAME:-u`date +%s`}
EMAIL=${EMAIL:-$USERNAME@mail.com}
PASSWORD=${PASSWORD:-password}

npx newman run $SCRIPTDIR/$SCRIPTNAME\
  --delay-request 500 \
  --global-var "APIURL=$APIURL" \
  --global-var "USERNAME=$USERNAME" \
  --global-var "EMAIL=$EMAIL" \
  --global-var "PASSWORD=$PASSWORD"
