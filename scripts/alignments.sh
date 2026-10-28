#! /usr/local/bin/bash
set -x
set -e

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
cd $SCRIPT_DIR/..
PD_HOME=$PWD
PYDIR=$PD_HOME/.direnv/python-3.15

# manto
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z SLCUI2TB -f json > $PD_HOME/data/indexes/manto.json
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z SLCUI2TB -f markdown -g zotkey > $PD_HOME/data/indexes/manto.md

# cfl/ago
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z 9KVQ7A64 -f json > $PD_HOME/data/indexes/cfl_ago.json
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z 9KVQ7A64 -f markdown -g zotkey > $PD_HOME/data/indexes/cfl_ago.md

# topostext
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z MC9RGDVB -f json > $PD_HOME/data/indexes/topostext.json
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z MC9RGDVB -f markdown -g zotkey > $PD_HOME/data/indexes/topostext.md

# aio
# https://www.zotero.org/groups/2533/items/ZPCURT27
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z ZPCURT27 -f json > $PD_HOME/data/indexes/aio.json
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z ZPCURT27 -f markdown -g zotkey > $PD_HOME/data/indexes/aio.md

# wikidata
# https://www.zotero.org/groups/2533/items/BCQIKDKS
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z BCQIKDKS -f json > $PD_HOME/data/indexes/wikidata.json
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z BCQIKDKS -f markdown -g zotkey > $PD_HOME/data/indexes/wikidata.md

# trismegistos
# https://www.zotero.org/groups/2533/items/TN3GJAU8
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z TN3GJAU8 -f json > $PD_HOME/data/indexes/tm.json
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z TN3GJAU8 -f markdown -g zotkey > $PD_HOME/data/indexes/tm.md

# Paus. (Spiro: Perseus)
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z GTGBFEI9 -f json > $PD_HOME/data/indexes/paus-spiro-perseus.json
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z GTGBFEI9 -f markdown -g zotkey > $PD_HOME/data/indexes/paus-spiro-perseus.md

# TP (Talbert: CUP)
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z QT8GLGGI -f json > $PD_HOME/data/indexes/tp-talbert-cup.json
$PYDIR/bin/python $PD_HOME/scripts/alignments.py -z QT8GLGGI -f markdown -g zotkey > $PD_HOME/data/indexes/tp-talbert-cup.md

