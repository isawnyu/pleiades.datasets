#! /usr/local/bin/bash
set -x
set -e 
set -o pipefail
set -u

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
cd $SCRIPT_DIR/..
PD_HOME=$PWD

nice git checkout main
nice git pull origin main
nice $VIRTUAL_ENV/bin/python $PD_HOME/scripts/update_gis.py
nice git add data/gis
nice git commit -m 'updated gis package'
nice git push origin main
rm $HOME/scratch/pleiades_gis_data.zip
nice zip $HOME/scratch/pleiades_gis_data.zip ./data/gis/*.csv ./data/gis/README.md ./data/gis/index.html
# nice scp $HOME/scratch/pleiades_gis_data.zip isaw1:pleiades_gis/
rsync --rsync-path="sudo rsync" --compress --progress --update --times --perms --chmod=Du=rwx,Dg=rx,Do=rx,Fu=rw,Fg=rw,Fo=r --owner --group --chown=www-data:plone_group --partial-dir=.rsync_partial $HOME/scratch/pleiades_gis_data.zip isaw1:/var/www/atlantides.org/downloads/pleiades/gis/
#nice scp $PD_HOME/data/gis/index.html isaw1:pleiades_gis/
rsync --rsync-path="sudo rsync" --compress --progress --update --times --perms --chmod=Du=rwx,Dg=rx,Do=rx,Fu=rw,Fg=rw,Fo=r --owner --group --chown=www-data:plone_group --partial-dir=.rsync_partial $PD_HOME/data/gis/index.html isaw1:/var/www/atlantides.org/downloads/pleiades/gis/
# echo "**** MANUAL STEP: ssh into isaw1, su to plone_daemon, and copy the files in ~/pleiades_gis/ to /var/www/atlantides.org/downloads/pleiades/gis/"

