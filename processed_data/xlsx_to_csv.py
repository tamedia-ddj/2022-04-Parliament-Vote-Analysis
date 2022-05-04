"""
Run this file to convert xlsx files to csv files in batch (pandas
reads csv much faster).
"""

import pandas as pd


INPATH = "../data/"
TO_CONVERT = ["votes", "votes_finaux"]
OUTPATH = "../processed_data/"


# Function to convert each file

def xlsx_to_csv(filename):
    filepath = f"{INPATH}{filename}.xlsx"
    outpath = f"{OUTPATH}{filename}.csv"

    df = pd.read_excel(filepath)
    df.to_csv(outpath, encoding='utf-8', header=True)


# Convert all the files specified in `TO_CONVERT`

for filename in TO_CONVERT:
    xlsx_to_csv(filename)
