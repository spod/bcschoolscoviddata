# bcschoolscoviddata
Python experiments with the [BC School Covid Tracker](https://bcschoolcovidtracker.knack.com/bc-school-covid-tracker#home/)

## Quick Start
* Clone the repo & set up a python virtual env
* `$ pip install knackpy`
* `$ python dump_data.py`

## Scripts
* `dump_data.py` - retrieve all exposure events and save them to `raw_data.json` - note this isn't incremental etc and takes a few seconds to run so don't run it repeatedly or even more than daily!

* `json_to_csv.py` - incomplete, script to take output from `dump_data.py` and generate a .csv file for import to excel or other analysis

* `knack_exp.py` - quick start for exploring bc schools covid data in a python repl, run as `python -i knack_exp.py`, exports the following globals:
  * `app` - a knackpy.App instance for the Covid Tracker Knack app, sample `app.info()`, see Knackpy docs below for more
  * `last5` - a list containing the 5 latest records from the Covid Tracker main Covid Events tab.
  * `r` - the latest covid event record, try eg `r.names()` or `r.values()`

## References
* [facebook.com/BCSchoolCovidTracker](https://www.facebook.com/BCSchoolCovidTracker)
* [Knack Developer API Docs](https://docs.knack.com/docs/introduction-to-the-api)
* [Knackpy](https://github.com/cityofaustin/knackpy) & [Knackpy User Guide](https://cityofaustin.github.io/knackpy/docs/user-guide/)