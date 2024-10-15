#!/bin/bash
set -e 
set -o pipefail
set -u

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RDFDIR="$SCRIPTDIR"/../data/rdf/

cd "$RDFDIR"
rm -f *.gz
rm -f *.gz.*
wget http://atlantides.org/downloads/pleiades/rdf/pleiades-latest.tar.gz
tar -xzf pleiades-latest.tar.gz
rm -f *.gz
rm -f *.gz.*
