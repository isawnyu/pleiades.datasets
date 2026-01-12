#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download JSON from Pleiades website and break into individual files
"""

from airtight.cli import configure_commandline
from airtight.logging import flog
from datetime import datetime, timezone
from dateutil.parser import parse as parse_date
import gzip
import json
import logging
from os import makedirs
from os.path import abspath, dirname, getmtime, join, realpath
import requests
from time import sleep

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
    [
        "-x",
        "--overwrite",
        False,
        "parse dates in files instead of timestamps on files",
        False,
    ],
    ["-r", "--rewrite", False, "write everything", False],
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
]

logger = logging.getLogger()


def get_last_mod(p):
    dates = [parse_date(h["modified"]) for h in p["history"]]
    for loc in p["locations"]:
        dates.extend([parse_date(h["modified"]) for h in loc["history"]])
        dates.append(parse_date(loc["created"]))
    for nam in p["names"]:
        dates.extend([parse_date(h["modified"]) for h in nam["history"]])
        dates.append(parse_date(nam["created"]))
    for con in p["connections"]:
        dates.extend([parse_date(h["modified"]) for h in con["history"]])
        dates.append(parse_date(con["created"]))
    sorted_dates = sorted(dates)
    try:
        last_date = sorted_dates[-1]
    except IndexError:
        logger.error(
            "Could not find created or last modified date for place {}"
            "".format(p["id"])
        )
        raise
    return last_date


def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    headers = {"User-Agent": kwargs["user_agent"]}
    if kwargs["from"] != "":
        headers["From"] = kwargs["from"]
    url = (
        "http://atlantides.org/downloads/pleiades/json/"
        "pleiades-places-latest.json.gz"
    )
    local_filename = url.split("/")[-1]
    path = join("data", "json", local_filename)
    fetch_json = False
    try:
        modified = datetime.fromtimestamp(getmtime(path), timezone.utc)
    except FileNotFoundError:
        # modified = datetime.fromtimestamp(getmtime('LICENSE'), timezone.utc)
        fetch_json = True
    else:
        if modified.date() < datetime.today().date():
            fetch_json = True
    if fetch_json:
        r = requests.get(url, stream=True)
        chunk_mb = 1  # 1 MB
        chunk_size = chunk_mb * 1024 * 1024  # bytes
        size = 0
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    size += chunk_mb
                    print(f"> read {size} MB of ?")
                    f.write(chunk)
        print(f"downloaded {size} MB to {path}")
        sleep(0.3)  # be nice to the server
    else:
        print("already have today's version of {}".format(path))
    with gzip.open(path, "rb") as f:
        j = json.load(f)
    places = j["@graph"]
    del j
    print("There are {} places in this file.".format(len(places)))
    total = len(places)
    for i, p in enumerate(places):
        if i % 1000 == 0:
            print("percent complete: {}".format(int(i / total * 100.0)))
        pid = p["id"]
        parts = list(pid)
        parts = parts[0 : len(parts) - 2]
        parts.insert(0, "json")
        parts.insert(0, "data")
        parts.append(pid)
        path = "{}.json".format(join(*parts))
        path = abspath(realpath(path))
        save = False
        if kwargs["rewrite"]:
            save = True
        elif kwargs["overwrite"]:
            try:
                with open(path, "r") as f:
                    fp = json.load(f)
            except FileNotFoundError:
                save = True
            else:
                del f
                file_modified = get_last_mod(fp)
                del fp
        else:
            try:
                file_modified = datetime.fromtimestamp(getmtime(path), timezone.utc)
            except FileNotFoundError:
                save = True
        if not save:
            place_modified = get_last_mod(p)
            if file_modified < place_modified:
                save = True
        if save:
            makedirs(dirname(path), exist_ok=True)
            with open(path, "w") as f:
                json.dump(p, f, sort_keys=True, indent=4, ensure_ascii=False)

        #


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
