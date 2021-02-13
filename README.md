# bcschoolscoviddata
Python experiments with the [BC School Covid Tracker](https://bcschoolcovidtracker.knack.com/bc-school-covid-tracker#home/)

## Quick Start
* Clone the repo & set up a python virtual env
* `$ pip install knackpy`
* `$ python dump_data.py`

## Scripts
* `dump_data.py` - retrieve all exposure events and save them to `raw_data.json` - note this isn't incremental etc and takes a few seconds to run so don't run it repeatedly

## References
* [facebook.com/BCSchoolCovidTracker](https://www.facebook.com/BCSchoolCovidTracker)
* [Knack Developer API Docs](https://docs.knack.com/docs/introduction-to-the-api)
* [Knackpy](https://github.com/cityofaustin/knackpy) & [Knackpy User Guide](https://cityofaustin.github.io/knackpy/docs/user-guide/)