#!/usr/bin/env python3

import pandas as pd
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", dest="output")
parser.add_argument("files", nargs="+")
args = parser.parse_args()

dfs = list(map(pd.read_csv, args.files))

pd.concat(dfs).to_csv(args.output, index=False)
