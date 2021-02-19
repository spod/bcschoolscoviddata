#!/usr/bin/env python3

import argparse
import csv
import sys

from collections import Counter, namedtuple
from operator import attrgetter

School = namedtuple("School", ["school", "school_district", "health_region"])
SchoolExposures = namedtuple(
    "SchoolExposures", ["school", "school_district", "health_region", "exposures"]
)


def multisort(xs, specs):
    for key, reverse in reversed(specs):
        xs.sort(key=attrgetter(key), reverse=reverse)
    return xs


def main():
    """CLI go brrrrr."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "incsv", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    parser.add_argument(
        "outcsv", nargs="?", type=argparse.FileType("w"), default=sys.stdout
    )
    config = parser.parse_args()

    # track exposures by school
    cnt = Counter()
    reader = csv.DictReader(config.incsv)

    for row in reader:
        sch = School(row["School"], row["School District"], row["Health Region"])
        cnt[sch] += 1

    # create a list of exposures so we can sort on multiple axis
    exposures = []
    for (sch, exps) in cnt.most_common():
        exposures.append(SchoolExposures(**sch._asdict() | {"exposures": exps}))

    # sort by exposures ascending, then school district descending, then school name descending
    exposures = multisort(
        exposures, (("exposures", True), ("school_district", False), ("school", False))
    )
    writer = csv.writer(config.outcsv)
    writer.writerow(
        (
            "School",
            "School District",
            "Health Region",
            "Exposures",
        )
    )
    for e in exposures:
        writer.writerow([e.school, e.school_district, e.health_region, e.exposures])


if __name__ == "__main__":
    main()
