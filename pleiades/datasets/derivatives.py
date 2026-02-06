#
# This file is part of pleiades.datasets
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2022 by New York University
# Licensed under the MIT License; see LICENSE.txt file.
#

"""
Code for making derivatives from JSON
"""
from bs4 import BeautifulSoup, Tag
import csv
from haversine import inverse_haversine, Direction
import logging
from pathlib import Path
from pprint import pformat
import requests_cache
from shapely import distance, GeometryCollection, Point, simplify
from shapely.geometry import shape, box
import sys
from textnorm import normalize_space
from datetime import timedelta
import traceback

HEADERS = {
    "User-Agent": "PleiadesDatasets/1.0 (https://pleiades.stoa.org/)",
    "From": "pleiades-admin@nyu.edu",
    "Cache-Control": "no-cache",
}


def dd_for_meters(orig_lon, orig_lat, meters):
    """
    Given a latitude and longitude in decimal degrees, return maximum distance
    in degrees to a point in any cardinal direction that is that many meters away.
    """
    orig_point = Point(orig_lon, orig_lat)
    disances_dd = [
        distance(orig_point, Point(lon, lat))
        for lat, lon in [
            inverse_haversine((orig_lat, orig_lon), meters / 1000.0, d)
            for d in [Direction.EAST, Direction.NORTH, Direction.WEST, Direction.SOUTH]
        ]
    ]
    return max(disances_dd)


def _place_accuracies(place_source: dict, *args):
    """
    Given a place, return the maximum and minimum accuracy of its locations
    """
    accuracies = {
        loc["accuracy_value"]
        for loc in place_source["locations"]
        if loc["accuracy_value"] not in [None, "", 0]
        and loc["accuracy"] not in [None, ""]
        and isinstance(loc["accuracy_value"], float)
    }
    if len(accuracies) == 0:
        return [-1]
    return list(accuracies)


def _place_convex_hull(place_source: dict, buffer=False, *args):
    """
    Given a place, return the concave hull of its locations
    """
    precise_location_ids = [
        f["id"]
        for f in place_source["features"]
        if f["properties"]["location_precision"] == "precise"
    ]
    if len(precise_location_ids) == 0:
        return ""

    precise_locations = {
        loc["id"]: loc
        for loc in place_source["locations"]
        if loc["id"] in precise_location_ids
        and loc["accuracy_value"] not in [None, ""]
        and loc["accuracy"] not in [None, ""]
    }
    if len(precise_locations) == 0:
        return ""

    for loc in precise_locations.values():
        loc["shape"] = shape(loc["geometry"])
        loc["accuracy_dd"] = dd_for_meters(
            *reversed(list(loc["shape"].centroid.coords[0])), loc["accuracy_value"]
        )
        if buffer:
            loc["buffered"] = loc["shape"].convex_hull.buffer(
                loc["accuracy_dd"]
            )  # using simplify then convex hull to avoid cost of buffering complex geometries
            loc["convex_hull"] = loc["buffered"].convex_hull
        else:
            loc["convex_hull"] = loc["shape"].convex_hull

    gc = GeometryCollection([loc["convex_hull"] for loc in precise_locations.values()])

    return gc.convex_hull.wkt


