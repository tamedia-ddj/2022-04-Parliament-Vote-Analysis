import pandas as pd
from math import log
import matplotlib.pyplot as plt

parlementaires = pd.read_excel(f'donnees/parlementaires.xlsx', index_col=0).T

groupes = set(parlementaires['faction'])
CURRENT_YEAR = 2022
AGE_CATS = [(0, 40), (40, 50), (50, 60), (60, 70), (70, 100)]

parlementaires_per_group = {gp: list(parlementaires[parlementaires['faction'] == gp].index) for gp in groupes}
years = pd.to_datetime(parlementaires['birthDate']).dt.year
parlementaires_per_age_cat = {cat: list(years[cat[0] <= CURRENT_YEAR - years][CURRENT_YEAR - years < cat[1]].index) for cat in AGE_CATS}

votes = pd.read_excel(f'donnees/votes.xlsx', usecols=(lambda n: str(n).isdigit()))
votes_per_group = {gp: votes[votes.columns[votes.columns.isin(parlementaires_per_group[gp])]] for gp in groupes}
votes_per_age_cat = {cat: votes[votes.columns[votes.columns.isin(parlementaires_per_age_cat[cat])]] for cat in AGE_CATS}

age_inds = []
group_inds = []
for vote in votes.index:
    # Groups
    gp_inds_sum = 0
    nb_gps = 0
    for gp in groupes:
        gp_votes = votes_per_group[gp].loc[vote]

        nb_yes = gp_votes[gp_votes == 'Oui'].count()
        nb_no = gp_votes[gp_votes == 'Non'].count()

        if nb_yes + nb_no == 0:
            continue

        gp_inds_sum += abs(nb_yes - nb_no) / (nb_yes + nb_no)
        nb_gps += 1

    if nb_gps == 0:
        continue

    # Ages
    ages_inds_sum = 0
    nb_ages_gps = 0
    for cat in AGE_CATS:
        age_gp_votes = votes_per_age_cat[cat].loc[vote]

        nb_yes = age_gp_votes[age_gp_votes == 'Oui'].count()
        nb_no = age_gp_votes[age_gp_votes == 'Non'].count()

        if nb_yes + nb_no == 0:
            continue

        ages_inds_sum += abs(nb_yes - nb_no) / (nb_yes + nb_no)
        nb_ages_gps += 1

    if nb_ages_gps == 0:
        continue

    # Add data
    age_inds.append(ages_inds_sum / nb_ages_gps)
    group_inds.append(gp_inds_sum / nb_gps)
    
print(group_inds, age_inds)
plt.scatter(group_inds, age_inds)
plt.xlabel("Average group RI")
plt.ylabel("Average age group RI")
plt.show()

for i in range(len(group_inds)):
    if age_inds[i] >= group_inds[i]:
        print(i)

"""
for gp in groupes:
    es = []
    for vote in votes.index:
        gp_votes = votes_per_group[gp].loc[vote]

        nb_yes = gp_votes[gp_votes == 'Oui'].count()
        nb_no = gp_votes[gp_votes == 'Non'].count()

        if nb_yes + nb_no == 0:
            es.append(es[-1] if len(es) > 0 else 0)
            continue

        proba_yes = nb_yes / (nb_yes + nb_no)
        proba_no = nb_no / (nb_yes + nb_no)

        e = - proba_yes * (log(proba_yes) if proba_yes > 0 else 0) - proba_no * (log(proba_no) if proba_no > 0 else 0)
        
        es.append(1 - e)

    plt.plot(es, label=gp)

plt.legend()
plt.show()
"""
