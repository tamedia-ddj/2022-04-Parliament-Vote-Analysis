import pandas as pd
import matplotlib.pyplot as plt

parlementaires = pd.read_csv(f'../data/parlementaires.csv', index_col=0).T
parties = set(parlementaires['party'])

for party in parties:
    plt.figure()
    parlementaires_party = parlementaires[parlementaires['party'] == party]
    parlementaires_party['year'] = pd.DatetimeIndex(parlementaires_party['birthDate']).year
    parlementaires_party['age'] = parlementaires_party['year'].apply(lambda year: 2022 - year)

    parlementaires_party['age'].plot.hist(xlim=(0, 100))
    plt.title(f'Age repartition for {party}')
    plt.savefig(f'{party}.png')
