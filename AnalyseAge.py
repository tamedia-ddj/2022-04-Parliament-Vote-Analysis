#from cProfile import label
from unittest import skip
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

CURRENT_YEAR = 2022

def extractParty(dataframe, partyName, mask=None):
    """
    Inputs:
        dataframe: panda dataframe of parlamentaires.xlsx
        partyName: name of the party
        mask: preprocess dataframe by taking only indeces defined by mask
    Output:
        numOfPOI: Parlementaire Of Interest from the corresponding party
    """
    if(mask): # if there was a mask provided to the function then apply it
        dataframe = dataframe.loc[mask]
    
    numOfPOI = dataframe.loc[dataframe['party'] == partyName].index #POI = Parlementaire Of Interest
    return numOfPOI

def extractAge(df_parlament, df_votes, base_year=CURRENT_YEAR, given_age_groups=None, nb_groups=5):
    """
    Inputs:
        df_parlament: panda dataframe of parlamentaires.csv
        df_votes: panda dataframe of votes.csv
        given_age_groups: list with age range (age not year), if it's None then eaqual age groups are calc.
    Output:
        df_age: dict. of panda frame containing age groups
        nb_age: dict. containing the number of elements in each group
    """
    # convert birthdate into datetime format
    df_parlament['birthDate'] = pd.to_datetime(df_parlament['birthDate']) 

    # sort df_parlament after age: index 0 = oldest, index 1 = youngest
    df_sorted = df_parlament.sort_values("birthDate")

    df_age = {} # dict. containing df for every age group
    nb_age = {} # dict. containint nb. of persons of every age group
    nb_parlamentarians = df_parlament.count()["ID"]

    # calc. youngest and oldest age
    age_lowest = base_year - df_sorted.iloc[nb_parlamentarians-1]["birthDate"].year
    age_highest = base_year - df_sorted.iloc[0]["birthDate"].year
    age_range = str(age_lowest)+"-"+str(age_highest)

    # add entire dataframe with all persons as reference
    nb_age[age_range] = nb_parlamentarians
    df_age[age_range] = df_votes

    if given_age_groups:
        group_indices = calcGivenAgeGroups(df_sorted, given_age_groups)
    else:
        group_indices = calcEqualAgeGroups(df_sorted, nb_groups)

    for (age_range, index) in group_indices.items():
        inverse_range = list(range(0,index[0])) + list(range(index[1],nb_parlamentarians))
        df_age_inverse = df_sorted.iloc[inverse_range]

        ID_list = df_age_inverse["ID"].astype(str).values.tolist() # convert ID to numpy array full of strings
        #ID_list = [ID_string + ".0" for ID_string in ID_list] # add ".0" because column names require it
        df_age[age_range] = df_votes.drop(ID_list, 1) # drop out all persons not belonging to a certain age group
        nb_age[age_range] = index[1] - index[0]

    return df_age, nb_age

def calcGivenAgeGroups(df_sorted, given_age_groups):
    nb_parlamentarians = df_sorted.count()["ID"]

    group_indices = {}
    prev_age = 0
    prev_index = nb_parlamentarians
    for i in range(nb_parlamentarians):
        index = nb_parlamentarians-i-1
        age = CURRENT_YEAR - df_sorted.iloc[index]["birthDate"].year

        if age>=given_age_groups[len(group_indices)] or i==nb_parlamentarians-1:
            age_range = str(prev_age)+"-"+str(age)
            group_indices[age_range] = [index,prev_index]

            prev_age = age
            prev_index = index
    
    return group_indices


def calcEqualAgeGroups(df_sorted, nb_groups):
    nb_parlamentarians = df_sorted.count()["ID"]
    nb_parl_per_group = int(np.floor(nb_parlamentarians/nb_groups))

    group_indices = {}  
    prev_limit = 0
    for i in range(nb_groups):
        next_limit = prev_limit + nb_parl_per_group
        if i < nb_parlamentarians%nb_groups:
            next_limit += 1

        age_lowest = CURRENT_YEAR - df_sorted.iloc[next_limit-1]["birthDate"].year
        age_highest = CURRENT_YEAR - df_sorted.iloc[prev_limit]["birthDate"].year
        age_range = str(age_lowest)+"-"+str(age_highest)
        
        group_indices[age_range] = [prev_limit,next_limit]
        prev_limit = next_limit

    return group_indices

def extractDepartement(df_votes):
    departments = np.unique(df_votes["Dept."].astype(str).values.tolist())
    
    df_departments = {}
    for dept in departments:
        df_departments[dept] = df_votes[df_votes["Dept."]==dept]

    return df_departments

def calcMeanRiceIndex(df_votes, name_list, column):
    """
    Input:  df_votes:   data frame of votes containing only parlamentarian of interest
            name_list:  list of names (departments, commissions, ...) from "column"
            column:     column that is taken to choose the rows
    Output: mean:       dict. with names from "name_list" as key and mean rice index as value
            nb_votes:   dict. with names from "name_list" as key and number of votes as value
            """
    mean = {}
    nb_votes = {}

    # calc mean rice index of all votes
    mean["all"] = df_votes["Rice index"].mean()
    nb_votes["all"] = df_votes.count()["Rice index"]

    # calc. mean rice index of all rows having "name" in "column"
    for name in name_list:
        particular_vote_bool = df_votes[column].str.contains(name)
        df_particular_vote = df_votes[particular_vote_bool.fillna(False)]

        mean[name] = df_particular_vote["Rice index"].mean()
        nb_votes[name] = df_particular_vote.count()["Rice index"]
    
    return mean, nb_votes
    
