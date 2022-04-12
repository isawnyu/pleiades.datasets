#
# This file is part of pleiades.datasets
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2022 by New York University
# Licensed under the MIT License; see LICENSE.txt file.
#

"""
Code for making derivatives from JSON
"""
from shapely.geometry import shape, box


class JSON2CSV:
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
        rights=lambda x, y: x["rights"],
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
        rights=lambda x, y: y["rights"],  # sic
    )
    location_keys = list(location_schema.keys())

    name_schema = common_schema.copy()
    name_schema.update(
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
        rights=lambda x, y: y["rights"],  # sic
    )
    name_keys = list(name_schema.keys())

    connection_schema = common_schema.copy()
    connection_schema.update()
    connection_keys = list(connection_schema.keys())

    def convert_place(self, place_source: dict, *args):
        result = {
            k: self.place_schema[k](place_source, None) or "" for k in self.place_keys
        }
        return result

    def convert_location(self, location_source: dict, place_source: dict):
        result = {
            k: self.location_schema[k](location_source, place_source) or ""
            for k in self.location_keys
        }
        return result

    def convert_name(self, name_source: dict, place_source: dict):
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
