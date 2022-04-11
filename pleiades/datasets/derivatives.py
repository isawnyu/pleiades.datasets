#
# This file is part of pleiades.datasets
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2022 by New York University
# Licensed under the MIT License; see LICENSE.txt file.
#

"""
Code for making derivatives from JSON
"""

class JSON2CSV:
    common_schema = dict(
        id=lambda x: x["id"],
        title=lambda x: x["title"],
        provenance=lambda x: x["provenance"]
    )

    place_schema = common_schema.copy()
    place_schema.update()
    place_keys = list(place_schema.keys())

    location_schema = common_schema.copy()
    location_schema.update()
    location_keys = list(location_schema.keys())

    name_schema = common_schema.copy()
    name_schema.update()
    name_keys = list(name_schema.keys())

    connection_schema = common_schema.copy()
    connection_schema.update()
    connection_keys = list(connection_schema.keys())

    def convert_place(self, source: dict):
        result = {k: self.place_schema[k](source) or "" for k in self.place_keys}
        return result

