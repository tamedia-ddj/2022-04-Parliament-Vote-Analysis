"""
Run this file to convert xlsx files to csv files (pandas reads csv
much faster).
"""

import pandas as pd

input = "votes_finaux.xlsx"
output = "votes_finaux.csv"

df = pd.read_excel(input)
df.to_csv(output, encoding='utf-8')
