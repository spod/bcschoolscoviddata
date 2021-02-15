# bcschoolscoviddata
Python experiments with the [BC School Covid Tracker](https://bcschoolcovidtracker.knack.com/bc-school-covid-tracker#home/)

## Quick Start
* Clone the repo & set up a python virtual env
* `$ pip install knackpy`
* `$ python dump_data.py`
* `$ python json_to_csv.py data/bc_school_covid_events_raw_data.json data/bc_school_covid_events_raw_data.csv`
* Explore `data/bc_school_covid_events_raw_data.csv` ...

## Scripts
* `dump_data.py` - retrieve all exposure events and save them to `data/bc_school_covid_events_raw_data.json` - note this isn't incremental etc and takes a few seconds to run so don't run it repeatedly or even more than daily!

* `json_to_csv.py` - script which parses json output from `dump_data.py` and generate a .csv file for import to excel or other analysis tools

* `knack_exp.py` - quick start for exploring bc schools covid data in a python repl, run as `python -i knack_exp.py`, exports the following globals:
  * `app` - a knackpy.App instance for the Covid Tracker Knack app, sample `app.info()`, see Knackpy docs below for more
  * `last5` - a list containing the 5 latest records from the Covid Tracker main Covid Events tab.
  * `r` - the latest covid event record, try eg `r.names()` or `r.values()`

## References
* [facebook.com/BCSchoolCovidTracker](https://www.facebook.com/BCSchoolCovidTracker)
* [Knack Developer API Docs](https://docs.knack.com/docs/introduction-to-the-api)
* [Knackpy](https://github.com/cityofaustin/knackpy) & [Knackpy User Guide](https://cityofaustin.github.io/knackpy/docs/user-guide/)
* [BC OpenData -  Education Analytics BC Schools - Class Size Class Size 2006-07 to 2020-21](https://catalogue.data.gov.bc.ca/dataset/bc-schools-class-size/resource/63e52d04-9431-44ea-93d4-5251e04a239c)
