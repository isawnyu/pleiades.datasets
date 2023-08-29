#
# This file is part of pleiades.datasets
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2022 by New York University
# Licensed under the MIT License; see LICENSE.txt file.
#

"""
Code for making derivatives from JSON
"""
from bs4 import BeautifulSoup
import csv
import logging
from pathlib import Path
from pprint import pformat
import requests_cache
from shapely.geometry import shape, box
import sys
import traceback


class JSON2CSV:
    logger = logging.getLogger("JSON2CSV")
    session = requests_cache.CachedSession("derivatives")

    common_schema = dict(
        created=lambda x, y: x["created"],
        description=lambda x, y: x["description"],
        details=lambda x, y: x["details"],
        provenance=lambda x, y: x["provenance"],
        title=lambda x, y: x["title"],
        uri=lambda x, y: x["uri"],
    )

    place_schema = common_schema.copy()
    place_schema.update(
        id=lambda x, y: x["id"],
        representative_latitude=lambda x, y: x["reprPoint"][1],
        representative_longitude=lambda x, y: x["reprPoint"][0],
        bounding_box_wkt=lambda x, y: box(*x["bbox"]).wkt,
        location_precision=lambda x, y: ["rough", "precise"][
            "precise"
            in set([f["properties"]["location_precision"] for f in x["features"]])
        ],
    )
    place_keys = list(place_schema.keys())

    location_schema = common_schema.copy()
    location_schema.update(
        id=lambda x, y: x["id"],
        place_id=lambda x, y: y["id"],
        accuracy_assessment_uri=lambda x, y: x["accuracy"],
        accuracy_radius=lambda x, y: x["accuracy_value"],
        archaeological_remains=lambda x, y: x["archaeologicalRemains"],
        association_certainty=lambda x, y: x["associationCertainty"],
        geometry_wkt=lambda x, y: shape(x["geometry"]).wkt,
        year_after_which=lambda x, y: x["start"],
        year_before_which=lambda x, y: x["end"],
    )
    location_keys = list(location_schema.keys())

    name_schema = common_schema.copy()
    name_schema.update(
        id=lambda x, y: x["id"],
        place_id=lambda x, y: y["id"],
        title=lambda x, y: x["romanized"].split(",")[0].strip(),
        name_type=lambda x, y: x["nameType"],
        language_tag=lambda x, y: x["language"],
        attested_form=lambda x, y: x["attested"],
        romanized_form_1=lambda x, y: x["romanized"].split(",")[0].strip(),
        romanized_form_2=lambda x, y: x["romanized"].split(",")[1].strip() or "",
        romanized_form_3=lambda x, y: x["romanized"].split(",")[2].strip() or "",
        association_certainty=lambda x, y: x["associationCertainty"],
        transcription_accuracy=lambda x, y: x["transcriptionAccuracy"],
        transcription_completeness=lambda x, y: x["transcriptionCompleteness"],
        year_after_which=lambda x, y: x["start"],
        year_before_which=lambda x, y: x["end"],
    )
    name_keys = list(name_schema.keys())

    connection_schema = common_schema.copy()
    connection_schema.update(
        id=lambda x, y: x["id"],
        place_id=lambda x, y: y["id"],
        connection_type=lambda x, y: x["connectionType"],
        connects_to=lambda x, y: x["connectsTo"],
        association_certainty=lambda x, y: x["associationCertainty"],
        year_after_which=lambda x, y: x["start"],
        year_before_which=lambda x, y: x["end"],
    )
    connection_keys = list(connection_schema.keys())

    vocabulary_schema = dict(
        key=lambda x: x["key"],
        term=lambda x: x["term"],
        definition=lambda x: x["definition"],
    )
    vocabulary_keys = list(vocabulary_schema.keys())

    def write(self, source: list, dir: str):
        dirpath = Path(dir).expanduser().resolve()
        dirpath.mkdir(parents=True, exist_ok=True)
        for filename in [
            "archaeological_remains",
            "association_certainty",
            "connection_types",
            "connections",
            "languages_and_scripts",
            "location_linestrings",
            "location_points",
            "location_polygons",
            "name_types",
            "names",
            "place_types",
            "places_place_types",
            "places",
            "transcription_accuracy",
            "transcription_completeness",
        ]:
            print(f"Processing {filename}", end=" ...")
            getattr(self, f"_write_{filename}_csv")(source, dirpath)
            print(f"done")
        # add test for missed location types

    def _parse_vocab(self, vocab_slug: str):
        vocab_uri = f"https://pleiades.stoa.org/vocabularies/{vocab_slug}"
        r = self.session.get(vocab_uri)
        if r.status_code != 200:
            r.raise_for_status()
        soup = BeautifulSoup(r.text, features="lxml")
        div = soup.find("div", id="content")
        links = div.find_all("a", href=True)
        components = list()
        for link in links:
            if (
                link["href"] in [".", ".."]
                or link.string.strip().lower() == "back to vocabularies"
            ):
                continue
            component_uri = f"{vocab_uri}/{link['href'].split('/')[-1]}"
            cr = self.session.get(component_uri)
            if cr.status_code != 200:
                cr.raise_for_status()
            component_soup = BeautifulSoup(cr.text, features="lxml")
            term_text = component_soup.find("div", id="content").find("p").text.strip()
            components.append(
                {
                    "key": link["href"].split("/")[-1],
                    "term": link.text.strip(),
                    "definition": term_text,
                }
            )
        entries = list()
        for component in components:
            entries.append(
                {
                    k: self.vocabulary_schema[k](component) or ""
                    for k in self.vocabulary_keys
                }
            )
        self.logger.debug(pformat(entries, indent=4))
        return entries

    def _write_archaeological_remains_csv(self, source_places: list, dirpath: Path):
        parsed_terms = self._parse_vocab("arch-remains")
        filename = "archaeological_remains.csv"
        self._write_csv(dirpath / filename, parsed_terms[0].keys(), parsed_terms)

    def _write_association_certainty_csv(self, source_places: list, dirpath: Path):
        parsed_terms = self._parse_vocab("association-certainty")
        filename = "association_certainty.csv"
        self._write_csv(dirpath / filename, parsed_terms[0].keys(), parsed_terms)

    def _write_connection_types_csv(self, source_places: list, dirpath: Path):
        parsed_terms = self._parse_vocab("relationship-types")
        filename = "connection_types.csv"
        self._write_csv(dirpath / filename, parsed_terms[0].keys(), parsed_terms)

    def _write_connections_csv(self, source_places: list, dirpath: Path):
        ready_connections = list()
        for place in source_places:
            for conn in place["connections"]:
                ready_connections.append(self._convert_connection(conn, place))
        filename = "connections.csv"
        self._write_csv(
            dirpath / filename, ready_connections[0].keys(), ready_connections
        )

    def _write_names_csv(self, source_places: list, dirpath: Path):
        ready_names = list()
        for place in source_places:
            ready_names.extend(
                [self._convert_name(name, place) for name in place["names"]]
            )
        filename = "names.csv"
        self._write_csv(dirpath / filename, ready_names[0].keys(), ready_names)

    def _write_languages_and_scripts_csv(self, source_places: list, dirpath: Path):
        parsed_terms = self._parse_vocab("ancient-name-languages")
        filename = "languages_and_scripts.csv"
        self._write_csv(dirpath / filename, parsed_terms[0].keys(), parsed_terms)

    def _write_location_linestrings_csv(self, source_places: list, dirpath: Path):
        ready_locations = list()
        for place in source_places:
            for loci, loc in enumerate(place["locations"]):
                feature = place["features"][loci]
                if loc["geometry"] is None:
                    if loc["id"] not in ["batlas-location", "undetermined"] and not loc[
                        "id"
                    ].startswith("gane-location"):
                        print(
                            f"WARNING: points NULL geometry for location {loc['id']} '{loc['title']}' of place {place['id']} {place['title']}"
                        )
                    continue
                if loc["geometry"]["type"] == "LineString":
                    ready_locations.append(self._convert_location(loc, place, feature))
        if ready_locations:
            filename = "location_linestrings.csv"
            self._write_csv(
                dirpath / filename, ready_locations[0].keys(), ready_locations
            )
        else:
            self.logger.warning(f"No linestring locations were found.")

    def _write_location_points_csv(self, source_places: list, dirpath: Path):
        ready_locations = list()
        for place in source_places:
            for loci, loc in enumerate(place["locations"]):
                feature = place["features"][loci]
                if loc["geometry"] is None:
                    if loc["id"] not in ["batlas-location", "undetermined"] and not loc[
                        "id"
                    ].startswith("gane-location"):
                        print(
                            f"WARNING: points NULL geometry for location {loc['id']} '{loc['title']}' of place {place['id']} {place['title']}"
                        )
                    continue
                if loc["geometry"]["type"] == "Point":
                    ready_locations.append(self._convert_location(loc, place, feature))
        if ready_locations:
            filename = "location_points.csv"
            self._write_csv(
                dirpath / filename, ready_locations[0].keys(), ready_locations
            )
        else:
            self.logger.warning(f"No point locations were found.")

    def _write_location_polygons_csv(self, source_places: list, dirpath: Path):
        ready_locations = list()
        for place in source_places:
            for loci, loc in enumerate(place["locations"]):
                feature = place["features"][loci]
                if loc["geometry"] is None:
                    if loc["id"] not in ["batlas-location", "undetermined"] and not loc[
                        "id"
                    ].startswith("gane-location"):
                        print(
                            f"WARNING: polygons NULL geometry for location {loc['id']} '{loc['title']}' of place {place['id']} {place['title']}"
                        )
                    continue
                if loc["geometry"]["type"] == "Polygon":
                    ready_locations.append(self._convert_location(loc, place, feature))
        if ready_locations:
            filename = "location_polygons.csv"
            self._write_csv(
                dirpath / filename, ready_locations[0].keys(), ready_locations
            )
        else:
            self.logger.warning(f"No polygon locations were found.")

    def _write_place_types_csv(self, source_places: list, dirpath: Path):
        parsed_terms = self._parse_vocab("place-types")
        filename = "place_types.csv"
        self._write_csv(dirpath / filename, parsed_terms[0].keys(), parsed_terms)

    def _write_places_place_types_csv(self, source_places: list, dirpath: Path):
        rows = list()
        for p in source_places:
            for ptype in p["placeTypes"]:
                rows.append({"place_id": p["id"], "place_type": ptype})
        filename = "places_place_types.csv"
        self._write_csv(dirpath / filename, rows[0].keys(), rows)

    def _write_places_csv(self, source_places: list, dirpath: Path):
        ready_places = [self._convert_place(p) for p in source_places]
        filename = "places.csv"
        self._write_csv(dirpath / filename, ready_places[0].keys(), ready_places)

    def _write_name_types_csv(self, source_places: list, dirpath: Path):
        parsed_terms = self._parse_vocab("name-types")
        filename = "name_types.csv"
        self._write_csv(dirpath / filename, parsed_terms[0].keys(), parsed_terms)

    def _write_transcription_accuracy_csv(self, source_places: list, dirpath: Path):
        parsed_terms = self._parse_vocab("name-accuracy")
        filename = "transcription_accuracy.csv"
        self._write_csv(
            dirpath / filename,
            parsed_terms[0].keys(),
            parsed_terms,
        )

    def _write_transcription_completeness_csv(self, source_places: list, dirpath: Path):
        parsed_terms = self._parse_vocab("name-completeness")
        filename = "transcription_completeness.csv"
        self._write_csv(
            dirpath / filename,
            parsed_terms[0].keys(),
            parsed_terms,
        )

    def _write_csv(self, filepath, fieldnames, rows, quoting=csv.QUOTE_MINIMAL):
        with open(filepath, "w", encoding="utf-8-sig") as fp:
            writer = csv.DictWriter(fp, fieldnames=fieldnames, quoting=quoting)
            writer.writeheader()
            writer.writerows(rows)
        del fp

    def _convert_connection(self, connection_source: dict, place_source: dict):
        try:
            result = {
                k: self.connection_schema[k](connection_source, place_source) or ""
                for k in self.connection_keys
            }
        except KeyError as err:
            result = dict()
            for k in self.connection_keys:
                try:
                    connection_source["connectsTo"]
                except KeyError:
                    logger = logging.getLogger("derivatives._convert_connection")
                    logger.warning(
                        "\n".join(
                            [
                                "BAD CONNECTION: " + str(err),
                                f"place_id: {place_source['id']}"
                                f"{pformat(connection_source, indent=4)}",
                            ]
                        )
                    )
                else:
                    result[k] = (
                        self.connection_schema[k](connection_source, place_source) or ""
                    )
        return result

    def _convert_location(
        self, location_source: dict, place_source: dict, feature_source: dict
    ):
        from pprint import pprint

        result = dict()
        for k in self.location_keys:
            try:
                result[k] = self.location_schema[k](location_source, place_source) or ""
            except KeyError as err:
                self.logger.error(pformat(location_source, indent=4))
                raise
        result["location_precision"] = feature_source["properties"][
            "location_precision"
        ]
        return result

    def _convert_name(self, name_source: dict, place_source: dict):
        result = dict()
        for k in self.name_keys:
            if k.startswith("romanized"):
                try:
                    result[k] = self.name_schema[k](name_source, place_source) or ""
                except IndexError:
                    result[k] = ""
            else:
                result[k] = self.name_schema[k](name_source, place_source) or ""
        return result

    def _convert_place(self, place_source: dict, *args):
        result = dict()
        for k in self.place_keys:
            try:
                result[k] = self.place_schema[k](place_source, None) or ""
            except TypeError as err:
                msg = str(err)
                if msg in [
                    "'NoneType' object is not subscriptable",
                    "shapely.geometry.geo.box() argument after * must be an iterable, not NoneType",
                ]:
                    result[k] = ""
                else:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    self.logger.error(
                        f"Error converting place {place_source['id']}, field key {k}:\n"
                        + "".join(
                            traceback.format_exception(
                                exc_type, exc_value, exc_traceback, limit=3
                            )
                        )
                    )
        return result
