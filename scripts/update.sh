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

echo "\n\nDownloading and splitting JSON into individual files\n=================================================\n"
$VIRTUAL_ENV/bin/python $PD_HOME/scripts/get_json.py -r
git add data/json
git commit -m 'updated json'

echo "\n\nDownloading legacy CSV\n=================================================\n"
bash ./scripts/get_csv.sh
git add data/csv/*.csv
git commit -m 'updated csv'

echo "\n\nDownloading RDF/TTL\n=================================================\n"
bash ./scripts/get_ttl.sh
git add data/rdf
git commit -m 'updated rdf/ttl'

echo "\n\nPushing changes to GitHub\n=================================================\n"
git push origin main


