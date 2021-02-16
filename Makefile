.PHONY: update gonow fetch push

gonow:	fetch update

fetch:
	./dump_data.py

update:
	# raw_data.csv is used for https://gist.github.com/spod/822be2b9a4dfc50a54e24042e9564532
	./json_to_csv.py data/bc_school_covid_events_raw_data.json data/raw_data.csv
	./json_to_csv.py data/bc_school_covid_events_raw_data.json data/bc_school_covid_events_raw_data.csv

	# execute leaderboard notebook using runipy from virtualenv
	[ -f /home/michael/.pyenv/bc_schools_knack/bin/activate ] && . /home/michael/.pyenv/bc_schools_knack/bin/activate && runipy ./leaderboards.ipynb

push:
	@# horrid "one liners" to update github gists with .csv files
	@# assumes nice symlinks to clones of the relevant gist repos
	@# gists/raw_data -> https://gist.github.com/spod/822be2b9a4dfc50a54e24042e9564532
	@# gists/leaderboard -> https://gist.github.com/spod/a5726637b1b4977503a59d809460489f
	@#
	@# note: git status -porcelain=v1 | grep "M" will error out if there are no changes
	@#
	-[ -d /home/michael/Source/gists/raw_data/ ] && \
	cp data/raw_data.csv /home/michael/Source/gists/raw_data/. && \
	cd /home/michael/Source/gists/raw_data/ && \
	git status --porcelain=v1 | grep "M" && git commit -am "update" && git push && cd -

	-[ -d /home/michael/Source/gists/leaderboard/ ] && \
	cp data/leaderboard.csv /home/michael/Source/gists/leaderboard/. && \
	cd /home/michael/Source/gists/leaderboard/ && \
	git status --porcelain=v1 | grep "M" && git commit -am "update" && git push && cd -