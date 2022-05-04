"""
Run this file to convert the xlsx file of MP to a csv 
file (the MP files need a special treatment because it
is transposed)
"""


import pandas as pd

INPATH = "../data/parlementaires.xlsx"
OUTPATH = "../processed_data/parlementaires.csv"

# Read and transpose the xlsx file
mp = pd.read_excel(INPATH)
mp = mp.transpose()

# Remove the first row (it contains to column indices)
mp.to_csv(OUTPATH)  # This might not be the most elegant solution
mp = pd.read_csv(OUTPATH, skiprows=1)
mp.to_csv(OUTPATH)
