# Pleiades gazetteer datasets

Please report problems and make feature requests via [the main Pleiades Gazetteer Issue Tracker](https://github.com/isawnyu/pleiades-gazetteer/issues/).

[![License: CC BY 3.0](https://licensebuttons.net/l/by/3.0/80x15.png)](https://creativecommons.org/licenses/by/3.0/) Content is governed by the copyrights of the individual contributors responsible for its creation. Some rights are reserved. All content is distributed under the terms of a [Creative Commons Attribution license (cc-by)](https://creativecommons.org/licenses/by/3.0/).

## Version 3.0 - 4 April 2023

What's new since 2.3 (12 October 2020):

- 2,655 new and 10,222 updated place resources (see `data/changelogs/release.html` for details)
- `data/changelogs/`: Monthly changelogs in HTML format since 2009.
- `data/csv/zotero.csv`: The complete bibliographic library cited in references throughout the dataset.
- `data/data_quality`: Some metrics.
- `gis`: CSV files tested in [QGIS](https://www.qgis.org/en/site/) (likely better than the original CSV package for most use cases).

## Overview

This is a package of data derived from the _Pleiades_ gazetteer of ancient places. It is used for archival and redistribution purposes and is likely to be __less up-to-date than the live data at https://pleiades.stoa.org.__

_Pleiades_ is a community-built gazetteer and graph of ancient places. It
publishes authoritative information about ancient places and spaces,
providing unique services for finding, displaying, and reusing that
information under open license. It publishes not just for individual human
users, but also for search engines and for the widening array of
computational research and visualization tools that support humanities
teaching and research.

_Pleiades_ is a continuously published scholarly reference work for the 21st
century. We embrace the new paradigm of citizen humanities, encouraging
contributions from any knowledgeable person and doing so in a context of
pervasive peer review. _Pleiades_ welcomes your contribution, no matter how
small, and we have a number of useful tasks suitable for volunteers of every
interest.

## Access and Archiving

The latest versions of this package can be had by fork or download from the master branch at https://github.com/isawnyu/pleiades-datasets. [Numbered releases](https://github.com/isawnyu/pleiades-datasets/releases) are created periodically at GitHub. These are archived at:

 - zenodo.org using the DOI https://doi.org/10.5281/zenodo.1193921
 - archive.nyu.edu using the URI http://hdl.handle.net/2451/34305

## Credits

Pleiades is brought to you by:

  * Our volunteer content contributors (see rdf/authors.ttl for complete list 
    and associated identifiers).
  * _Pleiades_ has received significant, periodic support from the [National 
    Endowment for the Humanities](https://www.neh.gov) since 2006. Grant numbers: HK-230973-15, 
    PA-51873-06, PX-50003-08, and PW-50557-10. Any views, findings, 
    conclusions, or recommendations expressed in this publication do not 
    necessarily reflect those of the National Endowment for the Humanities.
  * Additional support has been provided since 2000 by the [Ancient World 
    Mapping Center](https://awmc.unc.edu) at the University of North Carolina at Chapel Hill.
  * Development hosting and other project incubation support was provided 
    between 2000 and 2008 by [Ross Scaife](https://en.wikipedia.org/wiki/Ross_Scaife) and the [Stoa Consortium](http://www.stoa.org/).
  * Web hosting and additional support has been provided since 2008 by the 
    [Institute for the Study of the Ancient World](http://isaw.nyu.edu) at New York University.

## Contents

### JavaScript Object Notation (JSON)

__directory: /json/__

The __complete__ serialization of each published object in the _Pleiades_ database (i.e., every place, name, location, and connection resource) is written to [a single, large JSON file](http://atlantides.org/downloads/pleiades/json/) once daily. We periodically download this file and split it up into individual files, one for each place resource (together with its subordinate name, location, and connection resources). 

Each file is named with the final, numeric portion of the place resource's Uniform Resource Identifier (URI), plus the filename extension ".json". So, for example, the URI for the Pleiades place resource describing Roman Heidelberg is https://pleiades.stoa.org/places/118731. The corresponding JSON file in this dataset is named "118731.json". 

In order to avoid performance problems on operating systems that cannot handle large numbers of files in a single directory efficiently, the JSON files are distributed throughout a hierarchical directory structure using each of the first few digits in the base filename as a subdirectory. So, for the Heidelberg example, one would find the JSON file at the relative path ```json/1/1/8/7/118731.json```.

NB: Ryan Baumann has created a script that converts the _Pleiades_ CSV files (q.v.) into GeoJSON files for redistribution, together with a handy JSON index of names. These can be found at https://github.com/ryanfb/pleiades-geojson.

### Comma-Separated Values (CSV)

__directory: /csv/__

Each morning, tables __summarizing__ the published locations, names, and places are written to compressed CSV files at
http://atlantides.org/downloads/pleiades/dumps/. We periodically download these files, decompress them, and incorporate them into this distribution package.

We also periodically export to CSV the contents of [the _Pleiades_ Zotero Library](https://www.zotero.org/groups/2533/pleiades?), which is used for all reference citations in the gazetteer, for incorporation into this package. 

Note the /csv/README.txt file for additional, essential information.


### Resource Description Framework (RDF)

__directory: /rdf/__

The __summary__ data for all places, errata, authors, place types, and time periods
is available for download in Turtle (Terse RDF Triple Language) via
http://atlantides.org/downloads/pleiades/rdf/pleiades-latest.tar.gz. This is a
gzip-compressed, TAR archive. Previous RDF dumps are also available at
http://atlantides.org/downloads/pleiades/rdf/. RDF dumps are updated weekly on
Sundays. We periodically download, decompress, and unarchive these files. 

NB: RDF serializations of data for individual places — in both Turtle and
RDF/XML syntax — can be had from links on the place pages, such as
http://pleiades.stoa.org/places/579885/turtle for Athens, or by a negotiated
request for the resource http://pleiades.stoa.org/places/579885#this. Please
see the README in https://github.com/isawnyu/pleiades-rdf for a description of
the RDF and the vocabularies and ontologies used.

