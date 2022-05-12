"""
Run this file to compute the age of the MP

Note: We use the formula
    age = 2022 - year_of_birth
so the result might be off by one year at most.
"""

import pandas as pd
from datetime import datetime, date


INPATH = "processed_data/parlementaires.csv"
THISYEAR = 2022
OUTPATH = "processed_data/parlementaires_with_age.csv"


# Load the list of MP

mps = pd.read_csv(INPATH)


# Auxiliary function

def age(mp):
    """ Compute the age of a MP as 2022 - year_of_birth """

    birthdate = mp['birthDate']
    birthyear = int(birthdate[0:4])
    return THISYEAR - birthyear


# Compute the ages, sort accordingly and store the result

ages = mps.apply(lambda mp: age(mp), axis=1)
mps.insert(0, 'Age', ages)
mps = mps.sort_values('Age')
mps.to_csv(OUTPATH)
