"""
Summarize recent commits
"""

from airtight.cli import configure_commandline
import logging
import os
from pathlib import Path
from pprint import pprint
import re
import yaml

logger = logging.getLogger(__name__)
rx_insert_field = re.compile(r"#insert-(?P<fieldname>[a-z\-]+)#")
rx_append_to_list_field = re.compile(r"#append-(?P<fieldname>[a-z\-]+)#")
INPUT_CFF_FODDER = "cff/cff-fodder.yaml"
OUTPUT_CFF_FILE = "CITATION.cff"
PLEIADES_JSON_DIR = Path(__file__).parent.parent / "data" / "json"

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
        "-i",
        "--inputcfffodder",
        INPUT_CFF_FODDER,
        "path to input cff-fodder.yaml file",
        False,
    ],
    [
        "-o",
        "--outputcfffile",
        OUTPUT_CFF_FILE,
        "path to output cff file",
        False,
    ],
    [
        "-p",
        "--pleiadesjsondir",
        str(PLEIADES_JSON_DIR),
        "path to directory with Pleiades JSON files",
        False,
    ],
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
]


def contributors2cff(pjson_path: Path) -> list:
    return ["foo", "bar", "baz"]  # placeholder implementation


def get_replacement_for_field(fieldname, pjson_path: Path) -> str:
    filepath = Path(__file__).parent.parent / "cff" / f"cff-{fieldname}.txt"
    try:
        with open(filepath, "r", encoding="utf-8") as infile:
            value = infile.read().strip()
    except FileNotFoundError:
        raise NotImplementedError(f"No replacement defined for field '{fieldname}'")
    return value


def process_cff_field(
    key: str, value: str | list | dict, pjson_path: Path
) -> str | list | dict:

    if isinstance(value, str):
        m = rx_insert_field.match(value)
        if m:
            new_val = get_replacement_for_field(m.group("fieldname"), pjson_path)
            value = new_val
            logger.debug(
                f"Found insert field for key {key}: {value}. Replaced with {new_val}"
            )
    elif isinstance(value, list):
        newlist = []
        n = len(value)
        for i, item in enumerate(value):
            if i == n - 1 and isinstance(item, str):
                m = rx_append_to_list_field.match(item)
                if m:
                    if m.group("fieldname") == "contributors":
                        newitems = contributors2cff(pjson_path)
                        newlist.extend(newitems)
                    else:
                        raise NotImplementedError(
                            f"No append defined for field '{m.group('fieldname')}'"
                        )
                    continue
            newlist.append(process_cff_field(key, item, pjson_path))
        value = newlist
    elif isinstance(value, dict):
        newdict = {}
        for k, v in value.items():
            newdict[k] = process_cff_field(k, v, pjson_path)
        value = newdict
    else:
        raise NotImplementedError(f"Cannot process field {key} of type {type(value)}")
    return value


def main(**kwargs):
    inpath = Path(kwargs["inputcfffodder"]).expanduser()
    outpath = Path(kwargs["outputcfffile"]).expanduser()
    pjson_path = Path(kwargs["pleiadesjsondir"]).expanduser()
    with open(inpath, "r", encoding="utf-8") as infile:
        cff_fodder = yaml.load(infile, Loader=yaml.FullLoader)
    del infile
    cff = dict()
    for k, v in cff_fodder.items():
        cff[k] = process_cff_field(k, v, pjson_path)
    with open(outpath, "w", encoding="utf-8") as outfile:
        yaml.dump(cff, outfile, sort_keys=False)
    del outfile


if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL
        )
    )
