#!/usr/bin/env python3

import argparse
import os
import glob
import collections
import csv
import re

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", dest="output")
parser.add_argument("indirs", nargs="+")
args = parser.parse_args()

counts = collections.defaultdict(int)

for indir in args.indirs:
    for f in glob.iglob(os.path.join(indir, "*.tag")):
        key = re.match(".*/([^/]*?)(\\.[0-9]{3})?\\.xml\\.tag$", f).group(1)
        with open(f, "r") as infile:
            for line in infile.readlines():
                if line.strip() == "":
                    continue
                word, tag = line.split("\t")
                if tag not in (".", ",") and word not in ("(", ")"):
                    # For whatever reason, parentheses tend to be mistagged as
                    # nominal things (N, NPR, NUM, etc.)  Ideally we'd look
                    # only at the tag to determine wordhood, but until that's
                    # fixed we need to handle it.
                    counts[key] = counts[key] + 1

with open(args.output, "w") as out:
    writer = csv.writer(out)
    writer.writerow(["file", "words"])
    for f in sorted(counts.keys()):
        writer.writerow([f, counts[f]])
