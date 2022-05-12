import pandas as pd
import requests, json

#parlementaires = pd.read_excel('parlementaires.xlsx')
votes = [
    (
        pd.read_excel(f'sessions/{vote}.xlsx', header=8, usecols='A:K'),
        pd.read_excel(f'sessions/{vote}.xlsx', header=1, usecols=(
            lambda n: 'Unnamed' not in str(n) and n != 'CouncillorBioId'))
    )
    for vote in list(range(4901, 4921)) + list(range(5001, 5020)) + list(range(5101, 5114))
]

parlementaires_ids = set([id for vote in votes for id in vote[1].columns])

votes_concat = [
    pd.concat([
        (
            vote[1][id][7:] if id in vote[1]
            else pd.Series([None for _ in range(vote[0].shape[0])], index=vote[1][7:].index, name=id)
        ) for vote in votes
    ]) for id in parlementaires_ids
]
votes_concat = pd.concat(votes_concat, axis=1)
affaires_concat = pd.concat([vote[0] for vote in votes])


votes_concat.reset_index(drop=True, inplace=True)
affaires_concat.reset_index(drop=True, inplace=True)
votes_with_affairs = pd.concat([affaires_concat, votes_concat], axis=1)

votes_with_affairs.to_excel('donnees/votes.xlsx')
votes_with_affairs.to_csv('donnees/votes.csv')

def rcv(id):
    #print(id)
    return requests.get(
        f'http://ws-old.parlament.ch/councillors/{id}?format=json',
        headers={'Accept': 'application/json', 'Accept-Language': 'fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5'}
    ).json()

parlementaires = [
    rcv(id)
    for id in parlementaires_ids
]

IN_LABELS = ['cantonName', 'faction', 'party', 'birthDate', 'firstName', 'lastName', 'gender', 'councilMemberships']
OUT_LABELS = ['cantonName', 'faction', 'party', 'birthDate', 'firstName', 'lastName', 'gender', 'entryDate']
parlementaires = [[parlementaire[label] if label in parlementaire else None for label in IN_LABELS] for parlementaire in parlementaires]
for i in range(len(parlementaires)):
    parlementaires[i][7] = parlementaires[i][7][0]['entryDate']
parlementaires = pd.DataFrame(parlementaires, index=parlementaires_ids, columns=OUT_LABELS).T

parlementaires.fillna('None').to_excel('donnees/parlementaires.xlsx')
parlementaires.fillna('None').to_csv('donnees/parlementaires.csv')
