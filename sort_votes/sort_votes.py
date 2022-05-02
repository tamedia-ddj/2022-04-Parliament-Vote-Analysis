"""
Use this file to sort the votes by Rice index.

It does the same as the notebook, but it is easier to run
from the command line.
"""

import pandas as pd


# Load the votes (change the paths if you want to sort another kind of votes)

INPATH = "../data/votes_finaux.csv"
OUTPATH = "votes_finaux_sorted_RI.csv"

votes = pd.read_csv(INPATH)


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


# Compute the rice index of each vote and sort the votes accordingly

rice_indices = votes.apply(lambda row: rice_index(row), axis=1)
votes.insert(0, 'Rice index', rice_indices)
votes = votes.sort_values('Rice index')


# Export the sorted votes

votes.to_csv(OUTPATH)
print(f"Results stored in {OUTPATH}")
