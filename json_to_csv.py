#! /usr/bin/env python3

import argparse
import html.parser
import json
import sys

"""Generate csv from json output of dump_data.py"""

"""
This is hard coded to deal with the raw json structure and fields.
When the data format changes this will break!

Note to self for future ...
Poking around with knackpy it's likely possible to do this in a more clever way.
There is adequate metadata associate with each record to get field names etc.
If in future the format starts to iterate frequently, then I think it
should be possible to serialize some form of self describing schema for the
raw json data returned from knack.

>>> r = app.get('Covid Events', record_limit=1)[0]
>>> r.names()
['id', 'Address', ... ]
>>> r.values()
[<Field {'id': '602845984f05c4001b3ededd'}>, <Field {'field_19': '999 Noons Creek Dr, Port Moody, BC, V3H 4N3'}>, .... ]
>>> r.fields
{'id': <Field {'id': '602845984f05c4001b3ededd'}>, 'field_19': <Field {'field_19': '999 Noons Creek Dr, Port Moody, BC, V3H 4N3'}>,  ... }
>>> r.field_defs
[<FieldDef 'id'>, <FieldDef 'Address'>, <FieldDef 'City '>, ...]
"""


def main():
    """CLI go brrrrr."""
    shtmlparser = SimpleHTMLDataParser()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "injson", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    parser.add_argument(
        "outcsv", nargs="?", type=argparse.FileType("w"), default=sys.stdout
    )
    config = parser.parse_args()

    raw_data = json.load(config.injson)

    # write header
    config.outcsv.write(
        ", ".join(
            [
                "Notification Date",
                "School",
                "City",
                "School District",
                "Health Region",
                "Exposure Dates",
                "Extra Info",
            ]
        )
    )
    config.outcsv.write("\n")

    # parse and write out each record
    for record in raw_data:
        pr = CovidEventRecord(record, shtmlparser)
        config.outcsv.write(str(pr))
        config.outcsv.write("\n")


class SimpleHTMLDataParser(html.parser.HTMLParser, object):

    """SimpleHTMLDataParser - extract inner data from html."""

    # Sample usage:
    # p = SimpleHTMLDataParser()
    # p.feed("<p>Feb 10, 11</p><p><br /></p>")
    # assert p.get_data() == "Feb 10, 11"

    def __init__(self):
        self.data_stack = []
        super(SimpleHTMLDataParser, self).__init__()

    def handle_data(self, data):
        d = data.strip()
        if len(d) >= 1:
            self.data_stack.append(d)

    def get_data(self):
        return self.data_stack.pop()


class CovidEventRecord:

    """CovidEventRecord - parse a raw json record for an event, __str__ is csv version of record."""

    def __init__(self, data, shtmlparser):
        self.data = data
        self.id = self.data.get("id")
        self.notification_date = self.data.get("field_16")
        self.notification_timestamp = self.data.get("field_16_raw", {}).get(
            "unix_timestamp"
        )
        self.school = self.data.get("field_13_raw", [{}])[0].get("identifier")
        # some records have no city ...
        self.city = ""
        if "field_7_raw" in self.data and self.data["field_7_raw"] is not None:
            self.city = self.data.get("field_7_raw", [{}])[0].get("identifier")
        self.school_district = self.data.get("field_18_raw", [{}])[0].get("identifier")
        # some records have no health region ... !
        self.health_region = ""
        if "field_26_raw" in self.data and self.data["field_26_raw"] is not None:
            self.health_region = self.data.get("field_26_raw", [{}])[0].get(
                "identifier"
            )
        # Both exposure dates and extra info have raw html like: <p>Feb 10, 11</p><p><br /></p>
        # We parse the data out with shtmlparser and if the data contains commas we " quote it
        # some records have no exposure_dates ...
        self.exposure_dates = ""
        if "field_15_raw" in self.data and self.data["field_15_raw"] is not None:
            shtmlparser.feed(self.data.get("field_15_raw", ""))
            self.exposure_dates = shtmlparser.get_data()
            if "," in self.exposure_dates:
                self.exposure_dates = f'"{self.exposure_dates}"'
        # some records have no extra info ...
        self.extra_info = ""
        if "field_25_raw" in self.data and self.data["field_25_raw"] is not None:
            shtmlparser.feed(self.data.get("field_25_raw", ""))
            self.extra_info = shtmlparser.get_data()
            if "," in self.extra_info:
                self.extra_info = f'"{self.extra_info}"'

    def __str__(self):
        return ", ".join(
            [
                self.notification_date,
                self.school,
                self.city,
                self.school_district,
                self.health_region,
                self.exposure_dates,
                self.extra_info,
            ]
        )


def test():
    # test SimpleHTMLDataParser
    parser = SimpleHTMLDataParser()
    parser.feed("<p>Feb 10, 11</p><p><br /></p>")
    assert parser.get_data() == "Feb 10, 11"
    parser.feed("<p>Exposure 4</p>")
    assert parser.get_data() == "Exposure 4"

    # test we generate correct csv for the record in test.json
    test_record = None
    with open("test.json", "r") as tf:
        test_record = json.load(tf)
    expected = """02/13/2021, Mountain Meadows Elementary, Port Moody, 43, Fraser Health Authority, "Feb 10, 11", Exposure 4"""
    tr = CovidEventRecord(test_record, parser)
    assert str(tr) == expected

    # test with partial record
    test_partial = None
    with open("test2.json", "r") as tf2:
        test_partial = json.load(tf2)
    tr2 = CovidEventRecord(test_partial, parser)
    print(tr2)


if __name__ == "__main__":
    # test()
    main()
