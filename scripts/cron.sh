#! /bin/bash
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>log.out 2>&1
set -e
set -x

PD_HOME=/home/paregorios/Documents/files/P/pleiades.datasets

# su paregorios
. /home/paregorios/.profile
cd $PD_HOME
./.direnv/python-3.8.3/bin/python scripts/get_json.py
bash ./scripts/get_csv.sh
bash ./scripts/get_ttl.sh

