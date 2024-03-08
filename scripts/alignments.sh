#! /usr/local/bin/bash
set -x
set -e

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
cd $SCRIPT_DIR/..
PD_HOME=$PWD

# manto
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z SLCUI2TB -f json > $PD_HOME/data/indexes/manto.json
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z SLCUI2TB -f markdown -g zotkey > $PD_HOME/data/indexes/manto.md

# cfl/ago
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z 9KVQ7A64 -f json > $PD_HOME/data/indexes/cfl_ago.json
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z 9KVQ7A64 -f markdown -g zotkey > $PD_HOME/data/indexes/cfl_ago.md

# topostext
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z MC9RGDVB -f json > $PD_HOME/data/indexes/topostext.json
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z MC9RGDVB -f markdown -g zotkey > $PD_HOME/data/indexes/topostext.md

# aio
# https://www.zotero.org/groups/2533/items/ZPCURT27
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z ZPCURT27 -f json > $PD_HOME/data/indexes/aio.json
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z ZPCURT27 -f markdown -g zotkey > $PD_HOME/data/indexes/aio.md

# wikidata
# https://www.zotero.org/groups/2533/items/BCQIKDKS
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z BCQIKDKS -f json > $PD_HOME/data/indexes/wikidata.json
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z BCQIKDKS -f markdown -g zotkey > $PD_HOME/data/indexes/wikidata.md

# trismegistos
# https://www.zotero.org/groups/2533/items/TN3GJAU8
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z TN3GJAU8 -f json > $PD_HOME/data/indexes/tm.json
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/alignments.py -z TN3GJAU8 -f markdown -g zotkey > $PD_HOME/data/indexes/tm.md
