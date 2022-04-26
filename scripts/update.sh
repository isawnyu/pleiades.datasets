#! /usr/local/bin/bash
set -x

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
cd $SCRIPT_DIR/..
PD_HOME=$PWD

nice git checkout main
nice git pull origin main
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/get_json.py -r
nice bash ./scripts/get_csv.sh
nice bash ./scripts/get_ttl.sh
nice git add data/csv
nice git commit -m 'updated csv'
nice git add data/json
nice git commit -m 'updated json'
nice git add data/rdf
nice git commit -m 'updated rdf/ttl'
nice git push origin main


