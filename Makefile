.PHONY: update

update:
	./dump_data.py
	./json_to_csv.py data/bc_school_covid_events_raw_data.json data/raw_data.csv