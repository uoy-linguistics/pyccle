#!/usr/bin/env python3

import os
import fnmatch
import sys
import csv

import dates

hdrfiles = []
for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    for xf in fnmatch.filter(filenames, "*.hdr"):
        hdrfiles.append(dirpath + "/" + xf)

metadata = dates.date_files(hdrfiles, int(sys.argv[2]), int(sys.argv[3]))

with open(sys.argv[4], "w") as d:
    writer = csv.DictWriter(d, fieldnames=["file", "date", "author", "dob", "dod"])
    writer.writeheader()
    for text in sorted(metadata, key=lambda x: x['file']):
        writer.writerow(text)
