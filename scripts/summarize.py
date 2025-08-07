"""
Summarize recent commits
"""

from airtight.cli import configure_commandline
from datetime import date
import logging
from pprint import pprint
import requests
import requests_cache

logger = logging.getLogger(__name__)

today = date.today()


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
    ["-d", "--date", today.isoformat(), "date of commits", False],
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
]


def get_pd_commits(recent):
    commits = dict()
    for c in recent:
        msg = c["commit"]["message"].strip().lower()
        msg = msg.split(":")[0].strip()
        msg = msg.split("\n")[0].strip()
        try:
            commits[msg]
        except KeyError:
            commits[msg] = {
                "sha": c["sha"],
                "url": c["url"],
                "datestamp": c["commit"]["author"]["date"],
            }
        else:
            logger.error(
                f"commit collision ({c['sha']} and {commits[c['commit']['message']]['sha']}); using the latter"
            )
    components = {
        # "csv": "legacy csv",
        "json": "json",
        "rdf/ttl": "rdf/ttl",
        "gis package": "gis package",
        "data quality": "data quality",
        "bibliography": "bibliography",
        "indexes": "indexes",
        "sidebar": "sidebar",
    }
    json_sha = None
    msg = list()
    for k, v in components.items():
        success = False
        alternate_keys = list()
        full_k = f"updated {k}"
        try:
            c = commits[full_k]
        except KeyError:
            if k == "data quality":
                alternate_keys = [
                    "data_quality",
                    "data quailty",
                    "data quaality",
                ]
                for alt_k in alternate_keys:
                    try:
                        c = commits[f"updated {alt_k}"]
                    except KeyError:
                        pass
                    else:
                        success = True
                        break
            elif k == "bibliography":
                alternate_keys = [
                    "bibliogreaphy",
                    "bibliogography",
                    "bibligography",
                    "bibligoraphy",
                ]
                for alt_k in alternate_keys:
                    try:
                        c = commits[f"updated {alt_k}"]
                    except KeyError:
                        pass
                    else:
                        success = True
                        break
            if not success:
                logger.debug(f"commits.keys: {commits.keys()}")
                alternate_keys.append(k)
                goofy_k = list()
                for this_k in alternate_keys:
                    logger.debug(this_k)
                    goofy_k.extend([ak for ak in commits.keys() if this_k in ak])
                if len(goofy_k) == 1:
                    c = commits[goofy_k[0]]
                    success = True
        else:
            success = True
        if success:
            if k == "json":
                json_sha = c["sha"]
            short_sha = c["sha"][:8]
            msg.append(f"{short_sha} - updated {v}")
        else:
            msg.append(f"no change: {k}")
    return (json_sha, "\n".join(msg))


def get_json_changes(url):
    r = requests.get(url)
    j = r.json()
    files = {
        f["filename"]: {"status": f["status"], "url": f["raw_url"]} for f in j["files"]
    }
    new_count = len([f for f in files.values() if f["status"] == "added"])
    updated_count = len([f for f in files.values() if f["status"] == "modified"])
    if new_count and updated_count:
        msg = f"{new_count} new and {updated_count} updated place"
    elif new_count:
        msg = f"{new_count} new place"
    elif updated_count:
        msg = f"{updated_count} updated place"
    else:
        msg = "No new or updated places"
    total = new_count + updated_count
    if total > 1:
        msg += "s"
    msg += "."
    return msg


def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    commit_url = "https://api.github.com/repos/isawnyu/pleiades.datasets/commits"
    r = requests.get(commit_url)
    j = r.json()
    recent = [c for c in j if c["commit"]["author"]["date"].startswith(kwargs["date"])]

    json_sha, commit_summary = get_pd_commits(recent)
    try:
        count_summary = get_json_changes("/".join((commit_url, json_sha)))
    except TypeError:
        count_summary = "No new or updated places."

    print(f"Export Updates {kwargs['date']}:\nPleiades gazetteer of ancient places\n")
    print(count_summary)
    print("\n1. Downloads: https://pleiades.stoa.org/downloads\n")
    print("2. pleiades.datasets: https://github.com/isawnyu/pleiades.datasets:\n")
    print('"main" branch:\n')
    print(commit_summary)
    print("\n3. pleiades-geojson: https://github.com/ryanfb/pleiades-geojson:\n")

    commit_url = "https://api.github.com/repos/ryanfb/pleiades-geojson/commits"
    r = requests.get(commit_url)
    j = r.json()
    recent = [c for c in j if c["commit"]["author"]["date"].startswith(kwargs["date"])]
    if recent:
        c = recent[0]
        short_sha = c["sha"][:8]
        msg = f"{short_sha} - {c['commit']['message']}"
    else:
        msg = f"no change"
    print(msg)

    print("\n4. pleiades_wikidata: https://github.com/isawnyu/pleiades_wikidata/:\n")

    commit_url = "https://api.github.com/repos/isawnyu/pleiades_wikidata/commits"
    r = requests.get(commit_url)
    j = r.json()
    recent = [c for c in j if c["commit"]["author"]["date"].startswith(kwargs["date"])]
    if recent:
        c = recent[0]
        short_sha = c["sha"][:8]
        msg = f"{short_sha} - {c['commit']['message']}".split(":")[0].strip()
    else:
        msg = f"no change"
    print(msg)


if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL
        )
    )
