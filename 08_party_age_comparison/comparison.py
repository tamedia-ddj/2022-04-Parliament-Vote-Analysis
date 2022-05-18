import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

parlementaires = pd.read_csv(f'../../parlement/donnees/parlementaires.csv', index_col=0).T
parties = list(set(parlementaires['party']))

ages = []
data_parties = []

def median(l):
    l = sorted(l)
    if len(l) % 2 == 1:
        return l[len(l) // 2]
    else:
        return (l[len(l) // 2] + l[len(l) // 2 + 1]) // 2

for party in parties:
    parlementaires_party = parlementaires[parlementaires['party'] == party]
    if len(parlementaires_party) <= 10:
        continue

    parlementaires_party['year'] = pd.DatetimeIndex(parlementaires_party['birthDate']).year
    parlementaires_party['age'] = parlementaires_party['year'].apply(lambda year: 2022 - year)

    ages.append(list(parlementaires_party['age']))
    data_parties.append(f'{party} ({len(parlementaires_party)})')

parties_ages = list(zip(ages, data_parties))
parties_ages.sort(key=lambda t: median(t[0]))

ages = [pa[0] for pa in parties_ages]
data_parties = [pa[1] for pa in parties_ages]

fig, ax = plt.subplots()
#ax.violinplot(tuple(ages), vert=False, widths=.7, quantiles=[[.25, .5, .75]]*len(ages))
#ax.violinplot(tuple(ages), vert=False, widths=.7, showmeans=True)
ax.violinplot(tuple(ages), vert=False, widths=.7, quantiles=[[.5]]*len(ages))
ax.set_xlabel('Age')
ax.set_yticks(np.arange(1, len(data_parties) + 1), labels=data_parties)
plt.show()
