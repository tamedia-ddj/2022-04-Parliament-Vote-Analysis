"""
Use this file to sort the votes by Rice index.

It does the same as the notebook, but it is easier to run
from the command line.
"""

import pandas as pd


# Change the paths if you want

INPATH = "../processed_data/"
TO_SORT = ["votes_finaux", "votes"]  # files that will be sorted
OUTPATH = "../processed_data/"


# Auxiliary functions

def count(string, row):
    """ Count the number of occurrences of `string` in the row """

    if row.str.contains(string).any():
        return row.value_counts()[string]
    else:
        return 0


def rice_index(row):
    """ Compute the Rice index of the row """

    count_yes = count('Oui', row)
    count_no = count('Non', row)
    return abs(count_yes - count_no) / (count_yes + count_no)


# Sort the files in `TO_SORT`

for file in TO_SORT:
    filepath = f"{INPATH}{file}.csv"
    print(f"Processing {filepath}")

    # Compute the rice index of each vote and sort the votes accordingly
    votes = pd.read_csv(filepath)
    rice_indices = votes.apply(lambda row: rice_index(row), axis=1)
    votes.insert(0, 'Rice index', rice_indices)
    votes = votes.sort_values('Rice index')

    # Export the sorted votes
    outpath = f"{OUTPATH}{file}_sorted_RI.csv"
    votes.to_csv(outpath)
    print(f"Results stored in {outpath}")
    print("")
