#! /usr/local/bin/bash
set -x
set -e

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
cd $SCRIPT_DIR/..
PD_HOME=$PWD

# manto
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z SLCUI2TB -f json > $PD_HOME/data/alignments/manto.json
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z SLCUI2TB -f markdown -g zotkey > $PD_HOME/data/alignments/manto.md

# cfl/ago
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z 9KVQ7A64 -f json > $PD_HOME/data/alignments/cfl_ago.json
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z 9KVQ7A64 -f markdown -g zotkey > $PD_HOME/data/alignments/cfl_ago.md


# topostext
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z MC9RGDVB -f json > $PD_HOME/data/alignments/topostext.json
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z MC9RGDVB -f markdown -g zotkey > $PD_HOME/data/alignments/topostext.md


# aio
# https://www.zotero.org/groups/2533/items/ZPCURT27
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z ZPCURT27 -f json > $PD_HOME/data/alignments/aio.json
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z ZPCURT27 -f markdown -g zotkey > $PD_HOME/data/alignments/aio.md


# wikidata
# https://www.zotero.org/groups/2533/items/BCQIKDKS
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z BCQIKDKS -f json > $PD_HOME/data/alignments/wikidata.json
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z BCQIKDKS -f markdown -g zotkey > $PD_HOME/data/alignments/wikidata.md

