#! /usr/bin/env python3

import html.parser
import json

"""
Note for now this is hard coded to deal with the raw json structure and fields.
If the data format changes this will likely break ...

Poking around with knackpy it's likely possible to do this slightly more cleverly ...

>>> r = app.get('Covid Events', record_limit=1)[0]
>>> r.names()
['id', 'Address', 'City ', 'School District', 'Notification Date', 'School', 'Notification', 'Exposure Dates', 'Extra Info', 'Documentation', 'Health Region', 'Status']
>>> r.values()
[<Field {'id': '602845984f05c4001b3ededd'}>, <Field {'field_19': '999 Noons Creek Dr, Port Moody, BC, V3H 4N3'}>, <Field {'field_7': 'Port Moody'}>, <Field {'field_18': '43'}>, <Field {'field_16': '2021-02-13T00:00:00-08:00'}>, <Field {'field_13': 'Mountain Meadows Elementary'}>, <Field {'field_14': 'Letter to family'}>, <Field {'field_15': '<p>Feb 10, 11</p><p><br /></p>'}>, <Field {'field_25': '<p>Exposure 4</p>'}>, <Field {'field_28': 'https://api.knack.com/v1/applications/5faae3b10442ac00165da195/download/asset/60284589bc3817001bf307df/ceccb763ae294700bd3a671dba138ca6.jpeg'}>, <Field {'field_26': 'Fraser Health Authority'}>, <Field {'field_30': 'Current'}>]
>>> r.fields
{'id': <Field {'id': '602845984f05c4001b3ededd'}>, 'field_19': <Field {'field_19': '999 Noons Creek Dr, Port Moody, BC, V3H 4N3'}>, 'field_7': <Field {'field_7': 'Port Moody'}>, 'field_18': <Field {'field_18': '43'}>, 'field_16': <Field {'field_16': '2021-02-13T00:00:00-08:00'}>, 'field_13': <Field {'field_13': 'Mountain Meadows Elementary'}>, 'field_14': <Field {'field_14': 'Letter to family'}>, 'field_15': <Field {'field_15': '<p>Feb 10, 11</p><p><br /></p>'}>, 'field_25': <Field {'field_25': '<p>Exposure 4</p>'}>, 'field_28': <Field {'field_28': 'https://api.knack.com/v1/applications/5faae3b10442ac00165da195/download/asset/60284589bc3817001bf307df/ceccb763ae294700bd3a671dba138ca6.jpeg'}>, 'field_26': <Field {'field_26': 'Fraser Health Authority'}>, 'field_30': <Field {'field_30': 'Current'}>}
>>> r.field_defs
[<FieldDef 'id'>, <FieldDef 'Address'>, <FieldDef 'City '>, <FieldDef 'School District'>, <FieldDef 'id'>, <FieldDef 'Notification Date'>, <FieldDef 'School'>, <FieldDef 'Notification'>, <FieldDef 'Exposure Dates'>, <FieldDef 'Extra Info'>, <FieldDef 'Documentation'>, <FieldDef 'Health Region'>, <FieldDef 'Status'>, <FieldDef 'id'>, <FieldDef 'id'>, <FieldDef 'id'>, <FieldDef 'id'>, <FieldDef 'id'>]
"""


class SimpleHTMLDataParser(html.parser.HTMLParser, object):
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
    def __init__(self, data, shtmlparser):
        self.data = data
        self.id = self.data.get("id")
        self.notification_date = self.data.get("field_16")
        self.notification_timestamp = self.data.get("field_16_raw", {}).get(
            "unix_timestamp"
        )
        self.school = self.data.get("field_13_raw", [{}])[0].get("identifier")
        self.city = self.data.get("field_7_raw", [{}])[0].get("identifier")
        self.school_district = self.data.get("field_18_raw", [{}])[0].get("identifier")
        self.health_region = self.data.get("field_26_raw", [{}])[0].get("identifier")
        shtmlparser.feed(self.data.get("field_15_raw", ""))
        # exposure dates and extra info are raw html like: <p>Feb 10, 11</p><p><br /></p>
        # so we parse the data out with shtmlparser and escape commas
        self.exposure_dates = shtmlparser.get_data()
        if "," in self.exposure_dates:
            self.exposure_dates = f'"{self.exposure_dates}"'
        shtmlparser.feed(self.data.get("field_25_raw", ""))
        self.extra_info = shtmlparser.get_data()
        if "," in self.extra_info:
            self.extra_info = f'"{self.extra_info}"'

    def __str__(self):
        return f"{self.notification_date}, {self.school}, {self.city}, {self.school_district}, {self.health_region}, {self.exposure_dates}, {self.extra_info}"


def test():

    parser = SimpleHTMLDataParser()
    parser.feed("<p>Feb 10, 11</p><p><br /></p>")
    assert parser.get_data() == "Feb 10, 11"
    parser.feed("<p>Exposure 4</p>")
    assert parser.get_data() == "Exposure 4"

    test_record = None
    with open("test.json", "r") as tf:
        test_record = json.load(tf)
    expected = """02/13/2021, Mountain Meadows Elementary, Port Moody, 43, Fraser Health Authority, "Feb 10, 11", Exposure 4"""
    tr = CovidEventRecord(test_record, parser)
    print(tr)
    assert str(tr) == expected


if __name__ == "__main__":
    test()
