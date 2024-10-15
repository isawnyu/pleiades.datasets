#!/bin/bash
set -e 
set -o pipefail
set -u

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CSVDIR="$SCRIPTDIR"/../data/csv/

cd "$CSVDIR"
rm -f *.gz
rm -f *.gz.*
wget http://atlantides.org/downloads/pleiades/dumps/pleiades-places-latest.csv.gz
wget http://atlantides.org/downloads/pleiades/dumps/pleiades-locations-latest.csv.gz
wget http://atlantides.org/downloads/pleiades/dumps/pleiades-names-latest.csv.gz
rm pleiades-*.csv
gunzip *.csv.gz
rm -f *.gz
rm -f *.gz.*
