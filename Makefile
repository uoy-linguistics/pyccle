@PHONY: metadata upload-metadata

EEBO_PATH=/home/aecay/hdd/eebo
ECCO_PATH=/home/aecay/hdd/ecco

EEBO_TAGGED_PATH=/home/aecay/hdd/eebo-tagged
ECCO_TAGGED_PATH=/home/aecay/hdd/ecco-tagged

metadata/dates-eebo.csv:
	python3 scripts/dates-script.py $(EEBO_PATH) 1472 1701 metadata/dates-eebo-tmp.csv
	python3 scripts/concat-csv.py -o $@ metadata/dates-eebo-tmp.csv metadata/dates-eebo-manual.csv

metadata/dates-ecco.csv:
	python3 scripts/dates-script.py $(ECCO_PATH) 1699 1801 $@

metadata/dates.csv: metadata/dates-eebo.csv metadata/dates-ecco.csv
	python3 scripts/concat-csv.py -o $@ $^

metadata/word-counts.csv:
	python3 scripts/count-words.py -o $@ $(EEBO_TAGGED_PATH) $(ECCO_TAGGED_PATH)

metadata/metadata.csv: metadata/dates.csv metadata/word-counts.csv
	python3 scripts/merge-csv.py -o $@ $^

metadata: metadata/metadata.csv

upload-metadata: metadata
	scp metadata/metadata.csv babel.ling.upenn.edu:/histcorpora/TCP/EEBO-TAGGED/metadata/
