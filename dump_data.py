#! /usr/bin/env python

"""Quick script to dump the raw exposure event data from BC Schools Covid Tracker."""

# https://bcschoolcovidtracker.knack.com/bc-school-covid-tracker#home/
# https://www.facebook.com/BCSchoolCovidTracker

import json
import sys

DATA_FILE = "data/bc_school_covid_events_raw_data.json"

# pip install knackpy
try:
    import knackpy
except ImportError:
    print(
        "Please install knackpy, see https://cityofaustin.github.io/knackpy/docs/user-guide/#installation"
    )
    sys.exit(1)

# extracted from web app
APP_ID = "5faae3b10442ac00165da195"
# extracted from firefox debugger by setting a breakpoint for xhr events
API_KEY = "renderer"

# fetch events data from covid tracker knack app
app = knackpy.App(app_id=APP_ID, api_key=API_KEY)

print("Fetching all events, this will take a few seconds ...")
events_records = app.get("Covid Events")

# build a list of raw knack json for all covid event records
raw = []
for e in events_records:
    raw.append(e.raw)

print(f"Saving to '{DATA_FILE}' ...")
with open(DATA_FILE, "w") as f:
    json.dump(raw, f, indent=2, separators=(",", ": "))

print("Done!")
