#! /usr/local/bin/bash
set -x
set -e 
set -o pipefail
set -u

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
cd $SCRIPT_DIR/..
PD_HOME=$PWD

git checkout main
git pull origin main

set +x
printf "\n\nDownloading and splitting JSON into individual files\n=====================================================\n"
set -x
$VIRTUAL_ENV/bin/python $PD_HOME/scripts/get_json.py -r
git add data/json
set +e
git commit -m 'updated json'
set -e

set +x
printf "\n\nDownloading legacy CSV\n=====================================================\n"
set -x
bash ./scripts/get_csv.sh
git add data/csv/*.csv
set +e
git commit -m 'updated csv'
set -e

set +x
printf "\n\nDownloading RDF/TTL\n=====================================================\n"
set -x
bash ./scripts/get_ttl.sh
git add data/rdf
set +e
git commit -m 'updated rdf/ttl'
set -e

set +x
printf "\n\nPushing changes to GitHub\n=====================================================\n"
set -x
git push origin main