def count(string, row):
    """ Count the number of occurrences of `string` in the row
    if row.str.contains(string).any():
        return row.value_counts()[string]
    else:
        return 0"""
    try:
        return row.value_counts()[string]
    except:
        return 0

def rice_index(row):
    """ Compute the Rice index of the row """  
    count_yes = count('Oui', row)
    count_no = count('Non', row)
    if count_yes!=0 or count_no!=0:
        return abs(count_yes - count_no) / (count_yes + count_no)
    else:
        return 1 # change this

def calcRiceIndex(df, df_ref):
        rice_indices = df.apply(lambda row: rice_index(row), axis=1)

        # print("Test: {}".format(df_ref.empty))
        # if df_ref != None:

        rice_indices_ref = df_ref.apply(lambda row: rice_index(row), axis=1)
        rice_indices = rice_indices / rice_indices_ref

        df.insert(0, 'Rice index', rice_indices)
         #votes = votes.sort_values('Rice index')
        return df

def plotMeanRiceIndex(mean, nb_age, nb_votes, title="Average relative Rice Index (RI)", 
                      img_name="rel_RI", description="(nb. of elements per group in brackets)"):
    colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:gray', 'b', 'g', 'r', 'c', 'm', 'y']
    fig = plt.figure(figsize=(9, 6))
    ax1 = fig.add_subplot()
    for i, age in enumerate(mean):
        departments = []
        rice_indices = []
        for subject in mean[age]:
            departments.append(subject+"("+str(nb_votes[subject])+")")
            rice_indices.append(mean[age][subject])
        if i == 0:
            ax1.plot(departments, rice_indices, '--', color='b', label="["+age+"[ "+" ("+str(nb_age[age])+")")
        else:  
            ax1.plot(departments, rice_indices, 'o', color=colors[i], label="["+age+"[ "+" ("+str(nb_age[age])+")")
    ax1.legend(title="Age groups")
    plt.title(title+"\n"+description)
    plt.xlabel("Departments")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("RI(age group of one vote) / RI(all persons of one vote)")
    plt.grid()
    fig.savefig(os.path.join('AnalyseAge_results', img_name+".png"))


if __name__ == "__main__":
    #import dataframes
    dfp = pd.read_csv('processed_data/parlementaires.csv')
    dfv = pd.read_csv('processed_data/votes_finaux.csv')
    dfp.rename(columns={'Unnamed: 0':'ID'}, inplace=True)

    # define departments and commissions
    dept_list_french = ['DFAE','DFI','DFJP','DDPS','DFF','DEFR','DETEC','Parl', 'ChF', 'nan']
    dept_list_german = ['EDA','EDI','EJPD','VBS','EFD','WBF','UVEK','Parl', 'ChF', 'nan']
    commission_list_frensh = ['Bu','CdF','CdG','CPE','CSEC','CSSS','CEATE','CPS','CTT','CER','CIP','CAJ','CdI']
    commission_list_german = ['Bü','FK','GPK','APK','WBK','SGK','UREK','SiK','KVF','WAK','SPK','RK','IK']

    # replace german abbreviation with frensh ones
    dfv["Dept."] = dfv["Dept."].replace(regex=dept_list_german, value=dept_list_french)
    dfv["Commission"] = dfv["Commission"].replace(regex=commission_list_german, value=commission_list_frensh)

    # extract data frames for each age group, either "given_age_groups" provides the age groups
    # or "given_age_groups" is set to "None" and the groups are made that they have a equal size
    nb_age_groups = 3
    given_age_groups = [45,65,120]  
    # given_age_groups = None 
    df_age, nb_age = extractAge(dfp, dfv, given_age_groups=given_age_groups, nb_groups=nb_age_groups)

    # calc. rice index for age groups
    for age in df_age:
        df_age[age] = calcRiceIndex(df_age[age], dfv)

    # calc. relative mean rice index for every department and every age group
    mean_age_dept = {}
    for age in df_age:
        mean_age_dept[age], nb_votes_from_dept = calcMeanRiceIndex(df_age[age], dept_list_french, column='Dept.')

    # calc. relative mean rice index for every commission and every age group
    mean_age_com = {}
    for age in df_age:
        mean_age_com[age], nb_votes_from_com = calcMeanRiceIndex(df_age[age], commission_list_frensh, column='Commission')

    # plot results
    plot_title_dept = "Average relative Rice Index (RI) of departments"
    img_name_dept = "Departments"
    plotMeanRiceIndex(mean_age_dept, nb_age, nb_votes_from_dept, title=plot_title_dept, img_name=img_name_dept)
    plot_title_com = "Average relelative Rice Index (RI) of commissions"
    img_name_com = "Commissions"
    plotMeanRiceIndex(mean_age_com, nb_age, nb_votes_from_com, title=plot_title_com, img_name=img_name_com)
    