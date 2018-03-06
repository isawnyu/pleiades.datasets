# Pleiades gazetteer datasets

Please report problems and make feature requests via [the main Pleiades Gazetteer Issue Tracker](https://github.com/isawnyu/pleiades-gazetteer/issues/).

[![License: CC BY 3.0](https://licensebuttons.net/l/by/3.0/80x15.png)](https://creativecommons.org/licenses/by/3.0/) Content is governed by the copyrights of the individual contributors responsible for its creation. Some rights are reserved. All content is distributed under the terms of a [Creative Commons Attribution license (cc-by)](https://creativecommons.org/licenses/by/3.0/).

## Overview

This is a package of data derived from the _Pleiades_ gazetteer of ancient places. It is used for archival and redistribution purposes and is likely to be less up-to-date than the live data at https://pleiades.stoa.org.

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

## Credits

Pleiades is brought to you by:

  * Our volunteer content contributors (see html/credits.html).
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

NB: Ryan Baumann has created a script that converts the _Pleiades_ CSV files (q.v.) into GeoJSON files for redistribution, together with a handy JSON index of names. These can be found at https://github.com/ryanfb/pleiades-geojson.

### Hypertext Markup Language (HTML)

__directory: /html/__

Copies of select pages from the site are periodically downloaded into this directory (e.g., the [credits page](https://pleiades.stoa.org/credits)).

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

