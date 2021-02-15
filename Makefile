.PHONY: update gonow fetch

gonow:	fetch update

fetch:
	./dump_data.py

update:
	# raw_data.csv is used for https://gist.github.com/spod/822be2b9a4dfc50a54e24042e9564532
	./json_to_csv.py data/bc_school_covid_events_raw_data.json data/raw_data.csv
	./json_to_csv.py data/bc_school_covid_events_raw_data.json data/bc_school_covid_events_raw_data.csv
