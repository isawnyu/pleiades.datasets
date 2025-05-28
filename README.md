# _Pleiades_ gazetteer datasets

Please report problems and make feature requests via [the main _Pleiades_ Gazetteer Issue Tracker](https://github.com/isawnyu/pleiades-gazetteer/issues/).

[![License: CC BY 3.0](https://licensebuttons.net/l/by/3.0/80x15.png)](https://creativecommons.org/licenses/by/3.0/) Content is governed by the copyrights of the individual contributors responsible for its creation. Some rights are reserved. All content is distributed under the terms of a [Creative Commons Attribution license (cc-by)](https://creativecommons.org/licenses/by/3.0/).

In order to facilitate reproducibility and to comply with license terms, we encourage use and citation of [numbered releases](https://pleiades.stoa.org/downloads#releases) for scholarly work that will be published in static form.

Please share notices of data reuse with the _Pleiades_ community via email to pleiades.admin@nyu.edu. These reports help us to justify continued funding and operation of the gazetteer and to prioritize updates and improvements.

## Version 4.1 - 28 May 2025

### 41,480 place resources

Since release 4.0.1 of _pleiades.datasets_ on 6 February 2025, the _Pleiades_ gazetteer published 287 new and 2,757 updated place resources, reflecting the work of Jeffrey Becker, Sarah Bond, Catherine Bouras, Anne Chen, Birgit Christiansen, Matthew Clark, Stefano Costa, Anthony Durham, Tom Elliott, Margherita Fantoli, E.W.B. Fentress, Güner Girgin, Maxime Guénette, Greta Hawes, Brady Kiesling, Chris de Lisle, Sean Manning, Gabriel McKee, John Muccigrosso, Jamie Novotny, Gethin Rees, Rosemary Selth, R. Scott Smith, Nicolas Souchon, Néhémie Strupler, Richard Talbert, Clifflena Tiah, and Scott Vanderbilt. As a result, this release provides documentation for 41,480 place resources.

### Highlights

- Updated gazetteer data in this release: see "Contents" below.
- Removed deprecated "legacy CSV" serialization. JSON or "CSV for GIS" are the recommended packages for most third-party reuse.
- Added new "indexes" dataset: _Pleiades_ places that reference certain external resources.
- Improved serialization of vocabulary terms in "CSV for GIS" serialization and added the previously omitted "Time Periods" vocabulary.
- Added new "sidebar" dataset: assertions by external datasets of relationships to _Pleiades_ places.

## Overview

This is a package of data derived from the _Pleiades_ gazetteer of ancient places. It is used for archival and redistribution purposes and is likely to be __less up-to-date than the live data at https://pleiades.stoa.org.__

_Pleiades_ is a community-built gazetteer and graph of ancient places. It publishes authoritative information about ancient places and spaces, providing unique services for finding, displaying, and reusing that information under open license. It publishes not just for individual human users, but also for search engines and for the widening array of computational research and visualization tools that support humanities teaching and research.

_Pleiades_ is a continuously published scholarly reference work for the 21st century. We embrace the new paradigm of citizen humanities, encouraging contributions from any knowledgeable person and doing so in a context of pervasive peer review. _Pleiades_ welcomes your contribution, no matter how small, and we have a number of useful tasks suitable for volunteers of every interest.

## Access and Archiving

The latest versions of this package can be had by fork or download from the `main` branch at https://github.com/isawnyu/pleiades-datasets. [Numbered releases](https://github.com/isawnyu/pleiades-datasets/releases) are created periodically at GitHub. These are archived at:

 - zenodo.org using the DOI [10.5281/zenodo.1193921](https://doi.org/10.5281/zenodo.1193921)
 - archive.nyu.edu using the Handle [2451/34305](https://hdl.handle.net/2451/34305)
 - archive.org using the URI https://archive.org/details/pleiades.datasets-{version_number}

## Credits

_Pleiades_ is brought to you by:

  * Our volunteer content contributors (see `data/rdf/authors.ttl` for complete list and associated identifiers or data).
  * _Pleiades_ received significant, periodic support from the [National Endowment for the Humanities](https://www.neh.gov) between 2006 and 2019. Grant numbers: HK-230973-15, PA-51873-06, PX-50003-08, and PW-50557-10. Any views, findings, conclusions, or recommendations expressed in this publication do not necessarily reflect those of the National Endowment for the Humanities. 
  * Web hosting and additional support has been provided since 2008 by the [Institute for the Study of the Ancient World](https://isaw.nyu.edu) at New York University.
  * Additional support and in-kind collaboration has been provided since 2000 by the [Ancient World Mapping Center](https://awmc.unc.edu) at the University of North Carolina at Chapel Hill. 
  * Development hosting and other project incubation support was provided between 2000 and 2008 by [Ross Scaife](https://en.wikipedia.org/wiki/Ross_Scaife) and the [Stoa Consortium](https://www.stoa.org/).
  
## Contents

### JavaScript Object Notation (JSON)

__directory: `/data/json/`__

The __complete__ serialization of each published object in the _Pleiades_ database (i.e., every place, name, location, and connection resource) is written to [a single, large JSON file](http://atlantides.org/downloads/pleiades/json/) once daily. We periodically download this file and split it up into individual files, one for each place resource (together with its subordinate name, location, and connection resources). 

Each file is named with the final, numeric portion of the place resource's Uniform Resource Identifier (URI), plus the filename extension ".json". So, for example, the URI for the _Pleiades_ place resource describing Roman Heidelberg is https://pleiades.stoa.org/places/118731. The corresponding JSON file in this dataset is named "118731.json". 

In order to avoid performance problems on operating systems that cannot handle large numbers of files in a single directory efficiently, the JSON files are distributed throughout a hierarchical directory structure using each of the first few digits in the base filename as a subdirectory. So, for the Heidelberg example, one would find the JSON file at the relative path `data/json/1/1/8/7/118731.json`.

### GIS Package (in CSV format)

__directory: `/data/gis/`__

A collection of CSV files derived from data in the _Pleiades_ gazetteer of ancient places. This collection is intended to facilitate use of _Pleiades_ data in geographic information systems software and other programming contexts where JSON is inconvenient. __NB: not all attributes are included in this serialization.__ Files have been tested for use in QGIS. See further `data/gis/README.md`.

### Resource Description Framework (RDF)

__directory: `/data/rdf/`__

The __summary__ data for all places, errata, authors, place types, and time periods is available for download in Turtle (Terse RDF Triple Language) via http://atlantides.org/downloads/pleiades/rdf/pleiades-latest.tar.gz. This is a gzip-compressed, TAR archive. Previous RDF dumps are also available at http://atlantides.org/downloads/pleiades/rdf/. RDF dumps are updated weekly on Sundays. We periodically download, decompress, and unarchive these files. 

NB: RDF serializations of data for individual places — in both Turtle and RDF/XML syntax — can be had from links on the place pages, such as http://pleiades.stoa.org/places/579885/turtle for Athens, or by a negotiated request for the resource http://pleiades.stoa.org/places/579885#this. Please see the README in https://github.com/isawnyu/pleiades-rdf for a description of the RDF and the vocabularies and ontologies used.

### Changelogs

__directory: `/data/changelogs/`__

Monthly listings, in HTML files, of new and updated place resources since 2009. The listings include: place titles and summaries, links to the live resources on the Pleiades website using canonical URIs, and information about the creators and contributors of each resource, with a special entry for the authors of the referenced changes (includes change summary notes). The file `release.html` provides a changelog for the current release with respect to the previous release.

### Data Quality Metrics

__directory: `/data/data_quality/`__

Data quality and characterization reports, currently used by the Editorial College to prioritize and organize feature improvement and content cleanup efforts. Files include:

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

__directory: `/data/html/credits.html`__

A copy of the _Pleiades_ gazetteer credits page, which is online at https://pleiades.stoa.org/credits.

### Indexes

__directory: `/data/indexes/`__

Various indexes, potentially of value when working with _Pleiades_ content.

- `name_index.json`: a list of all name and place title strings occurring in the gazetteer, together with the associated _Pleiades_ place IDs.
- JSON files, and Markdown generated from them, reporting on references from _Pleiades_ places to the following external resources:
  - `aio`: Lambert, Stephen, Polly Low, Peter Liddel, and Chris de Lisle, eds. _Attic Inscriptions Online._ Athens: British School at Athens, 2012-. https://www.atticinscriptions.com/.
  - `cfl_ago`: Veronique Chankowski, Amélie Perrier, Catherine Bouras, Sabine Fourrier, John Bennet, Michaeol Loy, Kostis Christakis, L. Mulot, and G. Bejjaji. _Chronique Des Fouilles En Ligne = Archaeology in Greece Online._ Athens: Ecole française d’Athènes and British School at Athens, 2018-. https://chronique.efa.gr/?kroute=homepage.
  - `manto`: Hawes, Greta, and Scott Smith. MANTO. 2020-. https://www.manto-myth.org/manto.
  - `paus-spiro-perseus`: Pausanias. _Pausaniae Graeciae descriptio._ Edited by Friedrich Spiro. 3 vols. Bibliotheca Teubneriana. Lipsiae: Teubner, 1903. As digitized and published by the Perseus Digital Library http://data.perseus.org/texts/urn:cts:greekLit:tlg0525.tlg001.perseus-grc1.
  - `tm`: Depauw, Mark, Tom Gheldof, Herbert Verreth, Nico Dogaer, Willy Clarysse, Yanne Broux, Gert Baetens, and Heinz-Josef Thissen. _Trismegistos: An Interdisciplinary Portal of the Ancient World._ Leuven, 2006-. http://www.trismegistos.org/.
  - `topostext`: Kiesling, Brady. _ToposText – a Reference Tool for Greek Civilization._ Version 2.0. Aikaterini Laskaridis Foundation, 2016-. https://topostext.org/.
  - `wikidata`: _Wikidata: The Free Knowledge Base That Anyone Can Edit._ Wikimedia Foundation, 2014-. https://www.wikidata.org/.


### Sidebar

__directory: `/data/sidebar/`__

JSON files containing information about incoming links from external resources that are currently indexed. Files are named according to the corresponding _Pleiades_ ID. This data is used for [a "Linked Data" widget on Pleiades place pages](https://pleiades.stoa.org/help/linked-data-sidebar). This data is generated using code in the [pleiades_sidebar](https://github.com/isawnyu/pleiades_sidebar) repository. The following external sites are currently indexed for presentation in the sidebar:
<ul>
    <li>CFL/AGO: "Toponyme" entries from:<br>
    Veronique Chankowski, Amélie Perrier, Catherine Bouras, Sabine Fourrier, John Bennet, Michaeol Loy, Kostis Christakis, L. Mulot, and G. Bejjaji. _Chronique Des Fouilles En Ligne = Archaeology in Greece Online._ Athens: Ecole française d’Athènes and British School at Athens, 2018-. https://chronique.efa.gr/?kroute=homepage.</li>
    <li>Classical Temples: entries from:<br>
    John D. Muccigrosso and Louis I. Hamilton. _Temples of the Classical World._ Rome Research Group. https://romeresearchgroup.org/database-of-temples/.</li>
    <li>EDH: entries from the "Geographic Database" of:<br>
    Alföldy, Géza, and Christian Witschel, eds. _Epigraphic Database Heidelberg._ Heidelberg: Heidelberg Academy of Sciences and Humanities, 1997-2021. http://edh-www.adw.uni-heidelberg.de/.</li>
    <li>Itiner-E: road segment entries from:<br>
    Brughmans, Tom, Pau de Soto, A. Pažout, and P. Bjerregaard Vahlstrup. _Itiner-e: The Digital Atlas of Ancient Roads,_ 2024. https://itiner-e.org/.</li>
    <li>MANTO: place records from:<br>
    Hawes, Greta, and Scott Smith. _MANTO: a digital dataset of Greek myth._ 2020-. https://www.manto-myth.org/manto.</li>
    <li>Nomisma: mint records from:<br>
    Meadows, Andrew, Sebastian Heath, and Ethan Gruber. _Nomisma.org._ New York: American Numismatic Society, 2010-. http://nomisma.org/.</li>
    <li>PAThs Atlas: place records from:<br>
    Bogdani, Julian, and Paolo Rosati. _An Archaeological Atlas of Coptic Literature. PAThs - Tracking Papyrus and Parchment Paths: An Archaeological Atlas of Coptic Literature. Literary Texts in Their Geographical Context: Production, Copying, Usage, Dissemination and Storage._ Roma: Sapienza Università di Roma, 2016. https://atlas.paths-erc.eu/.</li>
    <li>Wikidata: items in:<br>
    _Wikidata: The Free Knowledge Base That Anyone Can Edit._ Wikimedia Foundation, 2014-. https://www.wikidata.org/.</li>
</ul>
