#! /usr/local/bin/bash
#
# orchestrate.sh
# manage the entire daily pleiades.datasets generation routine, including error handling

# set/unset shell attributes and other config
set -x # Print a trace of simple commands
set -e # Exit immediately if a pipeline returns a non-zero status
set -o pipefail # The return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status, or zero if all commands in the pipeline exit successfully
set -u

set +x
SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
cd $SCRIPT_DIR/..
PD_HOME=$PWD
echo "Config:"
echo "PD_HOME: $PD_HOME"
echo "VIRTUAL_ENV: $VIRTUAL_ENV"

# ensure clean and up-to-date git working copy
printf "\n\nEnsuring git working copy is up-to-date and does not have unsaved changes\n=====================================================\n"
set -x
git checkout main
git pull origin main

# download and archive exports
set +x
printf "\n\nDownloading and splitting JSON into individual files\n=====================================================\n"
set -x
$VIRTUAL_ENV/bin/python $PD_HOME/scripts/get_json.py -r

# check integrity of downloaded json (prerequisite for following steps)
set +x
printf "\n\nChecking integrity of downloaded data (have there been retractions?)\n=====================================================\n"
set -x
$VIRTUAL_ENV/bin/python $PD_HOME/scripts/check_integrity.py

# commit updated json to git and pushing to github
set +x
printf "\n\nAdding and committing new/changed JSON to git\n=====================================================\n"
set -x
git add data/json
set +e
git commit -m 'updated json'
set -e
git push origin main

# download and archive rdf/ttl
set +x
printf "\n\nDownloading RDF/TTL and committing to git and pushing to github\n=====================================================\n"
set -x
bash ./scripts/get_ttl.sh
git add data/rdf
set +e
git commit -m 'updated rdf/ttl'
set -e
git push origin main


# FORK 1 STARTS HERE
    # BRANCH 1.A 
        # generate and archive GIS package
        set +x
        printf "\n\Generating GIS package, committing to git, pushing to github, and syncing a zipped copy to the Pleiades server\n=====================================================\n"
        set -x
        $VIRTUAL_ENV/bin/python $PD_HOME/scripts/update_gis.py
        git add data/gis
        set +e
        git commit -m 'updated gis package'
        set -e
        git push origin main
        rm $HOME/scratch/pleiades_gis_data.zip
        zip $HOME/scratch/pleiades_gis_data.zip ./data/gis/*.csv ./data/gis/README.md ./data/gis/index.html
        rsync --rsync-path="sudo rsync" --compress --progress --update --times --perms --chmod=Du=rwx,Dg=rx,Do=rx,Fu=rw,Fg=rw,Fo=r --owner --group --chown=www-data:plone_group --partial-dir=.rsync_partial $HOME/scratch/pleiades_gis_data.zip isaw1:/var/www/atlantides.org/downloads/pleiades/gis/
        rsync --rsync-path="sudo rsync" --compress --progress --update --times --perms --chmod=Du=rwx,Dg=rx,Do=rx,Fu=rw,Fg=rw,Fo=r --owner --group --chown=www-data:plone_group --partial-dir=.rsync_partial $PD_HOME/data/gis/index.html isaw1:/var/www/atlantides.org/downloads/pleiades/gis/

    # BRANCH 1.B
        # update datasetter pleiades json (alternate local disk representation for some scripts that follow)
        set +x
        printf "\n\Updating the datasetter pleiades JSON\n=====================================================\n"
        set -x
        cd ../../D/datasetter
        set +x
        echo "PD_HOME: $PD_HOME"
        echo "VIRTUAL_ENV: $VIRTUAL_ENV"
        set -x


    # BRANCH 1.C
        # fetch latest Wikidata dump
    # BRANCH 1.D
        # fetch latest sidebar prerequisites
# FORK 1 ENDS HERE

# check exit status codes from both branches before proceeding

# FORK 2 STARTS HERE
    # BRANCH 2.A
        # pleiades wayback
    # BRANCH 2.B
        # generate and commit pleiades geojson
        # update bibliography
            # update datasetter pzot json
            # generate short titles json
            # export CSV from Zotero
            # generate keys/pids crosswalk index
            # add/commit to git
        # update indexes (yes, this is dependent on bib and pleiades geojson)
            # copy names index from pleiades geojson
            # generate other alignments
            # commit to git
        # update pleiades wikidata
        # update sidebar
# FORK 2 ENDS HERE

# generate and post reports to web
        
        
    








