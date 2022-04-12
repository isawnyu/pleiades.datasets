#
# This file is part of pleiades.datasets
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2022 by New York University
# Licensed under the MIT License; see LICENSE.txt file.
#

"""
Test the derivatives module
"""
import json
from pathlib import Path
from pleiades.datasets.derivatives import JSON2CSV


class TestJSON2CSV:
    converter = JSON2CSV()

    def test_place(self):
        filepath = Path("tests/data/zucchabar.json")
        with open(filepath, "r", encoding="utf-8") as fp:
            source = json.load(fp)
        del fp
        result = self.converter.convert_place(source)
        assert "2010-09-24T21:02:57Z" == result["created"]
        assert (
            "Zucchabar was an ancient city of Mauretania Caesariensis with Punic origins. The modern Algerian "
            "community of Miliana lies atop and around the largely unexcavated ancient site. Epigraphic evidence "
            "indicates that the Roman emperor Augustus established a veteran colony there."
        ) == result["description"]
        assert (
            "<p>The Barrington Atlas Directory notes: Miliana</p>" == result["details"]
        )
        assert "Barrington Atlas: BAtlas 30 D4 Zucchabar" == result["provenance"]
        assert "Zucchabar" == result["title"]
        assert "https://pleiades.stoa.org/places/295374" == result["uri"]
        assert "295374" == result["id"]
        assert 36.304939 == result["representative_latitude"]
        assert 2.223758 == result["representative_longitude"]
        assert (
            "POLYGON ((2.22619 36.304782, 2.22619 36.304939, 2.223758 36.304939, 2.223758 36.304782, 2.22619 36.304782))"
            == result["bounding_box_wkt"]
        )
        assert (
            "Copyright © The Contributors. Sharing and remixing permitted under terms of the Creative Commons Attribution 3.0 License (cc-by)."
            == result["rights"]
        )

    def test_location(self):
        filepath = Path("tests/data/zucchabar.json")
        with open(filepath, "r", encoding="utf-8") as fp:
            place = json.load(fp)
        del fp
        location = place["locations"][0]
        result = self.converter.convert_location(location, place)
        assert "2011-03-09T22:42:32Z" == result["created"]
        assert "500K scale point location" == result["description"]
        assert "DARMC OBJECTID: 15549" == result["details"]
        assert "DARMC OBJECTID: 15549" == result["provenance"]
        assert "DARMC location 15549" == result["title"]
        assert (
            "https://pleiades.stoa.org/places/295374/darmc-location-15549"
            == result["uri"]
        )
        assert "darmc-location-15549" == result["id"]
        assert "295374" == result["place_id"]
        assert (
            "https://pleiades.stoa.org/features/metadata/darmc-a"
            == result["accuracy_assessment_uri"]
        )
        assert "" == result["accuracy_radius"]
        assert "unknown" == result["archaeological_remains"]
        assert "certain" == result["association_certainty"]
        assert "POINT (2.223758 36.304939)" == result["geometry_wkt"]
        assert -330 == result["year_after_which"]
        assert 300 == result["year_before_which"]
        assert (
            "Copyright © The Contributors. Sharing and remixing permitted under terms of the Creative Commons Attribution 3.0 License (cc-by)."
            == result["rights"]
        )
