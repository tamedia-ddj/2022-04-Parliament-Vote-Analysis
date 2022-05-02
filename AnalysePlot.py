import pandas as pd
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np

# +
#import dataframes
dfp = pd.read_excel('parlementaires.xlsx')
dfp = dfp.set_index('Unnamed: 0').transpose()

dfv = pd.read_excel('votes.xlsx') #si on veut que les votes finaux il suffis de changer le fichier
dfv = dfv.set_index('Unnamed: 0').transpose()


# +
#fonction utiles 

def extractParty(dataframe,partyName) :
    
    numOfPOI = dataframe.loc[dataframe['party'] == partyName].index #POI = Parlementaire Of Interest
    return numOfPOI

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
plt.show()