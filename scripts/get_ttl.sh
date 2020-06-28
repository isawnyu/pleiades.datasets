#!/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RDFDIR="$SCRIPTDIR"/../data/rdf/

cd "$RDFDIR"
wget http://atlantides.org/downloads/pleiades/rdf/pleiades-latest.tar.gz
tar -xzf pleiades-latest.tar.gz
rm *.gz
rm *.gz.?
