#! /usr/local/bin/bash
#
# orchestrate.sh
# manage the entire daily pleiades.datasets generation routine, including error handling

# set/unset shell attributes
set -x # Print a trace of simple commands
set -e # Exit immediately if a pipeline returns a non-zero status
set -o pipefail # The return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status, or zero if all commands in the pipeline exit successfully

# download and archive exports


# check integrity of downloaded json (prerequisite for following steps)

# FORK 1 STARTS HERE
    # BRANCH 1.A 
        # generate and archive GIS package
    # BRANCH 1.B
        # update datasetter pleiades json (alternate local disk representation for some scripts that follow)
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
        
        
    








