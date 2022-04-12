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
            "places",
            "location_points",
            "location_polygons",
            "location_linestrings",
            "names",
            "connections",
        ]:
            try:
                getattr(self, f"_write_{filename}_csv")(source, dirpath)
            except AttributeError:
                pass
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

    def _write_connections_csv(self, source_places: list, dirpath: Path):
        ready_connections = list()
        for place in source_places:
            ready_connections.extend(
                [self._convert_connection(conn, place) for conn in place["connections"]]
            )
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

    def _write_location_linestrings_csv(self, source_places: list, dirpath: Path):
        ready_locations = list()
        for place in source_places:
            ready_locations.extend(
                [
                    self._convert_location(loc, place)
                    for loc in place["locations"]
                    if loc["geometry"]["type"] == "LineString"
                ]
            )
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
            ready_locations.extend(
                [
                    self._convert_location(loc, place)
                    for loc in place["locations"]
                    if loc["geometry"]["type"] == "Point"
                ]
            )
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
            ready_locations.extend(
                [
                    self._convert_location(loc, place)
                    for loc in place["locations"]
                    if loc["geometry"]["type"] == "Polygon"
                ]
            )
        if ready_locations:
            filename = "location_polygons.csv"
            self._write_csv(
                dirpath / filename, ready_locations[0].keys(), ready_locations
            )
        else:
            self.logger.warning(f"No polygon locations were found.")

    def _write_places_csv(self, source_places: list, dirpath: Path):
        ready_places = [self._convert_place(p) for p in source_places]
        filename = "places.csv"
        self._write_csv(dirpath / filename, ready_places[0].keys(), ready_places)

    def _write_csv(self, filepath, fieldnames, rows):
        with open(filepath, "w", encoding="utf-8-sig") as fp:
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        del fp

    def _convert_connection(self, connection_source: dict, place_source: dict):
        result = {
            k: self.connection_schema[k](connection_source, place_source) or ""
            for k in self.connection_keys
        }
        return result

    def _convert_location(self, location_source: dict, place_source: dict):
        result = {
            k: self.location_schema[k](location_source, place_source) or ""
            for k in self.location_keys
        }
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
        result = {
            k: self.place_schema[k](place_source, None) or "" for k in self.place_keys
        }
        return result
