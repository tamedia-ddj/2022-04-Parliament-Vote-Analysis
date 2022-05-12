# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import pandas as pd
votes = pd.read_excel('votes.xlsx')
votes_nonempty = votes[votes['DivisionText'].notna()]
votes_finaux = votes_nonempty[(votes_nonempty['DivisionText'] == 'Schlussabstimmung') | (votes_nonempty['DivisionText'] == 'Vote final')]

votes_finaux.to_excel("votes_finaux.xlsx")