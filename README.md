# _Pleiades_ gazetteer datasets

Please report problems and make feature requests via [the main _Pleiades_ Gazetteer Issue Tracker](https://github.com/isawnyu/pleiades-gazetteer/issues/).

[![License: CC BY 3.0](https://licensebuttons.net/l/by/3.0/80x15.png)](https://creativecommons.org/licenses/by/3.0/) Content is governed by the copyrights of the individual contributors responsible for its creation. Some rights are reserved. All content is distributed under the terms of a [Creative Commons Attribution license (cc-by)](https://creativecommons.org/licenses/by/3.0/).

We encourage use and citation of numbered releases for scholarly work that will be published in static form.

__Please share notices of data reuse with the _Pleiades_ community via email to pleiades.admin@nyu.edu. These reports help us to justify continued funding and operation of the gazetteer and to prioritize updates and improvements.__

## Version 3.2 - 3 November 2023

40,418 place resources

What's new since 3.1 (1 August 2023):

- 108 new and 1,629 updated place resources reflecting work by Erin Walcek Averett, Jeffrey Becker, Catherine Bouras, Anne Chen, Niels Christoffersen, Peter Cobb, Tom Elliott, Jonathan Fu, Greta Hawes, Carolin Johansson, Noah Kaye, Brady Kiesling, Thomas Landvatter, Stanisław Ludwiński, Ingrid Luo, Stephan Maurer, Colin McCaffrey, Gabriel McKee, David Meadows, Gabriel Moss, John Muccigrosso, Gifford Quinn, Rune Rattenborg, Enrico Regazzoni, Rosemary Selth, R. Scott Smith, Richard Talbert, Georgios Tsolakis, and Scott Vanderbilt (see `data/changelogs/release.html` for details).
- Included experimental JSON index of links extracted from _Pleiades_ place resources to "toponym" entries in Veronique Chankowski et al. [_Chronique Des Fouilles En Ligne = Archaeology in Greece Online._](https://chronique.efa.gr/?kroute=homepage) Athens: Ecole française d’Athènes and British School at Athens, 2018, together with links to the associated _Chronique_ archaeological reports. See `data/indexes/pids2chronique.json`.



## Overview

This is a package of data derived from the _Pleiades_ gazetteer of ancient places. It is used for archival and redistribution purposes and is likely to be __less up-to-date than the live data at https://pleiades.stoa.org.__

_Pleiades_ is a community-built gazetteer and graph of ancient places. It publishes authoritative information about ancient places and spaces, providing unique services for finding, displaying, and reusing that information under open license. It publishes not just for individual human users, but also for search engines and for the widening array of computational research and visualization tools that support humanities teaching and research.

_Pleiades_ is a continuously published scholarly reference work for the 21st century. We embrace the new paradigm of citizen humanities, encouraging contributions from any knowledgeable person and doing so in a context of pervasive peer review. _Pleiades_ welcomes your contribution, no matter how small, and we have a number of useful tasks suitable for volunteers of every interest.

## Access and Archiving

The latest versions of this package can be had by fork or download from the `main` branch at https://github.com/isawnyu/pleiades-datasets. [Numbered releases](https://github.com/isawnyu/pleiades-datasets/releases) are created periodically at GitHub. These are archived at:

 - zenodo.org using the DOI [10.5281/zenodo.1193921](https://doi.org/10.5281/zenodo.10070421)
 - archive.nyu.edu using the Handle [2451/69536](https://hdl.handle.net/2451/69872)
 - archive.org using the URI https://archive.org/details/pleiades.datasets-3.2

## Credits

_Pleiades_ is brought to you by:

  * Our volunteer content contributors (see `data/rdf/authors.ttl` for complete list and associated identifiers or data).
  * _Pleiades_ has received significant, periodic support from the [National Endowment for the Humanities](https://www.neh.gov) since 2006. Grant numbers: HK-230973-15, PA-51873-06, PX-50003-08, and PW-50557-10. Any views, findings, conclusions, or recommendations expressed in this publication do not necessarily reflect those of the National Endowment for the Humanities. 
  * Additional support has been provided since 2000 by the [Ancient World Mapping Center](https://awmc.unc.edu) at the University of North Carolina at Chapel Hill. * Development hosting and other project incubation support was provided between 2000 and 2008 by [Ross Scaife](https://en.wikipedia.org/wiki/Ross_Scaife) and the [Stoa Consortium](https://www.stoa.org/).
  * Web hosting and additional support has been provided since 2008 by the [Institute for the Study of the Ancient World](https://isaw.nyu.edu) at New York University.

## Contents

### JavaScript Object Notation (JSON)

__directory: /data/json/__

The __complete__ serialization of each published object in the _Pleiades_ database (i.e., every place, name, location, and connection resource) is written to [a single, large JSON file](http://atlantides.org/downloads/pleiades/json/) once daily. We periodically download this file and split it up into individual files, one for each place resource (together with its subordinate name, location, and connection resources). 

Each file is named with the final, numeric portion of the place resource's Uniform Resource Identifier (URI), plus the filename extension ".json". So, for example, the URI for the _Pleiades_ place resource describing Roman Heidelberg is https://pleiades.stoa.org/places/118731. The corresponding JSON file in this dataset is named "118731.json". 

In order to avoid performance problems on operating systems that cannot handle large numbers of files in a single directory efficiently, the JSON files are distributed throughout a hierarchical directory structure using each of the first few digits in the base filename as a subdirectory. So, for the Heidelberg example, one would find the JSON file at the relative path `data/json/1/1/8/7/118731.json`.

NB: Ryan Baumann has created a script that converts the _Pleiades_ CSV files (q.v.) into GeoJSON files for redistribution, together with a handy JSON index of names. These can be found at https://github.com/ryanfb/pleiades-geojson.

### GIS Package (in CSV format)

__directory: /data/gis/__

A collection of CSV files derived from data in the _Pleiades_ gazetteer of ancient places. This collection is intended to facilitate use of _Pleiades_ data in geographic information systems software. Files have been tested for use in QGIS. See further `data/gis/README.md`.

### Resource Description Framework (RDF)

__directory: /data/rdf/__

The __summary__ data for all places, errata, authors, place types, and time periods is available for download in Turtle (Terse RDF Triple Language) via http://atlantides.org/downloads/pleiades/rdf/pleiades-latest.tar.gz. This is a gzip-compressed, TAR archive. Previous RDF dumps are also available at http://atlantides.org/downloads/pleiades/rdf/. RDF dumps are updated weekly on Sundays. We periodically download, decompress, and unarchive these files. 

NB: RDF serializations of data for individual places — in both Turtle and RDF/XML syntax — can be had from links on the place pages, such as http://pleiades.stoa.org/places/579885/turtle for Athens, or by a negotiated request for the resource http://pleiades.stoa.org/places/579885#this. Please see the README in https://github.com/isawnyu/pleiades-rdf for a description of the RDF and the vocabularies and ontologies used.

### Changelogs

__directory: /data/changelogs/__

Monthly listings, in HTML files, of new and updated place resources since 2009. The listings include: place titles and summaries, links to the live resources on the Pleiades website using canonical URIs, and information about the creators and contributors of each resource, with a special entry for the authors of the referenced changes (includes change summary notes). 

### Data Quality Metrics

__directory: /data/data_quality/__

Experimental data quality reports, currently used by the Editorial College to prioritize and organize feature improvement and content cleanup efforts. Files include:

- `issues.json`: place ids for each category of error (see below), as well as summary information used in the generation of reports
- `bad_osm_way.csv`: place resources that reference OSM Way objects but that include coordinate information drawn from only the first Node in the referenced way. See [Pleiades Gazetteer Issue 492: add "reimport from OSM" affordance to Pleiades locations](https://github.com/isawnyu/pleiades-gazetteer/issues/492) for a feature addition that will facilitate supervised programmatic repair of such problems.
- `bad_place_type.csv`: place resources that make use of deprecated place/feature-type terms.
- `missing_accuracy.csv`: place resources with associated location resources that are missing positional accuracy metadata
- `missing_modern_name.csv`: place resources with no associated modern name resource (may not always be an error)
- `names_romanized_only.csv`: place resources that contain associated names that lack "attested" forms (i.e., original-script orthography)
- `poor_accuracy.csv`: place resources none of whose associated locations provide horizontal accuracy better than 2km.
- `question_mark_titles.csv`: place resources whose titles contain question marks (i.e., are legacy BAtlas entries for less-than-certain place/name/locations matches that have likely not yet been revisited for data modeling improvements)
- `rough_not_unlocated.csv`: place resources that are not marked (place type) as "unlocated", but that report only "rough" positions. Many of these are likely Barrington Atlas place resources that should be typed "unlocated" or that were never digitized.

### Credits

__directory: /data/html/credits.html__

A copy of the _Pleiades_ gazetteer credits page, which is online at https://pleiades.stoa.org/credits.

### DEPRECATED: Comma-Separated Values (CSV)

__directory: /data/csv/__

**Try the data in `/data/gis/` first. It may be easier to use and more complete for your use case.**

Each morning, tables __summarizing__ the published locations, names, and places are written to compressed CSV files at http://atlantides.org/downloads/pleiades/dumps/. We periodically download these files, decompress them, and incorporate them into this distribution package.

We also periodically export to CSV the contents of [the _Pleiades_ Zotero Library](https://www.zotero.org/groups/2533/pleiades?), which is used for all reference citations in the gazetteer, for incorporation into this package. 

Note the /csv/README.txt file for additional, essential information.

