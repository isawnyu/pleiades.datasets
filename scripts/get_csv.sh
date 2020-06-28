#!/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CSVDIR="$SCRIPTDIR"/../data/csv/

cd "$CSVDIR"
wget http://atlantides.org/downloads/pleiades/dumps/pleiades-places-latest.csv.gz http://atlantides.org/downloads/pleiades/dumps/pleiades-locations-latest.csv.gz http://atlantides.org/downloads/pleiades/dumps/pleiades-names-latest.csv.gz
rm pleiades-*.csv
gunzip *.csv.gz
