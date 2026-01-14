"""
Summarize recent commits
"""

from airtight.cli import configure_commandline
import logging
from pathlib import Path
from pprint import pprint
import re
import yaml

logger = logging.getLogger(__name__)
rx_insert_field = re.compile(r"#insert-(?P<fieldname>[a-z\-]+)#")
INPUT_CFF_FODDER = "cff-fodder.yaml"
OUTPUT_CFF_FILE = "CITATION.cff"

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
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
]


def get_replacement_for_field(fieldname) -> str:
    if fieldname == "":
        pass
    else:
        raise NotImplementedError(f"No replacement defined for field '{fieldname}'")
    return ""


def process_cff_field(key: str, value: str | list | dict) -> str | list | dict:

    if isinstance(value, str):
        m = rx_insert_field.match(value)
        if m:
            new_val = get_replacement_for_field(m.group("fieldname"))
            value = new_val
            logger.debug(
                f"Found insert field for key {key}: {value}. Replaced with {new_val}"
            )
    elif isinstance(value, list):
        newlist = []
        for item in value:
            newlist.append(process_cff_field(key, item))
        value = newlist
    elif isinstance(value, dict):
        newdict = {}
        for k, v in value.items():
            newdict[k] = process_cff_field(k, v)
        value = newdict
    else:
        raise NotImplementedError(f"Cannot process field {key} of type {type(value)}")
    return value


def main(**kwargs):
    inpath = Path(kwargs["inputcfffodder"]).expanduser()
    outpath = Path(kwargs["outputcfffile"]).expanduser()
    with open(inpath, "r", encoding="utf-8") as infile:
        cff_fodder = yaml.load(infile, Loader=yaml.FullLoader)
    del infile
    cff = dict()
    for k, v in cff_fodder.items():
        cff[k] = process_cff_field(k, v)
    with open(outpath, "w", encoding="utf-8") as outfile:
        yaml.dump(cff, outfile, sort_keys=False)
    del outfile


if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL
        )
    )
