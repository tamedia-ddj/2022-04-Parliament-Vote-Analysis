import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

CURRENT_YEAR = 2022

def calcVoteWeights(dfp, nb_age_groups):
   # convert birthdate into datetime format
    dfp['birthDate'] = pd.to_datetime(dfp['birthDate']) 

    age_limits = calcAgeLimits(dfp, nb_age_groups)

    nb_total = dfp.count()["ID"]
    parties = dfp["party"].unique()

    vote_weights = {}
    for party in parties:
        dfp_party = dfp.loc[dfp["party"] == party]
        nb_in_party = dfp_party.count()["ID"]
        prob_party = nb_in_party / nb_total

        vote_weights[party] = {}
        for age_str, age_limit in age_limits.items():
            dfp_party_age = dfp.loc[(dfp["birthDate"] >= age_limit[0]) & (dfp["birthDate"] <= age_limit[1])]
            nb_in_party_age = dfp_party_age.count()["ID"]
            prob_party_age = nb_in_party_age / nb_in_party

            vote_weights[party][age_str] = prob_party / prob_party_age
    return vote_weights, age_limits

def calcFakeWeights(dfp, nb_age_groups):
    age_limits = calcAgeLimits(dfp, nb_age_groups)
    parties = dfp["party"].unique()

    fake_weights = {}
    for party in parties:
        fake_weights[party] = {}
        for age_str in age_limits.keys():
            fake_weights[party][age_str] = 1
    return fake_weights


def calcAgeLimits(dfp, nb_age_groups):
    # convert birthdate into datetime format
    dfp['birthDate'] = pd.to_datetime(dfp['birthDate']) 
    # sort df_parlament after age: index 0 = oldest, index 1 = youngest
    dfp_sorted = dfp.sort_values("birthDate")

    nb_parlamentarians = dfp_sorted.count()["ID"]
    nb_parl_per_group = int(np.floor(nb_parlamentarians/nb_age_groups))

    age_limits = {}
    index_limit = 0
    last_limit = 0
    for i in range(nb_age_groups):
        index_limit += nb_parl_per_group

        if i < nb_parlamentarians%nb_age_groups:
            index_limit += 1

        age_str = str(CURRENT_YEAR-dfp_sorted.iloc[index_limit-1]['birthDate'].year) + "-" + str(CURRENT_YEAR-dfp_sorted.iloc[last_limit]['birthDate'].year)
        age_limits[age_str] = [ dfp_sorted.iloc[last_limit]['birthDate'], dfp_sorted['birthDate'].iloc[index_limit-1] ]

        last_limit = index_limit      
    return age_limits

def calcWeightedRI(dfp, dfv, vote_weights, age_limits):

    nb_votes = dfv.count()["AffairId"]

    weighted_RI = {}
    for age_str in age_limits.keys():
        weighted_RI[age_str] = np.zeros((nb_votes))

    for v_index in dfv.index:

        weighted_votes = {}
        for age_str in age_limits.keys():
            weighted_votes[age_str] = [0,0]

        for p_index in dfp.index:
            ID = str(dfp["ID"][p_index])
            party = dfp["party"][p_index]
            birthdate = dfp["birthDate"][p_index]
            age_str = determineAgeStr(age_limits, birthdate)

            vote_str = dfv[ID][v_index]
            if vote_str == "Oui":
                weighted_votes[age_str][1] += vote_weights[party][age_str]
            elif vote_str == "Non":
                weighted_votes[age_str][0] += vote_weights[party][age_str]

        total_oui = 0
        total_non = 0
        for votes_age_group in weighted_votes.values():
            total_oui += votes_age_group[1]
            total_non += votes_age_group[0]
        reference_RI = abs(total_oui-total_non)/(total_oui+total_non)

        for age_str, age_RI in weighted_RI.items():
            age_RI[v_index] = abs(weighted_votes[age_str][1]-weighted_votes[age_str][0])/(weighted_votes[age_str][1]+weighted_votes[age_str][0])
            age_RI[v_index] /= reference_RI

    return weighted_RI


def determineAgeStr(age_limits, birthdate):
    for age_str, age_limit in age_limits.items():
        if birthdate>=age_limit[0] and birthdate<=age_limit[1]:
            return age_str
    return "ERROR"

def plotPartyBias(weighted_RI, normal_RI):
    fig = plt.figure(figsize=(9, 6))
    ax1 = fig.add_subplot()
    
    weighted_data = []
    normal_data = []
    error_data = []
    labels = []
    for age_str in weighted_RI.keys():
        weighted_data.append(np.mean(weighted_RI[age_str]))
        normal_data.append(np.mean(normal_RI[age_str]))
        error_data.append(np.mean(weighted_RI[age_str] - normal_RI[age_str]))
        labels.append(age_str)

    X_axis = np.arange(len(labels))
    ax1.bar(X_axis - 0.25, weighted_data, color = 'b', width = 0.25, label="Mean weighted votes")
    ax1.bar(X_axis + 0.0, normal_data, color = 'g', width = 0.25, label="Mean unweighted votes")
    ax1.bar(X_axis + 0.25, error_data, color = 'r', width = 0.25, label="Mean error")

    ax1.legend()
    plt.title("Bias due to age distribution of parties")
    plt.xticks(X_axis, labels)
    plt.xlabel("Age groups")
    plt.ylabel("RI(age group) / RI(all persons)")
    plt.grid()
    fig.savefig("party_bias.png")  

if __name__ == "__main__":
    #import dataframes
    print(os.getcwd())
    dfp = pd.read_csv('../processed_data/parlementaires.csv')
    dfv = pd.read_csv('../processed_data/votes_finaux.csv')

    dfp.rename(columns={'Unnamed: 0.1':'ID'}, inplace=True)

    nb_age_groups = 3
    
    vote_weights, age_limits = calcVoteWeights(dfp, nb_age_groups)
    weighted_RI = calcWeightedRI(dfp, dfv, vote_weights, age_limits)

    fake_weights = calcFakeWeights(dfp, nb_age_groups)
    normal_RI = calcWeightedRI(dfp, dfv, fake_weights, age_limits)

    plotPartyBias(weighted_RI, normal_RI)
           