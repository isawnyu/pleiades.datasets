#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update GIS derivatives
"""

from airtight.cli import configure_commandline
import json
import logging
import os
from pathlib import Path
from pleiades.datasets.derivatives import JSON2CSV
from pprint import pformat
import sys

logger = logging.getLogger(__name__)

DEFAULT_LOG_LEVEL = logging.WARNING
OPTIONAL_ARGUMENTS = [
    [
        "-l",
        "--loglevel",
        "NOTSET",
        "desired logging level ("
        + "case-insensitive string: DEBUG, INFO, WARNING, or ERROR",
        False,
    ],
    ["-v", "--verbose", False, "verbose output (logging level == INFO)", False],
    [
        "-w",
        "--veryverbose",
        False,
        "very verbose output (logging level == DEBUG)",
        False,
    ],
    ["-r", "--refresh", True, "bypass local cache and refresh all data", False],
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
]


def main(**kwargs):
    """
    main function
    """
    logger = logging.getLogger(sys._getframe().f_code.co_name)
    converter = JSON2CSV(refresh_cache=kwargs.get("refresh", False))
    places = list()
    i = 0
    for root, dirs, files in os.walk("data/json"):
        for filename in files:
            if filename.endswith(".json"):
                filepath = Path(root) / filename
                with open(filepath, "r", encoding="utf-8") as fp:
                    places.append(json.load(fp))
                del fp
                i += 1
                if i % 1000 == 0:
                    print(f"Read {i} JSON files.")
        if "c" in dirs:
            dirs.remove("c")
    print(f"Read {len(places)} JSON files.")
    converter.write(places, "data/gis")


if __name__ == "__main__":
    try:
        main(
            **configure_commandline(
                OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL
            )
        )
    except Exception as err:
        logger.fatal(err)
        exit(1)
