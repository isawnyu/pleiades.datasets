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
RX_ZOTKEY = re.compile(r"^[A-Z0-9]{8}$")

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


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return sorted(list(obj), key=lambda x: int(x))
        return json.JSONEncoder.default(self, obj)


def extract_zotkeys(obj: dict) -> list:
    global zotshorts_d
    zotkeys = set()
    for ref in obj["references"]:
        buri = ref["bibliographicURI"]
        if "zotero.org" in buri:
            zotkey = [p for p in buri.split("/") if p][-1]
            if RX_ZOTKEY.match(zotkey) is None:
                continue
            zotkeys.add(zotkey)
        else:
            st = ref["shortTitle"]
            if st:
                try:
                    zotkey = zotshorts_d[st]
                except KeyError:
                    continue
                else:
                    zotkeys.add(zotkey)
    return zotkeys


def main(**kwargs):
    """
    main function
    """
    global zotshorts_d

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
    bad_zotkeys = dict()
    bad_pids_by_zotkeys = dict()
    for p in path.rglob("*"):
        if p.is_file():
            if p.suffix == ".json":
                with open(p, "r", encoding="utf-8") as fp:
                    j = json.load(fp)
                del fp
                zotkeys = extract_zotkeys(j)
                for k in ["locations", "names", "connections"]:
                    for obj in j[k]:
                        zotkeys.update(extract_zotkeys(obj))
                if zotkeys:
                    slug = [p for p in j["uri"].split("/") if p][-1]
                else:
                    continue
                for zotkey in zotkeys:
                    try:
                        zotkeys_d[zotkey]
                    except KeyError:
                        try:
                            bad_zotkeys[zotkey]
                        except KeyError:
                            bad_zotkeys[zotkey] = 0
                        bad_zotkeys[zotkey] += 1
                        try:
                            bad_pids_by_zotkeys[zotkey]
                        except KeyError:
                            bad_pids_by_zotkeys[zotkey] = set()
                        bad_pids_by_zotkeys[zotkey].add(slug)
                    try:
                        works2places[zotkey]
                    except KeyError:
                        works2places[zotkey] = set()
                    works2places[zotkey].add(slug)

    outj = json.dumps(
        works2places, ensure_ascii=False, indent=4, sort_keys=True, cls=SetEncoder
    )
    print(outj)
    logger.error(type(bad_zotkeys))
    for badk, count in sorted(bad_zotkeys.items(), key=lambda x: x[1], reverse=True):
        logger.error(
            f"Bad Zotkey: '{badk}': {count}\t: pids: {', '.join(sorted(bad_pids_by_zotkeys[badk], key=lambda x: int(x)))}"
        )


if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL
        )
    )
