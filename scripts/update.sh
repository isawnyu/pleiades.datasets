#! /usr/local/bin/bash
set -x

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
cd $SCRIPT_DIR/..
PD_HOME=$PWD

git checkout main
git pull origin main
$VIRTUAL_ENV/bin/python $PD_HOME/scripts/get_json.py -r
bash ./scripts/get_csv.sh
bash ./scripts/get_ttl.sh
git add data/csv
git commit -m 'updated csv'
git add data/json
git commit -m 'updated json'
git add data/rdf
git commit -m 'updated rdf/ttl'
git push origin main


