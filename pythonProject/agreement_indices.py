import pandas as pd
votes = pd.read_excel('votes_finaux_result.xlsx')
all_votes = pd.read_excel('all_votes_result.xlsx')
votes_indices = votes['VoteRegistrationNumber']
all_votes_indices = all_votes['VoteRegistrationNumber']
def count_yes(row):
    if row.str.contains('Oui').any():
        return row.value_counts()['Oui']
    else :
        return 0
def count_no(row):
    if row.str.contains('Non').any():
        return row.value_counts()['Non']
    else :
        return 0

def count_abs(row):
    if row.str.contains('Abstention').any():
        return row.value_counts()['Abstention']
    else:
        return 0

def PI(row):
    sum = count_yes(row) + count_no(row) + count_abs(row)
    max_ = max(count_yes(row),count_no(row),count_abs(row))
    if(sum < (2* max_ +1)):
        return 100*((2*max_ - sum)/sum)
    else :
        return 0

def RI(row):
    return abs(count_yes(row)-count_no(row))/(count_yes(row)-count_no(row))
def AI(row):
    sum = count_yes(row) + count_no(row) + count_abs(row)
    max_ = max(count_yes(row), count_no(row), count_abs(row))
    return 100*(max_ - 0.5*(sum-max_))/sum
#nb_votes = votes.apply(lambda r: pd.Series({'nb_yes': count_yes(r), 'nb_no': count_no(r), 'nb_abs' : count_abs(r)}),axis=1).transpose()
#nb_votes.to_excel('nb_votes.xlsx')

AI_votes_finaux_1 = votes.apply(lambda r : pd.Series({'PI' : PI(r), 'RI' : RI(r), 'AI' : AI(r)}), axis=1)
AI_votes_finaux = pd.concat([votes_indices, AI_votes_finaux_1],axis=1)
AI_votes_finaux.to_excel('AI_votes_finaux.xlsx')

AI_all_votes_1 = all_votes.apply(lambda r : pd.Series({'PI' : PI(r), 'RI' : RI(r), 'AI' : AI(r)}), axis=1)
AI_all_votes = pd.concat([all_votes_indices, AI_all_votes_1],axis=1)
AI_all_votes.to_excel('AI_all_votes.xlsx')