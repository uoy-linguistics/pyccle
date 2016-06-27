#!/usr/bin/env python3

import pandas as pd
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", dest="output")
parser.add_argument("files", nargs="+")
args = parser.parse_args()

res = pd.read_csv(args.files[0])

for f in args.files[1:]:
    res = res.merge(pd.read_csv(f), on="file", how="outer")

res.to_csv(args.output, index=False)
