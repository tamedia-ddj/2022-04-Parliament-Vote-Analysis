import pandas as pd
import requests, json
import matplotlib.pyplot as plt

# Gather data
"""
#parlementaires = pd.read_excel('parlementaires.xlsx')
votes_49 = [
    (
        pd.read_excel(f'sessions/{vote}.xlsx', header=8, usecols='A:K'),
        pd.read_excel(f'sessions/{vote}.xlsx', header=1, usecols=(
            lambda n: 'Unnamed' not in str(n) and n != 'CouncillorBioId'))
    )
    for vote in list(range(4901, 4921))
]
votes_50 = [
    (
        pd.read_excel(f'sessions/{vote}.xlsx', header=8, usecols='A:K'),
        pd.read_excel(f'sessions/{vote}.xlsx', header=1, usecols=(
            lambda n: 'Unnamed' not in str(n) and n != 'CouncillorBioId'))
    )
    for vote in list(range(5001, 5020))
]

parlementaires_49_ids = set([id for vote in votes_49 for id in vote[1].columns])
parlementaires_50_ids = set([id for vote in votes_50 for id in vote[1].columns])

def rcv(id):
    return requests.get(
        f'http://ws-old.parlament.ch/councillors/{id}?format=json',
        headers={'Accept': 'application/json', 'Accept-Language': 'fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5'}
    ).json()

parlementaires_49 = [
    rcv(id)
    for id in parlementaires_49_ids
]
parlementaires_50 = [
    rcv(id)
    for id in parlementaires_50_ids
]

IN_LABELS = ['cantonName', 'faction', 'party', 'birthDate', 'firstName', 'lastName', 'gender', 'councilMemberships']
OUT_LABELS = ['cantonName', 'faction', 'party', 'birthDate', 'firstName', 'lastName', 'gender', 'entryDate']

parlementaires_49 = [[parlementaire[label] if label in parlementaire else None for label in IN_LABELS] for parlementaire in parlementaires_49]
parlementaires_50 = [[parlementaire[label] if label in parlementaire else None for label in IN_LABELS] for parlementaire in parlementaires_50]

for i in range(len(parlementaires_49)):
    parlementaires_49[i][7] = parlementaires_49[i][7][0]['entryDate']
parlementaires_49 = pd.DataFrame(parlementaires_49, index=parlementaires_49_ids, columns=OUT_LABELS).T
for i in range(len(parlementaires_50)):
    parlementaires_50[i][7] = parlementaires_50[i][7][0]['entryDate']
parlementaires_50 = pd.DataFrame(parlementaires_50, index=parlementaires_50_ids, columns=OUT_LABELS).T

parlementaires_49.fillna('None').to_csv('parlementaires_49.csv')
parlementaires_50.fillna('None').to_csv('parlementaires_50.csv')
"""

parlementaires_49 = pd.read_csv('parlementaires_49.csv', index_col=0).T
parlementaires_50 = pd.read_csv('parlementaires_50.csv', index_col=0).T

parlementaires_49['year'] = pd.DatetimeIndex(parlementaires_49['birthDate']).year
parlementaires_49['age_49'] = parlementaires_49['year'].apply(lambda year: 2022 - year)
parlementaires_50['year'] = pd.DatetimeIndex(parlementaires_50['birthDate']).year
parlementaires_50['age_50'] = parlementaires_50['year'].apply(lambda year: 2022 - year)

parlementaires_49['age_49'].plot.hist(xlim=(0, 100),fc=(0, 0, 1, 0.5))
parlementaires_50['age_50'].plot.hist(xlim=(0, 100),fc=(1, 0, 0, 0.5))
plt.legend(loc='upper left')
plt.savefig('ages_repartition/lesislatures.png')
