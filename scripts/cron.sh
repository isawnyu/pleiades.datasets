#! /bin/bash
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>log.out 2>&1
#set -e
set -x

PD_HOME=/home/paregorios/Documents/files/P/pleiades.datasets

# su paregorios
. /home/paregorios/.profile
cd $PD_HOME
git checkout main
./.direnv/python-3.8.3/bin/python scripts/get_json.py
bash ./scripts/get_csv.sh
bash ./scripts/get_ttl.sh
git add data/csv
git commit -m 'updated csv'
git add data/json
git commit -m 'updated json'
git add data/rdf
git commit -m 'updated rdf/ttl'
git push origin main


