from cProfile import label
from cmath import nan
import pandas as pd
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np

# +
#fonction utiles 

def extractParty(dataframe,partyName, mask=None):
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

def extractAge(df_parlament, df_votes, age_list):
    """
    Inputs:
        df_parlament: panda dataframe of parlamentaires.csv
        df_votes: panda dataframe of votes.csv
        age_list: 2D list with age range (age not year): [range index][lower limit, upper limit]
    Output:
        df_age: list of panda frame containing age group
    """

    df_parlament['birthDate'] = pd.to_datetime(df_parlament['birthDate']) # convert birthdate into datetime format

    current_year = 2022 #datetime.now().year
    df_age = {}
    df_age[str(age_list[0][0])+"-"+str(age_list[-1][1])] = df_votes
    for range in age_list:
        upper_limit = current_year - range[0]
        lower_limit = current_year - range[1]
    
        # inveser logic to be able to dropout persons in df_age and keep the first indicative columns of df_votes
        df_age_inverse = df_parlament.loc[(df_parlament['birthDate'].dt.year<lower_limit) | (df_parlament['birthDate'].dt.year>upper_limit)]
        
        ID_list = df_age_inverse["ID"].astype(str).values.tolist() # convert ID to numpy array full of strings
        #ID_list = [ID_string + ".0" for ID_string in ID_list] # add ".0" because column names require it
        df_age[str(range[0])+"-"+str(range[1])] = df_votes.drop(ID_list, 1) # drop out all persons not belonging to a certain age group

    return df_age

def extractDepartement(df_votes):
    departments = np.unique(df_votes["Dept."].astype(str).values.tolist())
    
    df_departments = {}
    for dept in departments:
        df_departments[dept] = df_votes[df_votes["Dept."]==dept]

    return df_departments

def calcMeanDepartment(df_votes, dept_name_list):
    #departments = np.unique(df_votes["Dept."].astype(str).values.tolist())
    mean_dept = {}
    for dept in dept_name_list:
        dept_bool = df_votes["Dept."].str.contains(dept)
        df_dept = df_votes[dept_bool.fillna(False)]

        mean_dept[dept] = df_dept["Rice index"].mean()
    
    return mean_dept

# Auxiliary functions
    
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


if __name__ == "__main__":
    # +
    #import dataframes
    dfp = pd.read_csv('processed_data/parlementaires.csv')
    dfv = pd.read_csv('processed_data/votes_finaux.csv') #si on veut que les votes finaux il suffis de changer le fichier
    dfp.rename(columns={'Unnamed: 0.1':'ID'}, inplace=True)

    # df_departments = extractDepartement(dfv)
    # rise_dept = {}
    # for dept in df_departments:
    #     rice_indices = df_departments[dept].apply(lambda row: rice_index(row), axis=1)
    #     rise_dept[dept].insert(0, 'Rice index', rice_indices)


    age_list = [[0,40],[40,50],[50,60],[60,70],[70,120]]
    df_age = extractAge(dfp, dfv, age_list)

    for age in df_age:
        df_age[age] = calcRiceIndex(df_age[age], dfv)

    dept_name_list = ['DDPS', 'DEFR', 'DETEC', 'DFAE', 'DFF', 'DFI', 'DFJP', 'Parl', 'ChF', 'nan']
    mean_age_dept = {}
    for age in df_age:
        mean_age_dept[age] = calcMeanDepartment(df_age[age], dept_name_list)
    
    colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:gray', 'b', 'g', 'r', 'c', 'm', 'y']
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    for i, age in enumerate(mean_age_dept):
        departments = []
        rice_indices = []
        for j, dept in enumerate(mean_age_dept[age]):
            departments.append(dept)
            rice_indices.append(mean_age_dept[age][dept])
        if i == 0:
            ax1.plot(departments, rice_indices, '--', color='b', label=age)
        else:  
            ax1.plot(departments, rice_indices, 'o', color=colors[i], label=age)
    ax1.legend()
    plt.title("Relatif rice index of age groups for departments")
    plt.xlabel("Departments")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("RI(age group) / RI(of same vote with all persons)")
    plt.grid()
    fig.savefig('AnalyseAge_results/age_department_plot.png')



"""

def extractingPercentage(dataframe,POI,p = 0 ):        
    voteOfPOI = dataframe.loc[POI] #extraction d'un tableau avec uniquement les votes utiles 
    pourcent = np.zeros(voteOfPOI.shape[1])
    for i in range (0,voteOfPOI.shape[1]):
        vote = voteOfPOI.loc[:,i]
        nbOui = int(len(vote.loc[vote == "Oui"]))
        nbNon = int(len(vote.loc[vote == "Non"]))
        nbAbs = int(len(vote.loc[vote == "Abstention"]))
        nb = [nbOui,nbNon,nbAbs]
        m = max(nb)
        tot = nbOui+nbNon+nbAbs
        if tot == 0: #problem car si le tot=0 on ne devrait pas prendre en compte le vote du tout. =<
            tot = 2  #cette partie du code doit être changée... 
        if tot < 2*m+1: #j'ai garde le meme calcul pour le moment...
            pourcent[i] = 100*(2*m-(tot))/(tot)      
        else :
            pourcent[i] = 0
    return pourcent

# +
#creation du histogram en fct de l'age :
PLR = extractParty(dfp,'PLR')
plrP = np.mean(extractingPercentage(dfv,PLR))

ME = extractParty(dfp,'M-E')
meP = np.mean(extractingPercentage(dfv,ME))

PSS = extractParty(dfp,'PSS')
pssP = np.mean(extractingPercentage(dfv,PSS))

UDC = extractParty(dfp,'UDC')
udcP = np.mean(extractingPercentage(dfv,UDC))

VERT = extractParty(dfp,'VERT-E-S')
vertP = np.mean(extractingPercentage(dfv,VERT))

pvl = extractParty(dfp,'pvl')
pvlP = np.mean(extractingPercentage(dfv,pvl))

plot = [meP,plrP,pssP,udcP,vertP,pvlP]
index = ["M-E","PLR","PSS","UDC","VERT-E-S","PVL"]

plt.bar(index,plot)
plt.title("AI party")
plt.xlabel("party")
plt.ylabel("[%]")
plt.savefig('Ai_party.png')
plt.show()"""