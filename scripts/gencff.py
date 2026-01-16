"""
Summarize recent commits
"""

from airtight.cli import configure_commandline
import json
import logging
import os
from pathlib import Path
from pprint import pprint, pformat
import re
from slugify import slugify
import yaml

logger = logging.getLogger(__name__)
rx_insert_field = re.compile(r"#insert-(?P<fieldname>[a-z\-]+)#")
rx_append_to_list_field = re.compile(r"#append-(?P<fieldname>[a-z\-]+)#")
INPUT_CFF_FODDER = "cff/cff-fodder.yaml"
OUTPUT_CFF_FILE = "CITATION.cff"
PLEIADES_JSON_DIR = Path(__file__).parent.parent / "data" / "json"
DATASETTER_DIR = Path(__file__).parent.parent.parent.parent / "D" / "datasetter"

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
    [
        "-d",
        "--datasetterdir",
        str(DATASETTER_DIR),
        "path to directory with Datasetter files",
        False,
    ],
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
]


def contributors2cff(pjson_path: Path, username_subs: dict) -> list:
    people = dict()
    score = dict()
    for dirpath, dirnames, filenames in os.walk(pjson_path):
        for filename in filenames:
            if filename.endswith(".json"):
                filepath = Path(dirpath) / filename
                with open(filepath, "r", encoding="utf-8") as infile:
                    data = json.load(infile)
                    locations = data.get("locations", [])
                    pnames = data.get("names", [])
                    connections = data.get("connections", [])
                    authors = []
                    for ck in ["creators", "contributors"]:
                        authors.extend(data.get(ck, []))
                        for loc in locations:
                            authors.extend(loc.get(ck, []))
                        for pname in pnames:
                            authors.extend(pname.get(ck, []))
                        for conn in connections:
                            authors.extend(conn.get(ck, []))
                    for author in authors:
                        name = author.get("name", "").strip()
                        if name == "":
                            if author.get("username", "") == "admin":
                                continue
                        if not name:
                            raise ValueError(
                                f"Person in file {filepath} has no name: {pprint(authors, indent=2)}"
                            )
                        if name == "T. Elliott":
                            username = "thomase"
                            name = "Tom Elliott"
                        elif name == "R. Talbert":
                            username = "rtalbert"
                            name = "Richard J.A. Talbert"
                        else:
                            username = author.get("username", "")
                            if not username:
                                username = slugify(name, separator="")
                            username = username.strip().lower()
                            try:
                                sub = username_subs[username]
                            except KeyError:
                                pass
                            else:
                                username = sub
                        if username == "jr":
                            continue
                        if username == "darmcrtalberttelliottsgillies":
                            these_authors = [
                                (
                                    "darmc",
                                    "Digital Atlas of Roman and Medieval Civilizations",
                                ),
                                ("rtalbert", "Richard J.A. Talbert"),
                                ("thomase", "Tom Elliott"),
                                ("sgillies", "Sean Gillies"),
                            ]
                        elif username == "rtalberttelliottsgillies":
                            these_authors = [
                                ("rtalbert", "Richard J.A. Talbert"),
                                ("thomase", "Tom Elliott"),
                                ("sgillies", "Sean Gillies"),
                            ]
                        elif username == "lquiliciandsquilicigigli":
                            these_authors = [
                                ("lquilici", "Lorenzo Quilici"),
                                ("squilicigigli", "Stefania Quilici Gigli"),
                            ]
                        elif username == "richardtalbert":
                            these_authors = [("rtalbert", "Richard J.A. Talbert")]
                        else:
                            these_authors = [(username, name)]
                        for u, n in these_authors:
                            try:
                                people[u]
                            except KeyError:
                                people[u] = {"name": n}
                                score[u] = 1
                            else:
                                score[u] += 1
    logger.debug(f"People collected: {pformat(people, indent=2)}")
    logger.debug(f"Scores collected: {pformat(score, indent=2)}")
    sorted_keys = sorted(
        [k for k in people.keys()], key=lambda x: score[x], reverse=True
    )
    logger.debug(f"Sorted keys: {pformat(sorted_keys, indent=2)}")
    cff_contributors = [people[k] for k in sorted_keys]
    logger.debug(f"CFF contributors: {pformat(cff_contributors, indent=2)}")
    return cff_contributors


def get_replacement_for_field(fieldname, pjson_path: Path) -> str:
    filepath = Path(__file__).parent.parent / "cff" / f"cff-{fieldname}.txt"
    try:
        with open(filepath, "r", encoding="utf-8") as infile:
            value = infile.read().strip()
    except FileNotFoundError:
        raise NotImplementedError(f"No replacement defined for field '{fieldname}'")
    return value


def process_cff_field(
    key: str, value: str | list | dict, pjson_path: Path, username_subs: dict
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
        n = len(value)
        newlist = []
        for i, item in enumerate(value):
            if i == n - 1 and isinstance(item, str):
                m = rx_append_to_list_field.match(item)
                if m:
                    prior_items = value[: n - 2]
                    if m.group("fieldname") == "contributors":
                        additional_items = contributors2cff(pjson_path, username_subs)
                    else:
                        raise NotImplementedError(
                            f"No append defined for field '{m.group('fieldname')}'"
                        )
                    newlist.extend(
                        [item for item in additional_items if item not in prior_items]
                    )
                    continue
            newlist.append(process_cff_field(key, item, pjson_path, username_subs))
        value = newlist
    elif isinstance(value, dict):
        newdict = {}
        for k, v in value.items():
            newdict[k] = process_cff_field(k, v, pjson_path, username_subs)
        value = newdict
    else:
        raise NotImplementedError(f"Cannot process field {key} of type {type(value)}")
    return value


def main(**kwargs):
    inpath = Path(kwargs["inputcfffodder"]).expanduser()
    outpath = Path(kwargs["outputcfffile"]).expanduser()
    pjson_path = Path(kwargs["pleiadesjsondir"]).expanduser()
    datasetter_path = Path(kwargs["datasetterdir"]).expanduser()
    username_sub_path = datasetter_path / "data" / "cache" / "who_sub.json"
    with open(username_sub_path, "r", encoding="utf-8") as infile:
        username_subs = json.load(infile)
    del infile
    with open(inpath, "r", encoding="utf-8") as infile:
        cff_fodder = yaml.load(infile, Loader=yaml.FullLoader)
    del infile
    cff = dict()
    for k, v in cff_fodder.items():
        cff[k] = process_cff_field(k, v, pjson_path, username_subs)
    with open(outpath, "w", encoding="utf-8") as outfile:
        yaml.dump(cff, outfile, sort_keys=False)
    del outfile


if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL
        )
    )
