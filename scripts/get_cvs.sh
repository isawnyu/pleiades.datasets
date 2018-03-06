#!/bin/bash

cd ./csv
pwd
wget http://atlantides.org/downloads/pleiades/dumps/pleiades-places-latest.csv.gz http://atlantides.org/downloads/pleiades/dumps/pleiades-locations-latest.csv.gz http://atlantides.org/downloads/pleiades/dumps/pleiades-names-latest.csv.gz
gunzip *.csv.gz
