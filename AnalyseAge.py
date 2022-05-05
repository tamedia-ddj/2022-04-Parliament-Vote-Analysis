import pandas as pd
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np

# +
#import dataframes
dfp = pd.read_csv('processed_data/parlementaires.csv')
dfp.rename(columns={'Unnamed: 0.1':'ID'}, inplace=True)
#dfp = dfp.set_index('Unnamed: 0').transpose()

dfv = pd.read_csv('processed_data/votes.csv') #si on veut que les votes finaux il suffis de changer le fichier
#dfv = dfv.set_index('Unnamed: 0').transpose()

#dfp.info()
#dfv.info()

#print(dfp)
print(dfv)


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

def extractAge(dataframe, age_list, mask=None):
    """
    Inputs:
        dataframe: panda dataframe of parlamentaires.xlsx
        age_list: 2D list with age range (age not year): [range index][lower limit, upper limit]
        mask: preprocess dataframe by taking only indeces defined by mask
    Output:
        numOfPOI: list of Parlementaire Of Interest corresponding to age_list
    """
    if(mask): # if there was a mask provided to the function then apply it
        dataframe = dataframe.loc[mask]

    dataframe['birthDate'] = pd.to_datetime(dataframe['birthDate']) # convert birthdate into datetime format

    current_year = 2022 #datetime.now().year
    numOfPOI = []
    for range in age_list:
        upper_limit = current_year - range[0]
        lower_limit = current_year - range[1]
        #print("up={}, low={}".format(upper_limit, lower_limit))
        df_age = dataframe.loc[(dataframe['birthDate'].dt.year>lower_limit) & (dataframe['birthDate'].dt.year<upper_limit)]
        
        ID_list = df_age["ID"].astype(str).values.tolist()
        ID_list = [ID_string + ".0" for ID_string in ID_list]  
        numOfPOI.append(ID_list)
    return numOfPOI

def extractDepartement(dataframe, department):
    print(dataframe.iloc[3])
    print(dataframe.iloc[3]==department)
    print(dataframe.loc(dataframe.iloc[3]==department).head())
    #dataframe = dataframe[dataframe['Dept.']==department]
    #print(dataframe.head())
    return


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

#PLR = extractParty(dfp,'PLR')
#print(PLR)

age_list = [[0,40],[40,50],[50,60],[60,70],[70,120]]
#mask = [514.0, 4100.0, 4103.0, 4118.0, 4121.0, 4220.0, 1153.0, 4222.0]
numOfPOI = extractAge(dfp, age_list, mask=None)
#print(numOfPOI)
print(numOfPOI)

#department = "DFAE"
#extractDepartement(dfv, department)
dfv_age = dfv.drop(dfv.columns.difference(numOfPOI[0]), 1)
print(dfv_age)

"""
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