#!/usr/bin/env python3

import os
import fnmatch
import sys

import dates

hdrfiles = []
for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    for xf in fnmatch.filter(filenames, "*.hdr"):
        hdrfiles.append(dirpath + "/" + xf)

datesdict = dates.date_files(hdrfiles, int(sys.argv[2]), int(sys.argv[3]))

with open(sys.argv[4], "w") as d:
    for k, v in sorted(datesdict.items()):
        if v is not None:
            d.write("%s,%s\n" % (k, v))
