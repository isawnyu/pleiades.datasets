#
# This file is part of "pleiades.datasets"
# by Tom Elliott
# (c) Copyright 2024 by Tom Elliott
# Licensed under the MIT license; see LICENSE.txt file.
#

"""
Script to list alignments between Pleiades and specific Zotero IDs
"""

from airtight.cli import configure_commandline
from encoded_csv import get_csv
import json
import logging
from os.path import join
from pathlib import Path
from pprint import pformat

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
    [
        "-b",
        "--bibliopath",
        str(Path("./data/bibliography/zotero.csv").resolve()),
        "path to csv zotero export file",
        False,
    ],
    ["-f", "--format", "html", "output format (html or json)", False],
    [
        "-k",
        "--keys2pidspath",
        str(Path("./data/bibliography/zotkeys2pids.json").resolve()),
        "path to zotkeys json file",
        False,
    ],
    [
        "-p",
        "--pleiadesjsonpath",
        str(Path("./data/json/").resolve()),
        "path to pleiades JSON directory",
        False,
    ],
    [
        "-s",
        "--subordinates",
        False,
        "rip references from subordinate pleiades objects (names, locations, connections)",
        False,
    ],
    ["-z", "--zotkeys", "", "comma-separated list of zotero keys to mine", False],
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
]


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def get_place(ppath: Path, pid: str) -> dict:
    logger = logging.getLogger("get_place")
    logger.debug(f"pid: {pid}")
    parts = list(pid)
    parts = parts[0 : len(parts) - 2]
    parts.append(pid)
    filepath = ppath / Path("{}.json".format(join(*parts)))
    logger.debug(f"file_path: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        p = json.load(f)
    del f
    return p


def rip_refs(
    data: dict | list,
    zotkey: str,
    otype: str = "Place",
    subordinates: bool = False,
    results: list = None,
) -> dict:
    if not otype:
        raise ValueError(f"empty otype")
    if otype == "Place":
        results = list()
        for k in ["connections", "locations", "names"]:
            if data[k]:
                rip_refs(data[k], zotkey, k.title(), results)
    elif otype in ["Connections", "Locations", "Names"]:
        for c in data:
            rip_refs(c, zotkey, otype[0 : len(otype) - 1], results)
        return
    for ref in data["references"]:
        if ref["bibliographicURI"].endswith(zotkey):
            results.append(
                {
                    "accessURI": ref["accessURI"],
                    "citationDetail": ref["citationDetail"],
                    "context": otype,
                    "zotkey": zotkey,
                }
            )
    if otype == "Place":
        return results


def capture(results: dict, p: dict, refs: list):
    puri = p["uri"]
    try:
        results[puri]
    except KeyError:
        results[puri] = {
            "place_title": p["title"],
            "place_types": p["placeTypes"],
            "uri": p["uri"],
            "alignments": set(),
        }
        try:
            rp = p["reprPoint"]
        except KeyError:
            results[puri]["representative_longitude"] = None
            results[puri]["representative_latitude"] = None
        else:
            if rp is None:
                results[puri]["representative_longitude"] = None
                results[puri]["representative_latitude"] = None
            else:
                results[puri]["representative_longitude"] = rp[0]
                results[puri]["representative_latitude"] = rp[1]
    results[puri]["alignments"].update([ref["accessURI"] for ref in refs])

    for ref in refs:
        ruri = ref["accessURI"]
        try:
            results[ruri]
        except KeyError:
            results[ruri] = {
                "citaton_detail": ref["citationDetail"],
                "zotkey": ref["zotkey"],
                "alignments": set(),
            }
        results[ruri]["alignments"].add(puri)


def main(**kwargs):
    """
    main function
    """
    logger = logging.getLogger()

    supported_formats = {"markdown", "json"}
    if kwargs["format"] not in supported_formats:
        raise ValueError(f"Unsupported output format ({kwargs['format']}) requested")

    logger.info(f"Processsing zotkey input")
    if not kwargs["zotkeys"].strip():
        raise ValueError(f"At least one zotero key is required")
    zotkeys = [k.strip() for k in kwargs["zotkeys"].split()]
    zotkeys = {k for k in zotkeys if k}

    k2ppath = Path(kwargs["keys2pidspath"]).expanduser().resolve()
    logger.info(f"Loading zotkeys2pids data from {k2ppath}")
    with open(k2ppath, "r", encoding="utf-8") as f:
        k2p = json.load(f)
    del f

    ppath = Path(kwargs["pleiadesjsonpath"]).expanduser().resolve()
    results = dict()
    for k in zotkeys:
        try:
            pids = k2p[k]
        except KeyError:
            logger.error(f"No entry for zotkey {k} found in {k2ppath}")
        else:
            for pid in pids:
                p = get_place(ppath, pid)
                refs = rip_refs(p, k, "Place", subordinates=kwargs["subordinates"])
                if refs:
                    capture(results, p, refs)

    if kwargs["format"] == "json":
        print(
            json.dumps(
                results, ensure_ascii=False, indent=4, sort_keys=True, cls=SetEncoder
            )
        )
    else:
        raise NotImplementedError(kwargs["format"])


if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL
        )
    )
