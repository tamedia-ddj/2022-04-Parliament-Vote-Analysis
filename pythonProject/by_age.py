import pandas as pd
from datetime import datetime, date
votes = pd.read_excel('votes.xlsx')
parlementaires = pd.read_excel('parlementaires.xlsx')

parlm_1 = parlementaires.transpose().groupby(['birthDate'],axis=0)
print(parlm_1)
born='2000-10-2'
born = datetime.strptime(born, "%Y-%m-%d").date()

# Get today's date
today = date.today()
def age(date) :
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

#parlementaires.apply(lambda r : pd.Series{'id' : , 'age' : age(r)})