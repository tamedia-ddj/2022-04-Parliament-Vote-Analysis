"""
Run this file to compute the age of the MP
"""

import pandas as pd
from datetime import datetime, timezone
import matplotlib.pyplot as plt

INPATH = "../processed_data/parlementaires.csv"
OUTPATH = "../processed_data/parlementaires_with_age.csv"

# Load the list of MP
dfp = pd.read_csv(INPATH)


def age(birth_date):
    """Compute the age of a MP as NOW - date_of_birth"""
    age_float = (datetime.now(tz=timezone.utc) - birth_date).days / 365.25
    return int(round(age_float))


# Compute the ages, sort accordingly and store the result
ages = pd.to_datetime(dfp["birthDate"]).apply(lambda bd: age(bd))
dfp.insert(0, "Age", ages)

# Compute the ages, sort accordingly and store the result
dfp.sort_values("Age", inplace=True)
dfp.to_csv(OUTPATH)