class JSON2CSV:
    logger = logging.getLogger("JSON2CSV")
    session = requests_cache.CachedSession(
        "derivatives", expire_after=timedelta(hours=12)
    )

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

    place_accuracy_schema = dict(
        place_id=lambda x, y: x["id"],
        title=lambda x, y: x["title"],
        uri=lambda x, y: x["uri"],
        location_precision=lambda x, y: ["rough", "precise"][
            "precise"
            in set([f["properties"]["location_precision"] for f in x["features"]])
        ],
        # hull=lambda x, y: _place_convex_hull(x), reduce file size
        accuracy_hull=lambda x, y: _place_convex_hull(x, buffer=True),
        max_accuracy_meters=lambda x, y: max(_place_accuracies(x)),
        min_accuracy_meters=lambda x, y: min(_place_accuracies(x)),
        accuracy_bases=lambda x, y: ",".join(
            sorted(
                list(
                    {
                        loc["accuracy"].split("/")[-1]
                        for loc in x["locations"]
                        if loc["accuracy"] is not None
                    }
                )
            )
        ),
        location_types=lambda x, y: ",".join(
            sorted(
                list(
                    {
                        item
                        for sublist in [loc["locationType"] for loc in x["locations"]]
                        for item in sublist
                    }
                )
            )
        ),
    )
    place_accuracy_keys = list(place_accuracy_schema.keys())

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
        same_as=lambda x: x["same-as"],
        uri=lambda x: x["uri"],
    )
    vocabulary_keys = list(vocabulary_schema.keys())

    time_periods_schema = dict(
        key=lambda x: x["key"],
        term=lambda x: x["term"],
        definition=lambda x: x["definition"],
        lower_bound=lambda x: x["lower-bound"],
        upper_bound=lambda x: x["upper-bound"],
        same_as=lambda x: x["same-as"],
    )
    time_periods_keys = list(time_periods_schema.keys())

    def __init__(self, refresh_cache: bool = False):
        if refresh_cache:
            self.session.cache.clear()

    def write(self, source: list, dir: str):
        logging.getLogger("normalize_space").setLevel(logging.WARNING)
        logger = logging.getLogger("derivatives.JSON2CSV.write")
        logger.debug(f"Writing CSV derivatives to {dir}")
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
            "places_accuracy",
            "time_periods",
            "transcription_accuracy",
            "transcription_completeness",
        ]:
            print(f"Processing {filename}", end=" ...")
            getattr(self, f"_write_{filename}_csv")(source, dirpath)
            print(f"done")
        # add test for missed location types

    def _parse_vocab(self, vocab_slug: str):
        vocab_uri = f"https://pleiades.stoa.org/vocabularies/{vocab_slug}"
        logger = logging.getLogger("derivatives._parse_vocab")
        logger.debug(f"Parsing vocabulary at {vocab_uri}")
        r = self.session.get(vocab_uri, headers=HEADERS)
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
            cr = self.session.get(component_uri, headers=HEADERS)
            if cr.status_code != 200:
                cr.raise_for_status()
            component_soup = BeautifulSoup(cr.text, features="lxml")
            content_div = component_soup.find("div", id="content")
            term_text = normalize_space(content_div.find("p").text)  # type: ignore
            same_as_uri = ""
            sub_div = content_div.find("div")
            sub_paragraphs = sub_div.find_all("p")
            if len(sub_paragraphs) == 2:
                additional_text = normalize_space(sub_paragraphs[1].text)
                if additional_text.startswith("Same as:"):
                    same_as = sub_paragraphs[2].find("a")
                    if same_as:
                        same_as_uri = same_as["href"]
            components.append(
                {
                    "key": normalize_space(link["href"].split("/")[-1]),
                    "term": normalize_space(link.text),
                    "definition": term_text,
                    "same-as": same_as_uri,
                    "uri": component_uri,
                }
            )
            if vocab_slug == "time-periods":
                sub_div = (
                    component_soup.find("div", id="content").find("div").find("div")
                )
                for sub_tag in sub_div.children:
                    if not isinstance(sub_tag, Tag):
                        continue
                    try:
                        sub_text = sub_tag.strong.text
                    except AttributeError:
                        logger = logging.getLogger()
                        logger.error(component_uri)
                        logger.error(sub_tag.prettify())
                        raise
                    if sub_text == "Lower bound:":
                        components[-1]["lower-bound"] = normalize_space(
                            sub_tag.span.text
                        )
                    elif sub_text == "Upper bound:":
                        components[-1]["upper-bound"] = normalize_space(
                            sub_tag.span.text
                        )
                    elif sub_text == "Same as:":
                        try:
                            components[-1]["same-as"] = normalize_space(sub_tag.a.text)
                        except AttributeError:
                            # this field can be blank
                            components[-1]["same-as"] = ""
                    try:
                        components[-1]["same-as"]
                    except KeyError:
                        components[-1]["same-as"] = ""
        entries = list()
        for component in components:
            if vocab_slug == "time-periods":
                entries.append(
                    {
                        k: self.time_periods_schema[k](component) or ""
                        for k in self.time_periods_keys
                    }
                )
            else:
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

    def _write_places_accuracy_csv(self, source_places: list, dirpath: Path):
        ready_places = [self._convert_place_accuracy(p) for p in source_places]
        filename = "places_accuracy.csv"
        self._write_csv(dirpath / filename, ready_places[0].keys(), ready_places)

    def _write_name_types_csv(self, source_places: list, dirpath: Path):
        parsed_terms = self._parse_vocab("name-types")
        filename = "name_types.csv"
        self._write_csv(dirpath / filename, parsed_terms[0].keys(), parsed_terms)

    def _write_time_periods_csv(self, source_places: list, dirpath: Path):
        parsed_terms = self._parse_vocab("time-periods")
        filename = "time_periods.csv"
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
        except TypeError as err:
            err.add_note(
                f"Failure attempting to convert connection: {pformat(connection_source, indent=4)} for place {place_source["uri"]}"
            )
            raise err
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

    def _convert_place_accuracy(self, place_source: dict, *args):
        result = dict()
        for k in self.place_accuracy_keys:
            try:
                result[k] = self.place_accuracy_schema[k](place_source, None) or ""
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
