#! /usr/bin/env python3

import argparse
import html.parser
import json
import sqlite3
import sys

"""Generate a sqlite db from json output of dump_data.py"""

from json_to_csv import CovidEventRecord, SimpleHTMLDataParser


# If this is actually useful should split out tables for:
# - school, city, school_district, health_region
# - parse out exposure dates as a range
#

TABLE_SCHEMA = """
create table exposures (
    id                  integer primary key autoincrement not null,
    notification_date   text,
    school              text,
    city                text,
    school_district     text,
    health_region       text,
    exposure_dates      text,
    extra_info          text
);
"""


def c(field):
    """Remove " from field"""
    return field.replace('"', "")


def main():
    """CLI go brrrrr."""
    shtmlparser = SimpleHTMLDataParser()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "injson", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    parser.add_argument(
        "outdb",
        nargs="?",
        type=argparse.FileType("w"),
        default=":memory:",
    )
    config = parser.parse_args()

    raw_data = json.load(config.injson)
    conn = sqlite3.connect(config.outdb.name)

    conn.executescript(TABLE_SCHEMA)

    curr = conn.cursor()

    # parse and write out each record
    for record in raw_data:
        pr = CovidEventRecord(record, shtmlparser)
        insert_stmt = f'INSERT INTO exposures (notification_date, school, city, school_district, health_region, exposure_dates, extra_info) VALUES ("{pr.notification_date}", "{c(pr.school)}", "{pr.city}", "{pr.school_district}", "{pr.health_region}", "{c(pr.exposure_dates)}", "{c(pr.extra_info)}")'
        try:
            curr.execute(insert_stmt)
        except sqlite3.OperationalError as e:
            print(f"ERROR {e} executing: {insert_stmt}")
            sys.exit(1)
    conn.commit()
    curr.execute("vacuum;")
    conn.close()


if __name__ == "__main__":
    main()
