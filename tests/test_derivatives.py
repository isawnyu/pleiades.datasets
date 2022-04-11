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
        assert "295374" == result["id"]
        assert "Zucchabar" == result["title"]
