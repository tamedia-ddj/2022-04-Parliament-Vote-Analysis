import pandas as pd
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np
from dateutil.relativedelta import relativedelta
import numpy.ma as ma

# +
#import dataframes
dfp = pd.read_excel('parlementaires.xlsx')
dfp = dfp.set_index('Unnamed: 0').transpose()

dfv = pd.read_excel('data/votes_finaux.xlsx') #si on veut que les votes finaux il suffis de changer le fichier
dfv = dfv.set_index('Unnamed: 0').transpose()


# +
#import pandas as pd
#from datetime import datetime, timezone
#import matplotlib.pyplot as plt
#
#dfp = pd.read_excel('parlementaires.xlsx')
#dfp = dfp.set_index('Unnamed: 0').transpose()
#dfp['age'] = (datetime.now(tz=timezone.utc) - pd.to_datetime(dfp['birthDate'])).dt.days // 365.25
#
#for name, group in dfp.groupby('party'):
#    if len(group) > 5:
#        print(f'{name} ({len(group)} councillors)')
#        group['age'].hist()
#        plt.show()

# +
#fonction utiles 

def extractParty(dataframe,partyName) :
    
    numOfPOI = dataframe.loc[dataframe['party'] == partyName].index #POI = Parlementaire Of Interest
    return numOfPOI

def extractingPercentage(dataframe,POI,p = 0 ):
    POI.astype('int64')
    voteOfPOI = dataframe.loc[POI] #extraction d'un tableau avec uniquement les votes utiles 
    pourcent = np.zeros(voteOfPOI.shape[1])
    for i in range (0,voteOfPOI.shape[1]):
        vote = voteOfPOI.iloc[:,i]
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
plt.savefig('Ai_party_finaux.png')
plt.show()


# -

#calcul par age et par party:
def extractAgeParty(ageInter, party, dataVote,dataParl):
    party = extractParty(dataParl,party)
    voteOfParty = dataVote.loc[party]
    dataDate = dataVote.loc["VoteDate"]
    birthDate = dataParl.loc[party]["birthDate"]
    maskVote = voteOfParty.copy()
    for i in voteOfParty.columns:
        dateMin = pd.to_datetime(dataDate.loc[i]).date() - relativedelta(years = ageInter[1])
        dateMax = pd.to_datetime(dataDate.loc[i]).date() - relativedelta(years = ageInter[0])
        for j in voteOfParty.index:
            if pd.to_datetime(birthDate.loc[j]).date() <= dateMax and pd.to_datetime(birthDate.loc[j]).date() >= dateMin:
                maskVote.loc[j,i] = voteOfParty.loc[j,i]
            else :
                maskVote.loc[j,i]=0
    return maskVote


def extractingPercentage(voteOfPOI):
    pourcent = np.zeros(voteOfPOI.shape[1])
    for i in range (0,voteOfPOI.shape[1]):
        vote = voteOfPOI.iloc[:,i]
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
age1 = [0,40]
age2 = [40,50]
age3 = [50,60]
age4 = [60,80]

party = "pvl" #changer le party pour avoir les autres graph parmi : ["M-E","PLR","PSS","UDC","VERT-E-S","pvl"]
#PLR dans l'interval 1
votePLR1 = extractAgeParty(age1,party,dfv,dfp)
pourcentPLR1 = extractingPercentage(votePLR1)
plrp1 = np.mean(pourcentPLR1)

#PLR dans l'interval 2
votePLR2 = extractAgeParty(age2,party,dfv,dfp)
pourcentPLR2 = extractingPercentage(votePLR2)
plrp2 = np.mean(pourcentPLR2)

#PLR dans l'interval 3
votePLR3 = extractAgeParty(age3,party,dfv,dfp)
pourcentPLR3 = extractingPercentage(votePLR3)
plrp3 = np.mean(pourcentPLR3)


#PLR dans l'interval 4
votePLR4 = extractAgeParty(age4,party,dfv,dfp)
pourcentPLR4 = extractingPercentage(votePLR4)
plrp4 = np.mean(pourcentPLR4)


#le plot :
plot = [plrp1,plrp2,plrp3,plrp4]
index = ["0-40","40-50","50-60","60-80"]

plt.bar(index,plot)
plt.title("age PVL")
plt.xlabel("party")
plt.ylabel("[%]")
plt.savefig('age_pvl_finaux.png')
plt.show()
# -


