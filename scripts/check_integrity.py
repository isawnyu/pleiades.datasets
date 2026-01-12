#
# This file is part of "pleiades.datasets"
# by Tom Elliott
# (c) Copyright 2022 by Tom Elliott
# Licensed under the MIT license; see LICENSE.txt file.
#

"""
Script to check integrity of the current data/json directory
"""

from airtight.cli import configure_commandline
import gzip
import json
import logging
import os
from pathlib import Path
import requests

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
    ["-u", "--user_agent", "Pleiades Playground 0.1", "user agent for header", False],
    ["-f", "--from", "", "email address", False],
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
]


def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    headers = {"User-Agent": kwargs["user_agent"]}
    if kwargs["from"] != "":
        headers["From"] = kwargs["from"]

    # look for local json gz file, read it, and parse a list of place ids
    url = (
        "http://atlantides.org/downloads/pleiades/json/"
        "pleiades-places-latest.json.gz"
    )
    local_filename = url.split("/")[-1]
    local_path = Path("data/json") / local_filename
    try:
        fp = gzip.open(local_path, "rb")
    except FileNotFoundError:
        print(f"fetching {url}")
        r = requests.get(url, stream=True)
        with open(local_path, "wb") as fp:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    fp.write(chunk)
        fp.close()
        fp = gzip.open(local_path, "rb")
    else:
        print(f"Using previously downloaded local copy of {url}")
    print(f"Loading places from {local_path} ...")
    places = json.load(fp)["@graph"]
    fp.close()
    del fp
    pids_from_file = {int(p["id"]) for p in places}
    if len(pids_from_file) != len(places):
        raise RuntimeError(
            f"Unique pids count {len(pids_from_file)} does not match total number of places in file {len(places)}."
        )
    print(f"... done. Loaded {len(pids_from_file)} places.")

    # walk the data/json directory and make a list of place ids

    print("Walking the data/json directory to collect a list of pids on disk ...")
    pids_on_disk = set()
    for root, dirs, files in os.walk("data/json"):
        pids_on_disk.update(
            {int(fn.split(".")[0]) for fn in files if fn.endswith("json")}
        )
        if "c" in dirs:
            raise RuntimeError(f"There is a 'c' directory!")
    print(f"... done. Read {len(pids_on_disk)} unique pids from disk.")

    # compare the two lists and complain about differences
    extraneous_pids_on_disk = pids_on_disk - pids_from_file
    if extraneous_pids_on_disk:
        print(
            f"ERROR: There are {len(extraneous_pids_on_disk)} extraneous pids on disk that are not in {url}."
        )
        for pid in sorted(list(extraneous_pids_on_disk)):
            print(f"\t{pid}")
        raise RuntimeError("Missing PIDs in new JSON")
    missing_pids = pids_from_file - pids_on_disk
    if missing_pids:
        print(
            f"ERROR: There are {len(missing_pids)} pids in {url} that were not found on disk."
        )
        for pid in sorted(list(missing_pids)):
            print(f"\t{pid}")
        raise RuntimeError("Missing PIDs on disk")


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
