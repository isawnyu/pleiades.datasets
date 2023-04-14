"""
Make indexes
"""

from airtight.cli import configure_commandline
from encoded_csv import get_csv
import json
import logging
from pathlib import Path
import re

logger = logging.getLogger(__name__)
RX_ZOTKEY = re.compile(r"^[A-Z0-0]{8}$")

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_JSON_PATH = "data/json/"
DEFAULT_ZOTERO_PATH = "data/bibliography/zotero.csv"
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
    ["-z", "--zotero", DEFAULT_ZOTERO_PATH, "path to Zotero CSV export file", False],
    ["-j", "--json", DEFAULT_JSON_PATH, "path to Pleiades JSON files", False],
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
]


def main(**kwargs):
    """
    main function
    """
    # get biblio
    csv_content = get_csv(kwargs["zotero"])["content"]
    zotkeys_d = {r["Key"]: r for r in csv_content}
    zotshorts_d = {
        r["Short Title"].strip(): r["Key"]
        for r in csv_content
        if r["Short Title"].strip()
    }
    # crawl json
    path = Path(kwargs["json"])
    works2places = dict()
    for p in path.rglob("*"):
        if p.is_file():
            if p.suffix == ".json":
                with open(p, "r", encoding="utf-8") as fp:
                    j = json.load(fp)
                del fp
                for ref in j["references"]:
                    buri = ref["bibliographicURI"]
                    if "zotero.org" in buri:
                        zotkey = [p for p in buri.split("/") if p][-1]
                        if RX_ZOTKEY.match(zotkey) is None:
                            continue
                        try:
                            works2places[zotkey]
                        except KeyError:
                            works2places[zotkey] = set()
                        works2places[zotkey].add(j["uri"])
                    else:
                        st = ref["shortTitle"]
                        if st:
                            try:
                                zotkey = zotshorts_d[st]
                            except KeyError:
                                continue
                            else:
                                try:
                                    works2places[zotkey]
                                except KeyError:
                                    works2places[zotkey] = set()
                                works2places[zotkey].add(j["uri"])
    from pprint import pprint

    pprint(works2places, indent=4)


if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL
        )
    )
