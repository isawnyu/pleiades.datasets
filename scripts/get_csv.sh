#!/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CSVDIR="$SCRIPTDIR"/../csv/

cd "$CSVDIR"
wget http://atlantides.org/downloads/pleiades/dumps/pleiades-places-latest.csv.gz http://atlantides.org/downloads/pleiades/dumps/pleiades-locations-latest.csv.gz http://atlantides.org/downloads/pleiades/dumps/pleiades-names-latest.csv.gz
rm *.csv
gunzip *.csv.gz
