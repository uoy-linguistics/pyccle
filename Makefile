@PHONY: metadata

EEBO_PATH=/home/aecay/hdd/eebo
ECCO_PATH=/home/aecay/hdd/ecco

metadata: metadata/dates-eebo.csv metadata/dates-ecco.csv

metadata/dates-eebo.csv:
	python3 scripts/dates-script.py $(EEBO_PATH) 1472 1701 metadata/dates-eebo-tmp.csv
	cat metadata/dates-eebo-tmp.csv metadata/dates-eebo-manual.csv | sort > $@

metadata/dates-ecco.csv:
	python3 scripts/dates-script.py $(ECCO_PATH) 1699 1801 $@
